# Tapis Deployer 

The Tapis Deployer software generates scripts for deploying and manging a Tapis installation.
Tapis Deployer is based on the Ansible project. Currently, Tapis Deployer targets Kubernetes clusters
for deployment of Tapis services, but we plan to support using Docker Compose instead of Kubernetes
in a future release. 

## User Documentation

Full documentation is being developed for Tapis Deployer on the Tapis ReadTheDocs site. See 
the [Deployment & Administration Guide](https://tapis.readthedocs.org/deployment/index.html). 


## Developing Deployer

This section describes the process by which changes are made to Deployer itself. 

_In progress..._

### Procedures for normal development (By Developers and Deployer Maintainers together) 

    DEVs: create a temporary feature branch off of tapis-deployer dev branch (https://github.com/tapis-project/tapis-deployer)
        could be named for feature i.e. "refactor-tapisui" 
        put all changes you wish to make into this branch
        push your branch to github
        when happy with these changes as a batch, create a PR from this branch to dev
    Maintainers
        Maintainers: folks will review and iterate on the PR, maybe decline, ask for edits, etc
        Maintainers: once happy with the changes, folks will merge into dev  
    Maintainers will create PRs to merge dev into staging
        After some amount of testing and iteration
        Create a PR to bring changes from dev branch to staging
        Additional folks may review PR or just merge it.

### Procedures for NEW TAPIS RELEASE (IN PROGRESS, draft)

Performed by Deployer Maintainer Persons

This applies to a quick image-version-only increment or a more substantial release after some development by above procedure.

    Maintainers gather feedback and change requirements for new release. i.e. Ask developers, maintainers, users. This can be a longer dev process or a quick version-only change.
        For image-version-only changes, developers request an update to one or more production Tapis services. Requests are informal and take the form of a slack message on the tapis-deployer channel.
    Create a TEMPORARY branch from main called <next vesion of deployer>
        i.e. 1.3.99-rc
    bring in desired changes
        if it's a quick image version adjustment, maintainers change image numbers in tapis-deployer/playbooks/roles/<component>/defaults/main/images.yml
            The only changes to deployer are new image tags for the target services.
        if more substantial release, manually curate the changes from the staging branch into this RC branch
    update release notes

    increment the deployer version in https://github.com/tapis-project/tapis-deployer/blob/main/playbooks/roles/baseburnup/defaults/main/vars.yml (e.g.

        baseburnup_tapis_deployer_version: 1.3.99
    merge to main & immediately tag this new commit as a version "v1.3.99"
    send announcement of new release <boilerplate template HERE TBD>?

## Developer Guide

- Create a branch off of the appropriate trunk branch 
  - If you want a very simple change, like a change to a component image version, quick bugfix, etc., branch off of *main* branch. 
  - If it's a more elaborate change, branch off of *dev* branch. 
- Make and commit your changes 
  - For example, to increase the image version for the Apps API images, edit the file `playbooks/roles/apps/defaults/main/images.yml`
- Create a Pull Request from your branch against the branch you created the branch from, *main* or *dev* 
- Testers can pull and test your changes before merging into the common branches and creating a new release.

