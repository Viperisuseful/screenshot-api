# Contributing to ViperCapture

Thank you for your interest in contributing to ViperCapture.

ViperCapture is an open-source webpage capture engine built with Python, FastAPI, Playwright, and Chromium. Contributions that improve reliability, security, documentation, compatibility, or the capture experience are welcome.

## Ways to Contribute

You can contribute by:

* Fixing bugs
* Improving capture reliability
* Improving documentation
* Adding validation or error handling
* Improving the browser interface
* Improving platform compatibility
* Adding tests
* Reviewing pull requests
* Reporting reproducible issues

Before starting a large feature or architectural change, open an issue to discuss it with the maintainer. This helps avoid work on changes that may not fit the project’s scope.

## Project Scope

This public repository contains:

* The URL-to-image rendering engine
* The `/v1/render` API
* The local browser interface
* PNG, JPEG, and WebP rendering
* Full-page, viewport, and element captures
* Wait conditions and rendering options
* Self-hosting documentation

The following hosted-service components are maintained separately and are not part of this repository:

* User accounts and authentication
* Billing and subscriptions
* Credits and referrals
* Hosted deployment configuration
* Document or PDF rendering
* Private infrastructure and secrets

Pull requests should remain within the scope of the public engine unless the maintainer has approved the change beforehand.

## Reporting Bugs

Before opening a bug report:

1. Search existing issues to avoid duplicates.
2. Confirm the problem occurs on the latest `master` branch.
3. Verify that Python and Playwright Chromium are installed correctly.
4. Reduce the problem to the smallest reproducible example.

A useful bug report should include:

* Your operating system
* Your Python version
* The latest commit or branch used
* Whether you used `launch.py` or a manual installation
* The request payload or interface options used
* The expected behavior
* The actual behavior
* Relevant logs or error responses
* Reproduction steps

Remove API keys, cookies, authorization headers, private URLs, and other sensitive information before posting logs.

## Reporting Security Vulnerabilities

Do not report security vulnerabilities through public issues, discussions, or pull requests.

Follow the private reporting instructions in [`SECURITY.md`](SECURITY.md).

## Development Setup

### Requirements

You need:

* Python 3.11 or newer
* Git
* A supported operating system for Playwright Chromium

### Fork and Clone

Fork the repository on GitHub, then clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/ViperCapture.git
cd ViperCapture
```

Add the original repository as an upstream remote:

```bash
git remote add upstream https://github.com/Viperisuseful/ViperCapture.git
```

### Create a Branch

Update your local `master` branch:

```bash
git checkout master
git pull upstream master
```

Create a focused branch for your change:

```bash
git checkout -b fix/short-description
```

Suggested branch prefixes include:

* `fix/` for bug fixes
* `feat/` for new features
* `docs/` for documentation
* `refactor/` for internal improvements
* `test/` for tests
* `chore/` for maintenance work

### Automatic Setup

The simplest way to start ViperCapture is:

```bash
python launch.py
```

The launcher will:

* Create a `.venv` virtual environment
* Install Python dependencies
* Install Playwright Chromium
* Start the FastAPI application
* Open the local interface

The application should become available at:

```text
http://127.0.0.1:8000
```

### Manual Setup

On Linux or macOS:

```bash
bash install.sh
```

Then start the server:

```bash
.venv/bin/python -m uvicorn main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --workers 1 \
  --limit-concurrency 4 \
  --no-access-log
```

On Windows, you may run:

```powershell
python launch.py
```

or double-click `run.bat`.

## Project Structure

The main files and directories are:

| Path                 | Purpose                                                |
| -------------------- | ------------------------------------------------------ |
| `main.py`            | FastAPI application, browser lifecycle, and API routes |
| `render_contract.py` | Request models, limits, and input validation           |
| `render_engine.py`   | Playwright rendering and image generation              |
| `render_errors.py`   | Stable API errors and error responses                  |
| `launch.py`          | Local environment setup and application launcher       |
| `templates/`         | Browser interface HTML                                 |
| `static/`            | Styles, scripts, icons, and other frontend assets      |
| `docs/`              | Project documentation                                  |
| `requirements.txt`   | Python runtime dependencies                            |

## Coding Guidelines

### Python

Follow the style already used by the project:

* Use clear and descriptive names.
* Add type hints to new functions where practical.
* Keep functions focused on one responsibility.
* Prefer explicit validation over silent fallback behavior.
* Preserve asynchronous behavior in rendering and browser code.
* Avoid blocking calls inside asynchronous request handlers.
* Keep imports organized and remove unused imports.
* Do not add dependencies unless they provide a clear benefit.

Request validation belongs in `render_contract.py` rather than being scattered throughout the rendering engine.

Errors returned by the API should use the existing structured error system in `render_errors.py`. Avoid introducing endpoints that return unrelated or inconsistent error formats.

### API Compatibility

Changes to `/v1/render` should preserve compatibility whenever possible.

When changing the request or response contract:

* Document the change in `README.md`.
* Update request validation.
* Include valid and invalid request examples.
* Preserve existing defaults unless there is a strong reason to change them.
* Consider how existing API clients will be affected.

Breaking API changes require prior discussion with the maintainer.

### Frontend

When changing files in `templates/` or `static/`:

* Test the interface at common desktop and mobile widths.
* Keep the interface usable without unnecessary dependencies.
* Preserve keyboard accessibility.
* Provide visible labels for interactive controls.
* Confirm that frontend options match the API contract.
* Do not place secrets or private configuration in browser-facing code.

### Security Boundaries

ViperCapture processes user-provided URLs through a browser, so security-sensitive changes require additional care.

Contributions must not:

* Add CAPTCHA solving or CAPTCHA bypass functionality
* Send user-provided headers to unrelated origins
* Disable URL validation without an equivalent safeguard
* Expose local files, environment variables, or credentials
* Add credentials or secrets to the repository
* Weaken protections against private-network or cloud-metadata access
* Silently remove resource limits
* Treat browser automation as a trusted execution environment

Self-hosted production deployments must retain a final network-level egress boundary that blocks private address ranges and cloud metadata endpoints.

## Testing Changes

The project does not currently define a complete automated test suite. Until one is added, every pull request must include appropriate manual verification.

### Python Syntax Check

Run:

```bash
python -m py_compile \
  main.py \
  render_contract.py \
  render_engine.py \
  render_errors.py \
  launch.py
