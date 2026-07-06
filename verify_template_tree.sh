#!/usr/bin/env bash
#
# verify_template_tree.sh
#
# Renders deployment code twice against the SAME inventory/config:
#   1. with the OLD per-file `with_community.general.filetree` + template loop
#   2. with the NEW single-task `template_tree` action plugin
# then diffs the two output trees and reports whether they are byte-for-byte
# identical (contents AND file modes).
#
# The only legitimate difference between the two trees is the absolute output
# path itself, which a few generated scripts embed (e.g. admin/validate-all-yaml).
# The script normalizes that path before diffing so a clean run reports zero diffs.
#
# It temporarily swaps playbooks/roles/template-filetree/tasks/main.yml to the
# old implementation for run #1 and restores your working copy for run #2. An
# EXIT trap always restores your working copy, even on Ctrl-C or error.
#
# Usage:
#   ./verify_template_tree.sh -i <inventory.yml> [-l <host>] [-w <workdir>] [-- <extra ansible-playbook args>]
#
# Examples:
#   ./verify_template_tree.sh -i /home/kprice/ansible_inventory/kube-inventory.yml
#   ./verify_template_tree.sh -i inv.yml -l tapisquickstart-kube1
#   # exclude mlhub and pass dummy globus creds, as in local testing:
#   ./verify_template_tree.sh -i inv.yml -- \
#     -e '{"components_to_deploy":["actors","apps","tokens","proxy"]}' \
#     -e globus_client_id=00000000-0000-0000-0000-000000000000 -e globus_client_secret=x
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAYBOOKS_DIR="$SCRIPT_DIR/playbooks"
MAIN_YML="$PLAYBOOKS_DIR/roles/template-filetree/tasks/main.yml"
GENERATE_YML="$PLAYBOOKS_DIR/generate.yml"

INVENTORY=""
HOST_LIMIT=""
WORKDIR=""
EXTRA_ARGS=()

usage() { sed -n '2,33p' "$0"; exit "${1:-0}"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    -i) INVENTORY="$2"; shift 2 ;;
    -l) HOST_LIMIT="$2"; shift 2 ;;
    -w) WORKDIR="$2"; shift 2 ;;
    -h|--help) usage 0 ;;
    --) shift; EXTRA_ARGS=("$@"); break ;;
    *) echo "Unknown argument: $1" >&2; usage 1 ;;
  esac
done

[[ -n "$INVENTORY" ]] || { echo "ERROR: -i <inventory> is required" >&2; usage 1; }
[[ -f "$INVENTORY" ]] || { echo "ERROR: inventory not found: $INVENTORY" >&2; exit 1; }
[[ -f "$MAIN_YML"   ]] || { echo "ERROR: cannot find $MAIN_YML" >&2; exit 1; }
command -v ansible-playbook >/dev/null || { echo "ERROR: ansible-playbook not on PATH" >&2; exit 1; }

WORKDIR="${WORKDIR:-$(mktemp -d "${TMPDIR:-/tmp}/tt-verify.XXXXXX")}"
mkdir -p "$WORKDIR"
OLD_OUT="$WORKDIR/old_out"
NEW_OUT="$WORKDIR/new_out"
BACKUP="$WORKDIR/main.yml.working"

LIMIT_ARGS=()
[[ -n "$HOST_LIMIT" ]] && LIMIT_ARGS=(--limit "$HOST_LIMIT")

echo "==> Workdir:        $WORKDIR"
echo "==> Inventory:      $INVENTORY"
[[ -n "$HOST_LIMIT" ]] && echo "==> Host limit:     $HOST_LIMIT"
echo "==> Old output:     $OLD_OUT"
echo "==> New output:     $NEW_OUT"
echo

# Preserve the working (new-plugin) main.yml and guarantee its restoration.
cp -p "$MAIN_YML" "$BACKUP"
restore_working() {
  cp -p "$BACKUP" "$MAIN_YML"
}
trap restore_working EXIT

