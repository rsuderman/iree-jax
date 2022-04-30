# Copyright 2021 The IREE Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import json
import os
from setuptools import find_namespace_packages, setup

# Setup and get version information.
THIS_DIR = os.path.realpath(os.path.dirname(__file__))
VERSION_INFO_FILE = os.path.join(THIS_DIR, "version_info.json")


def load_version_info():
  with open(VERSION_INFO_FILE, "rt") as f:
    return json.load(f)


try:
  version_info = load_version_info()
except FileNotFoundError:
  print("version_info.json not found. Using defaults")
  version_info = {}

PACKAGE_SUFFIX = version_info.get("package-suffix") or ""
PACKAGE_VERSION = version_info.get("package-version") or "0.1dev1"


def get_pinned_package(name):
  pinned_versions = version_info.get("pinned-versions")
  if not pinned_versions or name not in pinned_versions:
    return name
  else:
    return f"{name}=={pinned_versions[name]}"

setup(
    name=f"iree-jax{PACKAGE_SUFFIX}",
    version=f"{PACKAGE_VERSION}",
    packages=find_namespace_packages(include=[
        "iree.jax",
        "iree.jax.*",
    ],),
    install_requires=[
        "numpy",
        get_pinned_package("jax"),
        get_pinned_package("iree-compiler"),
        get_pinned_package("iree-runtime"),
    ],
    extras_require={
      "xla": [
        get_pinned_package("iree-tools-xla"),
      ],
      "cpu": [
        get_pinned_package("jaxlib"),
      ],
      "test": [
        "lit",
      ]
    },
)
