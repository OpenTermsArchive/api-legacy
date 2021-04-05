#!/bin/bash
echo "Checking for data"

echo "Copying all environment variables"
for variable_value in $(cat /proc/1/environ | sed 's/\x00/\n/g'); do
  export $variable_value
done

curl -X "GET" \
  "http://localhost$BASE_PATH/check_for_dataset" \
  -H "accept: application/json"
