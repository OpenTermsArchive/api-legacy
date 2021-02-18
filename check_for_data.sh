#!/bin/bash
file_url=$(curl --silent "https://api.github.com/repos/ambanum/CGUs-versions/releases/latest" | grep '"browser_download_url":' | sed -E 's/.*"([^"]+)".*/\1/');

if [ $file_url != $MOST_RECENT_DATASET ]
then
    source download_dataset.sh;
else
    :
fi