"""
This program computes the service differences (in terms of docker image tags) between two
delpoyer releases and generates an associated change log for the two deployer releases.
"""
import requests
import yaml

DEPLOYER_GITHUB_IMAGE_VAR_BASE_URL = "https://raw.githubusercontent.com/tapis-project/tapis-deployer/<version>/"

DEPLOYER_GITHUB_IMAGE_VAR_FILE_PATH = {
    "actors": "playbooks/roles/actors/defaults/main/images.yml",
    "apps": "playbooks/roles/apps/defaults/main/images.yml",
    "authenticator": "playbooks/roles/authenticator/defaults/main/images.yml",
    "files": "playbooks/roles/files/defaults/main/images.yml",
    "globus_proxy":"playbooks/roles/globus-proxy/defaults/main/images.yml",
    "jobs": "playbooks/roles/jobs/defaults/main/images.yml",
    "meta": "playbooks/roles/meta/defaults/main/images.yml",
    "notifications": "playbooks/roles/notifications/defaults/main/images.yml",
    "pgrest": "playbooks/roles/pgrest/defaults/main/images.yml",
    "pods": "playbooks/roles/pods/defaults/main/images.yml",
    "security": "playbooks/roles/security/defaults/main/images.yml",
    "streams": "playbooks/roles/streams/defaults/main/images.yml",
    "systems": "playbooks/roles/systems/defaults/main/images.yml",
    "tenants": "playbooks/roles/tenants/defaults/main/images.yml",
    "tokens": "playbooks/roles/tokens/defaults/main/images.yml",
    "workflows": "playbooks/roles/workflows/defaults/main/images.yml",
}

CHANGELOG_URLS = {
    "actors": {
      "url": "https://raw.githubusercontent.com/TACC/abaco/blob/k8-v3/CHANGELOG.md",
      "images": ["abaco/core-v3", "abaco/promv3", "abaco/nginxk8s"],
    },
    "apps": {
      "url": "https://raw.githubusercontent.com/tapis-project/tapis-apps/blob/prod/CHANGELOG.md",
      "images": ["tapis/apps"],
    },
    "authenticator": {
      "url": "https://raw.githubusercontent.com/tapis-project/authenticator/prod/CHANGELOG.md",
      "images": ["tapis/authenticator", "tapis/authenticator-migrations"],
    },
    "files": {
      "url": "https://raw.githubusercontent.com/tapis-project/tapis-files/blob/prod/CHANGELOG.md",
      "images": ["tapis/tapis-files", "tapis/tapis-files-workers"],
    },
    "globus_proxy": {
      "url": "",
      "images": [],
    },
    "jobs": {
      "url": "https://raw.githubusercontent.com/tapis-project/tapis-jobs/blob/dev/tapis-jobsapi/CHANGELOG.md",
      "images": ["tapis/jobapi", "tapis/jobsmigrate", "tapis/jobsworker"],
    },
    "meta": {
      "url": "https://raw.githubusercontent.com/tapis-project/tapis-meta/blob/dev/CHANGELOG.md",
      "images": ["tapis/tapis-meta-rh-server", "tapis/mongo-singlenode", "tapis/tapis-meta-rh-server:1.3.0-vdj"],
    },
    "notifications": {
      "url": "https://raw.githubusercontent.com/tapis-project/tapis-notifications/blob/prod/CHANGELOG.md",
      "images": ["tapis/notifications", "tapis/notifications-dispatcher"],
    },
    "pgrest": {
      "url": "https://raw.githubusercontent.com/tapis-project/paas/blob/prod/CHANGELOG.md",
      "images": ["tapis/pgrest-api"],
    },
    "pods": {
      "url": "https://raw.githubusercontent.com/tapis-project/pods_service/blob/prod/CHANGELOG.md",
      "images": ["tapis/pods-api", "notchristiangarcia/traefik-testing"],
    },
    "security": {
      "url": "https://raw.githubusercontent.com/tapis-project/tapis-security/blob/dev/tapis-securityapi/CHANGELOG.md",
      "images": ["tapis/securityapi", "tapis/securityadmin", "tapis/securityexport", "tapis/securitymigrate"],
    },
    "streams": {
      "url": "https://raw.githubusercontent.com/tapis-project/streams-api/prod/CHANGELOG.md",
      "images": ["tapis/streams-api", "scleveland/tapis-chords-app:0.9.8.2.3"],
    },
    "systems": {
      "url": "https://raw.githubusercontent.com/tapis-project/tapis-systems/blob/prod/CHANGELOG.md",
      "images": ["tapis/systems"],
    },
    "tenants": {
      "url": "https://raw.githubusercontent.com/tapis-project/tenants-api/prod/CHANGELOG.md",
      "images": ["tapis/tenants-api", "tapis/tenants-api-migrations"],
    },
    "tokens": {
      "url": "https://raw.githubusercontent.com/tapis-project/tokens-api/prod/CHANGELOG.md",
      "images": ["tapis/tokens-api"],
    },
    "workflows": {
      "url": "",
      "images": [],
    },

}