# The OLD implementation: per-file filetree loop. Written verbatim from the
# pre-plugin version of the role so this script stays valid even after the
# original is dropped from git history.
write_old_impl() {
  cat > "$MAIN_YML" <<'OLD_EOF'
---

- name: 'create {{ calling_rolename }} base dir: {{ tapisdir }}/{{ tree_name }}'
  ansible.builtin.file:
    state: directory
    path: '{{ tapisdir }}/{{ tree_name }}'

- name: 'ensure directory structure exists for {{ calling_rolename }} in {{ tapisdir }}/{{ tree_name }}'
  ansible.builtin.file:
    path: '{{ tapisdir }}/{{ tree_name }}/{{ item.path }}'
    state: directory
  with_community.general.filetree: '../{{ calling_rolename }}/templates/{{ tapisflavor }}/'
  when: item.state == 'directory'

- name: 'populate files from templates for {{ calling_rolename }} in {{ tapisdir }}/{{ tree_name }}'
  ansible.builtin.template:
    src: '{{ item.src }}'
    dest: '{{ tapisdir }}/{{ tree_name }}/{{ item.path }}'
    mode: preserve
  with_community.general.filetree: '../{{ calling_rolename }}/templates/{{ tapisflavor }}/'
  when: item.state == 'file'
OLD_EOF
}

run_generate() {
  # $1 = label, $2 = output tapisdir
  local label="$1" out="$2"
  rm -rf "$out"
  echo "==> [$label] rendering into $out ..."
  local start end rc
  start=$(date +%s)
  set +e
  ansible-playbook -i "$INVENTORY" "$GENERATE_YML" \
    "${LIMIT_ARGS[@]}" -e "tapisdir=$out" "${EXTRA_ARGS[@]}" \
    > "$WORKDIR/$label.log" 2>&1
  rc=$?
  set -e
  end=$(date +%s)
  local nfiles
  nfiles=$(find "$out" -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "    [$label] rc=$rc  wall=$((end - start))s  files=$nfiles  (log: $WORKDIR/$label.log)"
  if [[ $rc -ne 0 ]]; then
    echo "    [$label] WARNING: ansible-playbook returned non-zero. Last error(s):"
    grep -m3 -iE "undefined|fatal:|ERROR|failed=[1-9]" "$WORKDIR/$label.log" | sed 's/^/      /' || true
  fi
  return 0
}

# ---- Run #1: OLD engine ----
write_old_impl
run_generate old "$OLD_OUT"

# ---- Run #2: NEW engine (restore your working main.yml) ----
restore_working
run_generate new "$NEW_OUT"

echo
echo "==> Comparing output trees (normalizing the embedded output path) ..."

# 1) Structural diff: which files exist on only one side?
missing=0
diff <(cd "$OLD_OUT" && find . -type f | sort) \
     <(cd "$NEW_OUT" && find . -type f | sort) > "$WORKDIR/tree.diff" || missing=1
if [[ $missing -ne 0 ]]; then
  echo "    FILE SET DIFFERS (see $WORKDIR/tree.diff):"
  sed 's/^/      /' "$WORKDIR/tree.diff"
fi

# 2) Content diff, file by file, normalizing OLD_OUT/NEW_OUT -> __TAPISDIR__.
content_diffs=0
while IFS= read -r f; do
  rel="${f#"$OLD_OUT"/}"
  nf="$NEW_OUT/$rel"
  [[ -f "$nf" ]] || continue
  if ! diff -q \
        <(sed "s#$OLD_OUT#__TAPISDIR__#g" "$f") \
        <(sed "s#$NEW_OUT#__TAPISDIR__#g" "$nf") >/dev/null 2>&1; then
    echo "    CONTENT DIFF: $rel"
    content_diffs=$((content_diffs + 1))
  fi
done < <(find "$OLD_OUT" -type f)

# 3) File-mode diff.
mode_diffs=0
diff <(cd "$OLD_OUT" && find . -type f -exec stat -c '%a %n' {} \; | sort) \
     <(cd "$NEW_OUT" && find . -type f -exec stat -c '%a %n' {} \; | sort) \
     > "$WORKDIR/modes.diff" || mode_diffs=1
if [[ $mode_diffs -ne 0 ]]; then
  echo "    FILE MODES DIFFER (see $WORKDIR/modes.diff):"
  sed 's/^/      /' "$WORKDIR/modes.diff"
fi

echo
if [[ $missing -eq 0 && $content_diffs -eq 0 && $mode_diffs -eq 0 ]]; then
  echo "==> RESULT: IDENTICAL — old and new engines produced byte-for-byte identical output."
  exit 0
else
  echo "==> RESULT: DIFFERENCES FOUND (file-set: $missing, content: $content_diffs, modes: $mode_diffs)."
  echo "    Output trees kept for inspection under: $WORKDIR"
  exit 1
fi
