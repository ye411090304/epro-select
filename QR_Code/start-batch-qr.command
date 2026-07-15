#!/bin/bash
set -e

cd "$(dirname "$0")"

python3 image_qr_generator.py --serve
