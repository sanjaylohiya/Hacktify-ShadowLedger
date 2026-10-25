#!/usr/bin/env bash
set -euo pipefail

echo "[+] Resetting ShadowLedger..."

curl --fail --silent --show-error \
  --request POST \
  http://127.0.0.1:5002/admin/reset-lab

echo
echo "[+] Reset complete."