#!/usr/bin/env python3
import json
import subprocess
import sys


def main(args):
    docker_login_cmd = (
        "docker login -u AWS -p $(aws --profile ds ecr get-login-password --region us-east-1) "
        "442113982298.dkr.ecr.us-east-1.amazonaws.com"
    )
    subprocess.check_output(docker_login_cmd, shell=True)

    for image in ["dask-gateway-server"]:
        print(image)
        list_tags_cmd = f"aws ecr list-images --repository-name {image}"
        tags_json = subprocess.check_output(list_tags_cmd, shell=True, encoding="UTF-8")
        tags = json.loads(tags_json)["imageIds"]
        tags = [tag.get("imageTag", "") for tag in tags]
        for tag in sorted(tags):
            print(f"\t{tag}")


if __name__ == "__main__":
    main(sys.argv[1:])
