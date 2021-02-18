#!/bin/bash
file_url=$(curl --silent "https://api.github.com/repos/ambanum/CGUs-versions/releases/latest" | grep '"browser_download_url":' | sed -E 's/.*"([^"]+)".*/\1/');
curl -LJS $file_url -o dataset.zip
unzip dataset.zip && mv dataset-* dataset