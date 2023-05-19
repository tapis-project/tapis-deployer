# Tapis Deployer 

The Tapis Deployer software generates scripts for deploying and manging a Tapis installation.
Tapis Deployer is based on the Ansible project. Currently, Tapis Deployer targets Kubernetes clusters
for deployment of Tapis services, but we plan to support using Docker Compose instead of Kubernetes
in a future release. 

## User Documentation

Full documentation is being developed for Tapis Deployer on the Tapis ReadTheDocs site. See 
the [Deployment & Administration Guide](https://tapis.readthedocs.io/en/latest/deployment/index.html). 


## Developer Documentation


### Developer Guide

- Create a branch off of the *dev* branch
  - Optional: Name it after your new feature or change, i.e. "refactor-tapisui"
- Make and commit your changes to your branch
  - For example, to increase the image version for the Apps API images, edit the file `playbooks/roles/apps/defaults/main/images.yml`
  - Include a note about your changes in the CHANGELOG.md. 
    - Link to your component's CHANGELOG.md details for the new version. For example: 
      - [Tapis Systems version change from 1.3.1 to 1.3.2](https://github.com/tapis-project/tapis-systems/blob/local/CHANGELOG.md#132---2023-04-25)
  - **Note** Your changes could affect other services, so please be sure to describe these issues in CHANGELOG.md, especially if there are breaking changes or if your require additional steps for upgrade.
- Create a Pull Request from your branch against the source (*dev*).  


### Getting Changes into a Tapis Deployer Release

- Once your changes are in *dev* branch (see above), Testers/Admins/Maintainers can then deploy and test your changes amongst various environments.
  - This should be accompanied by an increase in the `baseburnup_tapis_deployer_version` variable in `playbooks/roles/baseburnup/defaults/main/vars.yml` (Maintainers do this.)
- After successful testing and combined with other devs' changes, *dev* branch will be merged with *staging* in preparation for a release.
- After successful testing in *staging* branch, it will be merged into *main* by Tapis Deployer Maintainers and a new release will be created.
