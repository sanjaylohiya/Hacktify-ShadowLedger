
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "[+] Installing ShadowLedger dependencies..."

sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install "Flask==3.1.1"

echo "[+] Installation complete."
echo "[+] Start the lab with:"
echo "    .venv/bin/python -m flask --app app run --host 0.0.0.0 --port 5002"
