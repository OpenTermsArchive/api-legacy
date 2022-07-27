#!/bin/bash
file_url=$(curl --silent "https://api.github.com/repos/OpenTermsArchive/contrib-versions/releases/latest" | jq '.assets[0].browser_download_url' | sed -E 's/.*"([^"]+)".*/\1/')
echo "updating" > latest_dataset.txt
echo "Downloaded $file_url"
curl -LJS $file_url -o dataset.zip
unzip -o dataset.zip && rm -rf dataset && mv dataset-* dataset
echo $file_url > latest_dataset.txt
