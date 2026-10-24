#!/usr/bin/env bash
# Setup di Debian 12: bash setup.sh
set -e
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install psutil matplotlib
echo "Selesai. Aktifkan dengan: source .venv/bin/activate"
