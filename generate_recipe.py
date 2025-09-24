#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
import argparse

# List of architectures and UIs
architectures = ["arm64", "armhf", "amd64"]
uis = ["plasma", "plasma-mobile"]

# Common suffix for all files
suffix = datetime.today().strftime('%Y%m%d')

# Function to generate the content
def generate_content(architecture, ui):
    return f"""{{{{- $product := or .product "rootfs" -}}}}
{{{{- $architecture := or .architecture "{architecture}" -}}}}
{{{{- $suffix := or .suffix "{suffix}" -}}}}
{{{{- $edition := or .edition "{ui}" -}}}}
{{{{- $version := or .version "nightly" -}}}}
{{{{- $mtype := or .mtype "OFFICIAL" -}}}}
{{{{- $image := or .image (printf "droidian-%s-%s-%s-%s-%s_%s.zip" $mtype $edition $architecture $version $suffix) -}}}}
{{{{- $output_type := or .output_type "rootfs" -}}}}
{{{{- $use_internal_repository := or .use_internal_repository "no" -}}}}

architecture: {{{{ $architecture }}}}
actions:

  - action: run
    description: Do nothing
    chroot: false
    command: echo "Doing nothing!"

  - action: recipe
    description: Build Droidian
    recipe: ../rootfs-templates/lindroid_{ui}.yaml
    variables:
      architecture: {{{{ $architecture }}}}
      suffix: {{{{ $suffix }}}}
      edition: {{{{ $edition }}}}
      version: {{{{ $version }}}}
      image: {{{{ $image }}}}
      output_type: {{{{ $output_type }}}}
      use_internal_repository: {{{{ $use_internal_repository }}}}
"""

# Directory to save generated files
output_dir = "generated"
os.makedirs(output_dir, exist_ok=True)

# Generate files and matrix
matrix = []
for architecture in architectures:
    for ui in uis:
        filename = f"lindroid-{ui}-{architecture}.yaml"
        filepath = os.path.join(output_dir, filename)
        content = generate_content(architecture, ui)
        with open(filepath, 'w') as file:
            file.write(content)

        job_name = f"rootfs ({ui} edition) - {architecture}"
        matrix.append({
            "job_name": job_name,
            "product": "rootfs",
            "arch": architecture,
            "edition": ui
        })

# Parse arguments for matrix generation
parser = argparse.ArgumentParser(description='Generate device recipe files and matrix.')
parser.add_argument('--matrix', action='store_true', help='Generate and display the matrix.')
args = parser.parse_args()

# Display the matrix if the --matrix flag is set
if args.matrix:
    print(json.dumps(matrix, indent=4))
