#!/bin/bash

# Number of files to create
num_files=10

# Base name for the files
base_name="file"

# Loop to create files
for i in $(seq 1 $num_files); do
  touch "${base_name}${i}.txt"
done

echo "$num_files files created with base name $base_name"

