#!/bin/bash

# Convenience script for data preparation
# Example usage:
# CUDA_VISIBLE_DEVICES=x ./prepare_data.sh user=alonso

set -e

# Collect all arguments to pass directly to the Python script
args=()

for arg in "$@"; do
    args+=("$arg")
done

# Run the Python script with the provided arguments
python ./prepare_data.py "${args[@]}"
