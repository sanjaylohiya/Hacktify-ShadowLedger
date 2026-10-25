# ShadowLedger — Web Exploitation Lab

## Overview
ShadowLedger is an intentionally vulnerable Flask-based internal asset management portal designed for cybersecurity training.

The challenge demonstrates a two-stage broken access control chain. An authenticated analyst can submit privileged reviewer identities through untrusted form fields to approve a deployment and subsequently release a restricted backup archive.

## Requirements
- Ubuntu 24.04 LTS
- Python 3 and internet access for initial dependency installation
- Port 5002 available

## Installation
Open a terminal inside the extracted `hacktify-project` directory and run:

```bash
bash setup.sh
```

## Start the Application
Run:

```bash
bash START-SHADOWLEDGER.sh
```

Open Firefox in the Ubuntu VM and visit:

http://127.0.0.1:5002/

Alternatively, start Flask manually:

```bash
.venv/bin/python -m flask --app app run --host 127.0.0.1 --port 5002
```

Keep the terminal running while using the lab.

## Lab Credentials
- Username: `analyst`
- Password: `ShadowLab-2026`

## Challenge Objective
Starting with the analyst account, identify the broken authorization checks in the deployment review and backup approval workflows. Complete the connected stages to release the restricted archive and capture the flag.

## Reset
While the application is running, open a second terminal in the project directory:

```bash
bash reset.sh
```

## Health Check
Visit:

http://127.0.0.1:5002/health

## Notes
- This is a local, intentionally vulnerable training environment. Do not expose it to the public internet.
- The application was tested on Ubuntu 24.04 LTS.
- The technical writeup and walkthrough video are provided separately in the submission package.
