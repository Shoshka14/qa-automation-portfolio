# QA Automation Portfolio

![tests](https://github.com/YOUR-USERNAME/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg)

Automated UI and API tests in Python, run in CI with GitHub Actions.

## What's inside

| Area | Tools | Target |
|------|-------|--------|
| UI tests | Playwright, pytest, page objects | [Sauce Demo](https://www.saucedemo.com) (public practice shop) |
| API tests | requests, pytest fixtures | [Restful Booker](https://restful-booker.herokuapp.com) (public practice API) |
| CI | GitHub Actions | runs on every push and weekly |

## Test design

- **Page objects** keep locators out of the tests, so a UI change means one edit.
- **Accessible locators** (role, placeholder) mirror how a user finds elements.
- **Independent tests:** each API test creates its own data and deletes it afterwards.
- **Negative tests:** invalid logins, missing auth, deleted resources.
- **Traces on failure:** Playwright traces are uploaded as CI artifacts for debugging.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
pytest --browser chromium
```

## Roadmap

- [ ] Cart and checkout UI tests
- [ ] Cross-browser runs (Firefox, WebKit)
- [ ] API schema validation
- [ ] Serverless test runner on AWS Lambda
