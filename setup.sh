#!/bin/bash

# only supporting nix/mac on amd64, im lazy ok..

[[ $# -gt 0 && "--venv" =~ $@ ]] && venv=true || venv=false

if [[ $EUID -ne 0 && $venv == "false" ]]; then
    echo "This script must be either run as root or within a virtual environment." 1>&2
    exit 1
fi

OS=$(uname)
ARCH="amd64"

case $OS in
    "Linux")
        BINARY_NAME="linux_${ARCH}.zip"
        ;;
    "Darwin")
        BINARY_NAME="macOS_${ARCH}.zip"
        ;;
    *)
        echo "Unsupported OS"
        exit 1
        ;;
esac

VERSION=$(curl -s https://api.github.com/repos/projectdiscovery/subfinder/releases/latest | grep "tag_name" | cut -d '"' -f 4 | tr -d 'v') # cursed af lol
echo "Version: $VERSION"  # Debugging line

FULL_BINARY_NAME="subfinder_${VERSION}_${BINARY_NAME}"
echo "Binary Name: $FULL_BINARY_NAME"  # Debugging line

SUBFINDER_URL=$(curl -s https://api.github.com/repos/projectdiscovery/subfinder/releases/latest | grep browser_download_url | grep $FULL_BINARY_NAME | cut -d '"' -f 4)
echo "Download URL: $SUBFINDER_URL"  # Debugging line

wget $SUBFINDER_URL -O subfinder.zip
unzip subfinder.zip
chmod +x subfinder
rm subfinder.zip

exit 1