```

On PowerShell, run the command on one line:

```powershell
python -m py_compile main.py render_contract.py render_engine.py render_errors.py launch.py
```

### Basic API Smoke Test

Start the application, then run:

```bash
curl "http://127.0.0.1:8000/v1/render" \
  --header "Content-Type: application/json" \
  --data '{
    "url": "https://example.com",
    "output": "png",
    "full_page": true
  }' \
  --output example.png
```

Confirm that:

* The response is successful.
* The output file opens correctly.
* The returned media type matches the requested format.
* The server remains available after the request.

### Relevant Capture Checks

Depending on your change, test the applicable modes:

* PNG output
* JPEG output
* WebP output
* Full-page capture
* Viewport capture
* CSS selector capture
* Transparent background
* Image quality
* Custom viewport sizes
* Wait events
* Selector waiting
* Text waiting
* Fixed delays
* Same-origin request headers
* Invalid payload handling
* Timeout behavior
* CAPTCHA detection behavior

Do not test against websites where you do not have permission to perform repeated or automated requests.

### Validation Checks

Changes to request validation should test both accepted and rejected values.

Verify that invalid requests return a structured JSON error rather than an unhandled exception or server crash.

### Documentation Checks

For documentation changes:

* Confirm commands can be copied and run.
* Confirm relative links work from GitHub.
* Confirm documented fields match the current API contract.
* Avoid documenting private hosted-service behavior as part of the public engine.

## Commits

Write clear commit messages describing what changed.

Examples:

```text
fix: prevent selector capture with full-page mode
feat: add configurable navigation timeout
docs: clarify hosted network boundaries
refactor: separate browser recovery logic
test: add render contract validation tests
```

Keep commits focused. Avoid mixing unrelated formatting, refactoring, documentation, and behavior changes into one commit.

Do not commit:

* `.venv/`
* Captured images created during testing
* `.env.local`
* API keys or credentials
* Browser profiles
* Local logs
* Editor-specific files not needed by the project
* Large generated files

## Pull Requests

Before submitting a pull request:

1. Rebase or update your branch against the latest `master`.
2. Review your own diff.
3. Remove debugging code and unrelated changes.
4. Run the relevant checks.
5. Update documentation when behavior changes.
6. Confirm that no private information is included.

A pull request description should explain:

* What problem the change solves
* How the implementation works
* How the change was tested
* Any compatibility or security considerations
* Any remaining limitations

Keep each pull request focused on one issue or closely related group of changes.

For visual changes, include screenshots when practical. Do not include screenshots containing private data, tokens, or authenticated pages.

## AI-Assisted Contributions

AI-assisted contributions are welcome, but the contributor remains responsible for the submitted code.

Before submitting AI-generated or AI-modified code:

* Read and understand the changes.
* Confirm that referenced functions and files actually exist.
* Remove unnecessary abstractions and dependencies.
* Test the behavior locally.
* Check for security regressions.
* Ensure the pull request accurately describes the implementation.

Large unreviewed code dumps may be closed without detailed review.

## Review Process

Maintainers may request changes related to:

* Correctness
* Security
* API compatibility
* Performance
* Resource usage
* Documentation
* Scope
* Code clarity

Submitting a pull request does not guarantee that it will be merged. A contribution may be declined when it conflicts with the project’s direction, duplicates existing functionality, introduces excessive maintenance cost, or belongs to the private hosted-service layer.

## License

By contributing to ViperCapture, you agree that your contributions will be licensed under the repository’s [MIT License](LICENSE).
