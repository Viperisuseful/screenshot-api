# Self-hosting ViperCapture

The public ViperCapture repository contains the MIT-licensed URL-to-image engine and browser interface only. Hosted accounts, billing, credits, referrals, document/PDF rendering, managed cleanup, deployment configuration, and secrets are deliberately excluded.

## Local install

Use Python 3.11 or newer, then run `python launch.py`. This is the supported
setup and startup method. The launcher creates a virtual environment, installs
Playwright Chromium, starts the application, and opens the local interface.

## Production boundaries

- Put hosted mode behind a rate-limited reverse proxy.
- Run one application process; every process owns a Chromium process tree.
- Keep `VIPERCAPTURE_MAX_CONCURRENCY=1` until memory and swap pressure are measured.
- Apply container or systemd memory, PID, and CPU limits.
- Enforce network egress rules that block private ranges and cloud metadata endpoints.
- Do not place credentials in the repository or browser-facing JavaScript.

## Capability boundary

The public engine supports a public URL source, PNG/JPEG/WebP output, viewport/full-page/selector capture, image quality, transparency, wait conditions, and same-origin target headers. It blocks detected page-level challenges by default. Callers may set `proceed_on_captcha: true` to capture the visible challenge as displayed; ViperCapture never solves or bypasses CAPTCHAs.