def get_tapis_images_for_deployer_version(version):
    """
    Retrieves the Tapis images associated with a specific `version` of the deployer as 
    a set of image strings, with tags.
    Returns a dictionary with keys that are the service names and values that are lists of the
    images, as strings. e.g., 

    images = {
      'actors': ['abaco/core-v3:1.3.0', 'grafana/grafana'', ],
      'apps': ['tapis/apps:1.3.0', 'postgres:12.4'],
      . . .
    }
    """
    images = {}
    base_url = DEPLOYER_GITHUB_IMAGE_VAR_BASE_URL.replace("<version>", version)
    for service, url_path in DEPLOYER_GITHUB_IMAGE_VAR_FILE_PATH.items():
        # look up the file associates with the images for the service in deployer
        url = f"{base_url}{url_path}"
        # make a get request to fetch the file
        try:
            rsp = requests.get(url)
            rsp.raise_for_status()
        except Exception as e:
            print(f"Could not retrieve images for service {service} from Github.\n URL: {url}; Exception: {e}")
        try:
            images_dict = yaml.safe_load(rsp.content)
        except Exception as e:
            print(f"Could not load images as yaml for service {service}; content: {rsp.content}. Exception: {e}")
        images[service] = []
        # the images_dict is a simple key:value pairs dictionary with key being the name 
        # (i.e, Ansible variable) of the image and the value being the docker image, including the tag.
        # 
        for _, value in images_dict.items():
            images[service].append(value)
    return images 

def compare_deployer_version_images(images_v1, images_v2):
    """
    Compares the images returned from the get_tapis_images_for_deployer_version for 
    two deployer versions. 
    Returns
    """
    comparison = {
        "changed": {},
        "unchanged": {}
    }
    for service, image_list in images_v2.items():
        comparison["changed"][service] = []
        comparison["unchanged"][service] = []
        for img in image_list:
            # look up the image in images_v1
            if img in images_v1[service]:
                # if the image is in the list, we know it is an unchanged version
                comparison["unchanged"][service].append(img)
            # otherwise, it is a change, so check for tag
            else:
                # if the image has a tag, look for an image with the same name and a 
                # different tag
                if ":" in img:
                    parts = img.split(":")
                    img_name = parts[0]
                    img_tag = parts[1]
                    for img1 in images_v1[service]:
                        if ':' not in img1:
                            # it's possible the image changed from not having a tag to 
                            # having one, in which case we will find a match with the entire
                            # img1.
                            if img1 == img_name:
                                comparison["changed"][service].append({
                                    "new": img,
                                    "prev": img1,
                                })
                                break
                            else:
                                continue
                        parts1 = img1.split(':')
                        img1_name = parts1[0]
                        img1_tag = parts1[1]
                        # we found a match, so the tag difference is the difference we 
                        # need to record
                        if img1_name == img_name:
                            comparison["changed"][service].append({
                                "new": img,
                                "prev": img1,
                            })
                            break
                    else:
                        # if we get to the end of the for loop without finding the image, add
                        # the whole image as changed
                        comparison["changed"][service].append({
                                "new": img,
                                "prev": None,
                        })
                # if the image does not have a tag, we assume it is a completely changed
                # image with no previous counterpart. 
                else:
                    comparison["changed"][service].append({
                                "new": img,
                                "prev": None,
                            })
    return comparison


def main():
    # valid options include tags that exist, e.g., "v1.3.1", "v1.3.0", ... as well as
    # branches, e.g., "dev", "main".
    version_1 = 'v1.3.0'
    version_2 = 'v1.3.1'
    version_3 = 'dev'
    images_v1 = get_tapis_images_for_deployer_version(version_1)
    images_v2 = get_tapis_images_for_deployer_version(version_2)
    images_v3 = get_tapis_images_for_deployer_version(version_3)
    comparison_1 = compare_deployer_version_images(images_v1, images_v2)
    comparison_2 = compare_deployer_version_images(images_v1, images_v3)
    return images_v1, images_v2, images_v3, comparison_1, comparison_2

if __name__ == '__main__':
    main()



        



