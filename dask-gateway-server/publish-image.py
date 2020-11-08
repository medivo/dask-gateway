#!/usr/bin/env python3
import argparse
import subprocess
import sys


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--no-latest", action="store_true", help="Do not tag this image as latest in repo")
parser.add_argument("tag", help="Version tag to apply to image")


def main(args):
    args = parser.parse_args(args)
    docker_login_cmd = (
        "aws ecr get-login-password --region us-east-1 | "
        "docker login --username AWS --password-stdin 442113982298.dkr.ecr.us-east-1.amazonaws.com"
    )
    subprocess.check_output(docker_login_cmd, shell=True)

    # build images
    for image in ["dask-gateway-server"]:
        # Create repo if it doesn't exist
        try:
            subprocess.check_output(f"aws ecr describe-repositories --repository-names {image}", shell=True)
        except subprocess.CalledProcessError:
            subprocess.check_output(f"aws ecr create-repository --repository-name {image}", shell=True)

        image_repo = f"442113982298.dkr.ecr.us-east-1.amazonaws.com/{image}"
        subprocess.check_output(f"docker build -t {image_repo}:{args.tag} .", shell=True, encoding="UTF-8")
        subprocess.check_output(f"docker push {image_repo}:{args.tag}", shell=True)
        if not args.no_latest:
            subprocess.check_output(f"docker tag {image_repo}:{args.tag} {image_repo}:latest", shell=True)
            subprocess.check_output(f"docker push {image_repo}:latest", shell=True)


if __name__ == "__main__":
    main(sys.argv[1:])
