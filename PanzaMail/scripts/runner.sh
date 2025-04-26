#!/bin/bash

# Convenience script for launching your fine-tuned model.
# Example usage:
# CUDA_VISIBLE_DEVICES=x ./runner.sh user=USERNAME interfaces=cli writer/llm=transformers

set -e

# Collect all arguments
args=()

for arg in "$@"; do
    args+=("$arg")
done

# Run the Python script with the arguments
python3 runner.py "${args[@]}"
