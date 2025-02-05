#!/bin/bash

source venv/bin/activate

python3.10 scripts/modeldownloader.py
python3.10 app.py --deepspeed --rvc

echo "Launch"