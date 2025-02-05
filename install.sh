#!/bin/bash

# Create a Python virtual environment with compatible Python version
python3.10 -m venv venv
# Activate the virtual environment
source venv/bin/activate

# Install other dependencies from requirements.txt
pip install -r requirements.txt

echo "Install deepspeed for Linux for python 3.10.x and CUDA 11.8"
python3.10 scripts/modeldownloader.py

echo "Install complete."