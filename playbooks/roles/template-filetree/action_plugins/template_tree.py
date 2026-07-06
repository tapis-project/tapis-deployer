# Copyright: (c) 2026, Tapis Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# template_tree: render an entire directory tree of Jinja2 templates in a single
# task, in-process on the controller.
#
# Why this exists
# ---------------
# The deployer previously rendered files with a `with_community.general.filetree`
# loop over `ansible.builtin.template`. That invokes the template action plugin
# (and the copy action plugin underneath it) once per file. On localhost the
# per-item overhead dominates -- ~0.7s/file -- so a full generate of ~900 files
# took the better part of ten minutes despite the actual Jinja rendering being
# trivial.
#
# This plugin walks the template directory once and renders every file using the
# same templating path as `ansible.builtin.template` (AnsibleEnvironment,
# trim_blocks on, mode preserve, identical searchpath/template-vars), but without
# a per-file module round-trip. Output is byte-for-byte identical to the old
# loop; only the wall-clock changes.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import stat

from ansible.errors import AnsibleActionFail, AnsibleError
from ansible.module_utils._text import to_bytes, to_text, to_native
from ansible.plugins.action import ActionBase
from ansible.template import generate_ansible_template_vars, AnsibleEnvironment


class ActionModule(ActionBase):

    TRANSFERS_FILES = False
    DEFAULT_NEWLINE_SEQUENCE = "\n"

    def _resolve_src_tree(self, calling_rolename, tapisflavor, task_vars):
        """Locate roles/<calling_rolename>/templates/<tapisflavor>/.

        Mirrors how the old filetree loop resolved '../<role>/templates/<flavor>/'.
        Tries the playbook basedir first (the canonical layout), then falls back
        to walking the role search paths so the plugin keeps working if it is
        ever invoked from a different working directory.
        """
        rel = os.path.join('roles', calling_rolename, 'templates', tapisflavor)

        candidates = []
        basedir = self._loader.get_basedir()
        if basedir:
            candidates.append(os.path.join(basedir, rel))
        for p in task_vars.get('ansible_search_path', []):
            candidates.append(os.path.join(p, rel))

        for cand in candidates:
            if os.path.isdir(to_bytes(cand)):
                return os.path.realpath(cand)

        # Last resort: let the loader's needle search find it.
        try:
            found = self._find_needle('templates', os.path.join('..', calling_rolename, 'templates', tapisflavor))
            if found and os.path.isdir(to_bytes(found)):
                return os.path.realpath(found)
        except AnsibleError:
            pass

        raise AnsibleActionFail(
            "template_tree: could not locate template directory '%s' (tried: %s)"
            % (rel, ', '.join(candidates))
        )

    def _render_one(self, source, dest, src_arg, task_vars):
        """Render a single template exactly like ansible.builtin.template.

        Returns the rendered text. Raises AnsibleActionFail on any error,
        annotated with the offending source path so failures stay debuggable.
        """
        b_source = to_bytes(source, errors='surrogate_or_strict')
        try:
            with open(b_source, 'rb') as f:
                try:
                    template_data = to_text(f.read(), errors='surrogate_or_strict')
                except UnicodeError:
                    raise AnsibleActionFail("Template source files must be utf-8 encoded: %s" % source)

            # Jinja2 include/import searchpath -- same construction as template.py:
            # each search path plus its 'templates' subdir.
            searchpath = list(task_vars.get('ansible_search_path', []))
            searchpath.extend([self._loader._basedir, os.path.dirname(source)])
            newsearchpath = []
            for p in searchpath:
                newsearchpath.append(os.path.join(p, 'templates'))
                newsearchpath.append(p)
            searchpath = newsearchpath

            temp_vars = task_vars.copy()
            temp_vars.update(generate_ansible_template_vars(src_arg, source, dest))

            templar = self._templar.copy_with_new_env(
                environment_class=AnsibleEnvironment,
                searchpath=searchpath,
                newline_sequence=self.DEFAULT_NEWLINE_SEQUENCE,
                trim_blocks=True,
                lstrip_blocks=False,
                available_variables=temp_vars,
            )
            return templar.do_template(
                template_data,
                preserve_trailing_newlines=True,
                escape_backslashes=False,
            )
        except AnsibleActionFail:
            raise
        except Exception as e:
            raise AnsibleActionFail("template_tree: failed rendering %s: %s: %s"
                                    % (source, type(e).__name__, to_native(e)))

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp

        calling_rolename = self._task.args.get('calling_rolename')
        tapisflavor = self._task.args.get('tapisflavor')
        dest_base = self._task.args.get('dest')

        for name, val in (('calling_rolename', calling_rolename),
                          ('tapisflavor', tapisflavor),
                          ('dest', dest_base)):
            if not val:
                raise AnsibleActionFail("template_tree: '%s' is required" % name)

        check_mode = self._task.check_mode
        src_tree = self._resolve_src_tree(calling_rolename, tapisflavor, task_vars)
        dest_base = os.path.expanduser(dest_base)

        created_dirs = 0
        written_files = 0

        # Always ensure the destination base exists.
        if not os.path.isdir(to_bytes(dest_base)):
            if not check_mode:
                os.makedirs(to_bytes(dest_base))
            created_dirs += 1

        # Walk the template tree once. os.walk is top-down, so parent dirs are
        # created before their children.
        for root, dirs, files in os.walk(to_text(src_tree)):
            rel_root = os.path.relpath(root, src_tree)

            for d in sorted(dirs):
                rel = d if rel_root == os.curdir else os.path.join(rel_root, d)
                target = os.path.join(dest_base, rel)
                if not os.path.isdir(to_bytes(target)):
                    if not check_mode:
                        os.makedirs(to_bytes(target))
                    created_dirs += 1

            for fname in sorted(files):
                source = os.path.join(root, fname)
                rel = fname if rel_root == os.curdir else os.path.join(rel_root, fname)
                target = os.path.join(dest_base, rel)
                # 'src_arg' is the path as the template module would have seen it
                # (relative to the templates dir) -- only surfaces via the
                # generate_ansible_template_vars template_* vars.
                src_arg = os.path.join('..', calling_rolename, 'templates', tapisflavor, rel)

                rendered = self._render_one(source, target, src_arg, task_vars)

                if not check_mode:
                    parent = os.path.dirname(target)
                    if parent and not os.path.isdir(to_bytes(parent)):
                        os.makedirs(to_bytes(parent))
                    with open(to_bytes(target, errors='surrogate_or_strict'), 'wb') as f:
                        f.write(to_bytes(rendered, encoding='utf-8', errors='surrogate_or_strict'))
                    # mode: preserve -- match the source file's permission bits.
                    src_mode = stat.S_IMODE(os.stat(to_bytes(source)).st_mode)
                    os.chmod(to_bytes(target), src_mode)
                written_files += 1

        result['changed'] = True
        result['created_dirs'] = created_dirs
        result['written_files'] = written_files
        result['src_tree'] = src_tree
        result['dest'] = dest_base
        return result
