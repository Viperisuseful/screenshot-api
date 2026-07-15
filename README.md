# ViperCapture

ViperCapture is an MIT-licensed webpage capture engine and browser interface.
It loads a public URL in Chromium, performs a bounded lazy-content scroll, and
returns a full-page PNG.

This public repository contains the capture API, website, launchers, and safety
controls. The hosted service's accounts, payment processing, subscription
entitlements, private API-key storage, and deployment configuration are not
part of this repository.

## Features

- Full-page PNG capture with headless Chromium
- Bounded scrolling for lazy-loaded pages
- Phone through 4K presets plus custom viewport sizes
- Configurable pixel density, wait time, and filenames
- CAPTCHA detection with an explicit capture-anyway decision
- Responsive light and dark interfaces
- Hosted-mode public-network validation and resource limits
- Local Windows launcher and cross-platform Python launcher

## Run locally

Requirements: Python 3.11 or newer.

On Windows, double-click `run.bat`. On any supported platform:

```bash
python launch.py
```

The launcher creates a virtual environment, installs dependencies and
Chromium when needed, starts the application, and opens
`http://127.0.0.1:8000`.

To install without opening the launcher:

```bash
bash install.sh
.venv/bin/python -m uvicorn main:app \
  --host 127.0.0.1 --port 8000 --workers 1 \
  --limit-concurrency 4 --no-access-log
```

## API

```http
GET /screenshot?url=https://www.wikipedia.org&width=1920&height=1080&device_scale_factor=2&wait=1
```

| Parameter | Default | Description |
| --- | --- | --- |
| `url` | required | Public page URL to capture |
| `width` | `1920` | Viewport width |
| `height` | `1080` | Viewport height |
| `device_scale_factor` | `2` | Pixel density from 1–4 |
| `wait` | `1` | Extra seconds after page load, from 0–15 |
| `proceed_on_captcha` | `false` | Capture a detected challenge as displayed |

A successful request returns `image/png`. The engine does not solve or bypass
CAPTCHAs.

## Hosted-mode safety

Set `SHOT_HOSTED=1` only behind a rate-limited reverse proxy. Hosted mode
disables server-side file saving and desktop folder opening, and rejects
private-network targets. Keep an OS or network egress rule blocking private
ranges and cloud metadata endpoints as the final SSRF boundary.

Useful limits:

```bash
SHOT_HOSTED=1
SHOT_MAX_CONCURRENCY=1
SHOT_MAX_PIXELS=50000000
```

Run one Uvicorn worker because each worker owns a Chromium process tree. Apply
container or systemd memory/task limits and measure before increasing browser
concurrency.

Machine-only overrides can live in `.env.local`, which is ignored by Git.
Never commit credentials.

## Structure

```text
screenshot-api/
├── main.py              # FastAPI routes and capture engine
├── launch.py            # Local environment and browser launcher
├── run.bat              # Windows entry point
├── requirements.txt
├── templates/index.html # Browser interface
├── static/              # Styles, JavaScript, and media
└── test_main.py
```

## Stack

- FastAPI and Uvicorn
- Playwright with headless Chromium
- Vanilla HTML, CSS, and JavaScript

## License

[MIT](LICENSE)
