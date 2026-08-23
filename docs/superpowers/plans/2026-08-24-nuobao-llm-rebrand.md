# Nuobao LLM Rebrand Implementation Plan

> For agentic workers: REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Deliver a Nuobao LLM / NBLLM white-label build using the supplied logo without breaking deployment compatibility, then deploy the verified branch to the user-authorized Zeabur service.

**Architecture:** Keep framework packages, database migrations, Docker service names, provider names and legal attribution unchanged. Change product-facing defaults, bundled assets, and first-party external navigation. A deterministic Python/Pillow asset generator creates each icon and splash variant from the supplied source image; source-contract tests prevent upstream branding from returning.

**Tech Stack:** Python 3 + Pillow, FastAPI/Open WebUI backend, Svelte 5/Vite, JSON i18n resources, npm build/check, Git and Zeabur browser deployment.

## Global Constraints

- Default display name is exactly Nuobao LLM; compact brand is NBLLM / nbllm.
- Source logo is C:/Documents_Jeffrey/【机构】诺宝青年创客家俱乐部/【档案】机构运营资料/01_品牌资料/logo.png.
- Keep Ollama, OpenAI and other provider names unchanged.
- Do not rename package names, Docker image/service names, persisted database identifiers, migrations, or protocol compatibility identifiers.
- Keep LICENSE, LICENSE_NOTICE, contributor agreements and required third-party attributions unchanged.
- Do not retain Open WebUI-owned default favicon URLs, remote custom-brand API calls, community links, social links, release links or model links in the stock runtime.
- Deploy only after static checks and the local build pass, using the user-provided Zeabur service URL.

---

### Task 1: Set backend defaults and remove upstream branding fetches

**Files:**
- Modify: backend/open_webui/env.py, lines 891-895
- Modify: backend/open_webui/config.py, lines 181-214
- Modify: backend/open_webui/events.py
- Modify: backend/open_webui/tools/builtin.py
- Modify: backend/open_webui/routers/notifications.py
- Modify: backend/open_webui/utils/notifications.py
- Create: backend/tests/test_nuobao_branding.py

**Interfaces:**
- Consumes: WEBUI_NAME and WEBUI_FAVICON_URL environment-backed backend settings.
- Produces: default configuration, notifications and webhook activity cards named Nuobao LLM, with local /static/favicon.png.

- [ ] **Step 1: Write the failing source-contract test**

~~~python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_default_name_and_favicon_are_nuobao() -> None:
    env = (ROOT / 'backend/open_webui/env.py').read_text(encoding='utf-8')
    assert "WEBUI_NAME = os.getenv('WEBUI_NAME', 'Nuobao LLM')" in env
    assert "WEBUI_NAME += ' (Open WebUI)'" not in env
    assert "WEBUI_FAVICON_URL = '/static/favicon.png'" in env

def test_legacy_remote_custom_branding_is_removed() -> None:
    config = (ROOT / 'backend/open_webui/config.py').read_text(encoding='utf-8')
    assert 'api.openwebui.com/api/v1/custom' not in config
    assert 'CUSTOM_NAME = os.getenv' not in config
~~~

- [ ] **Step 2: Run the test to verify it fails**

Run: uv run pytest backend/tests/test_nuobao_branding.py -q

Expected: FAIL because defaults still contain Open WebUI and the legacy remote custom-brand API.

- [ ] **Step 3: Make the minimal backend changes**

~~~python
# backend/open_webui/env.py
WEBUI_NAME = os.getenv('WEBUI_NAME', 'Nuobao LLM')
WEBUI_FAVICON_URL = '/static/favicon.png'
~~~

Delete the full CUSTOM_NAME Legacy block in backend/open_webui/config.py, including outbound requests.get calls and assignments to WEBUI_NAME / WEBUI_FAVICON_URL. Replace only fallback user-visible product strings in the listed backend consumers with Nuobao LLM; preserve imports, package paths, provider names and header defaults.

- [ ] **Step 4: Run the test to verify it passes**

Run: uv run pytest backend/tests/test_nuobao_branding.py -q

Expected: PASS with 2 tests.

- [ ] **Step 5: Commit**

~~~powershell
git add backend/open_webui/env.py backend/open_webui/config.py backend/open_webui/events.py backend/open_webui/tools/builtin.py backend/open_webui/routers/notifications.py backend/open_webui/utils/notifications.py backend/tests/test_nuobao_branding.py
git commit -m "feat: set Nuobao LLM branding defaults"
~~~

### Task 2: Generate and install the supplied Nuobao brand assets

**Files:**
- Create: scripts/generate_nuobao_brand_assets.py
- Modify: static/manifest.json
- Modify: static/static/site.webmanifest
- Modify: static/static/favicon.svg
- Modify: src/app.html
- Replace: static/static/logo.png, favicon.png, favicon-96x96.png, favicon.ico, apple-touch-icon.png, web-app-manifest-192x192.png, web-app-manifest-512x512.png, splash.png, splash-dark.png
- Modify: backend/tests/test_nuobao_branding.py

**Interfaces:**
- Consumes: a square PNG passed as --source.
- Produces: browser, PWA and splash files at the existing /static URLs.

- [ ] **Step 1: Extend the failing test with image and PWA contracts**

~~~python
from PIL import Image

ASSET_DIR = ROOT / 'static/static'

def test_nuobao_icons_have_declared_sizes() -> None:
    assert Image.open(ASSET_DIR / 'web-app-manifest-192x192.png').size == (192, 192)
    assert Image.open(ASSET_DIR / 'web-app-manifest-512x512.png').size == (512, 512)
    assert Image.open(ASSET_DIR / 'favicon-96x96.png').size == (96, 96)

def test_manifest_declares_nuobao_brand() -> None:
    manifest = (ROOT / 'static/manifest.json').read_text(encoding='utf-8')
    assert 'Nuobao LLM' in manifest
    assert 'NBLLM' in manifest
~~~

- [ ] **Step 2: Run the test to verify it fails**

Run: uv run pytest backend/tests/test_nuobao_branding.py -q

Expected: FAIL because the manifest names Open WebUI/WebUI.

- [ ] **Step 3: Add the deterministic generator and create assets**

~~~python
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image

TARGETS = {
    'logo.png': 512, 'favicon.png': 512, 'favicon-96x96.png': 96,
    'apple-touch-icon.png': 180, 'web-app-manifest-192x192.png': 192,
    'web-app-manifest-512x512.png': 512, 'splash.png': 512, 'splash-dark.png': 512,
}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, default=Path('static/static'))
    args = parser.parse_args()

    image = Image.open(args.source).convert('RGBA')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, size in TARGETS.items():
        image.resize((size, size), Image.Resampling.LANCZOS).save(args.output_dir / name)
    image.save(args.output_dir / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])

if __name__ == '__main__':
    main()
~~~

Run:

~~~powershell
uv run python scripts/generate_nuobao_brand_assets.py --source 'C:/Documents_Jeffrey/【机构】诺宝青年创客家俱乐部/【档案】机构运营资料/01_品牌资料/logo.png'
~~~

Set each manifest name to Nuobao LLM, short_name to NBLLM, and both colors to #09298f. Replace favicon.svg with this local image reference:

~~~svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><image href="/static/favicon.png" width="512" height="512"/></svg>
~~~

Replace the literal document title in src/app.html with Nuobao LLM.

- [ ] **Step 4: Run asset tests and validate whitespace**

Run: uv run pytest backend/tests/test_nuobao_branding.py -q

Expected: PASS with 4 tests.

Run: git diff --check

Expected: no output.

- [ ] **Step 5: Commit**

~~~powershell
git add scripts/generate_nuobao_brand_assets.py static/manifest.json static/static src/app.html backend/tests/test_nuobao_branding.py
git commit -m "feat: add Nuobao LLM brand assets"
~~~

### Task 3: Replace product copy and upstream product-owned navigation

**Files:**
- Modify: src/lib/i18n/locales/all translation.json resources
- Modify: src/routes/+layout.svelte
- Modify: src/routes/(app)/workspace/tools/create/+page.svelte
- Modify: src/routes/(app)/workspace/tools/edit/+page.svelte
- Modify: src/routes/(app)/admin/functions/create/+page.svelte
- Modify: src/routes/(app)/admin/functions/edit/+page.svelte
- Modify: src/lib/components/chat/Settings/About.svelte
- Modify: src/lib/components/admin/Functions.svelte
- Modify: src/lib/components/admin/Evaluations/Feedbacks.svelte
- Modify: src/lib/components/chat/Placeholder.svelte
- Modify: src/lib/components/chat/ModelSelector/ModelItemMenu.svelte
- Modify: src/lib/components/chat/Messages/RateComment.svelte
- Modify: src/lib/components/workspace/common/CommunityDiscover.svelte
- Modify: static/opensearch.xml
- Modify: backend/tests/test_nuobao_branding.py

**Interfaces:**
- Consumes: dynamic WEBUI_NAME and existing i18n lookup keys.
- Produces: a UI showing Nuobao LLM and no default Open WebUI-owned outbound destination.

- [ ] **Step 1: Add a failing runtime-source scan**

~~~python
def test_runtime_sources_do_not_keep_product_upstream_branding() -> None:
    targets = [
        ROOT / 'src/app.html',
        ROOT / 'static/manifest.json',
        ROOT / 'static/static/site.webmanifest',
        ROOT / 'static/opensearch.xml',
        ROOT / 'src/lib/components/chat/Settings/About.svelte',
        ROOT / 'src/lib/components/admin/Functions.svelte',
        ROOT / 'src/lib/components/admin/Evaluations/Feedbacks.svelte',
        ROOT / 'src/lib/components/chat/Placeholder.svelte',
        ROOT / 'src/lib/components/chat/ModelSelector/ModelItemMenu.svelte',
        ROOT / 'src/lib/components/chat/Messages/RateComment.svelte',
    ]
    offenders = []
    for path in targets:
        text = path.read_text(encoding='utf-8', errors='ignore')
        if 'Open WebUI' in text or 'OpenWebUI' in text or 'openwebui.com' in text:
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []
~~~

- [ ] **Step 2: Run the scan to verify it fails**

Run: uv run pytest backend/tests/test_nuobao_branding.py::test_runtime_sources_do_not_keep_product_upstream_branding -q

Expected: FAIL and list current product-facing occurrences.

- [ ] **Step 3: Apply the exact copy and navigation policy**

Apply these literal substitutions only to UI text and translation values:

~~~text
Open WebUI -> Nuobao LLM
OpenWebUI -> NBLLM
openwebui -> nbllm
Open WebUI Community -> Nuobao LLM Community
~~~

Do not touch imports, package metadata, Docker files, OAuth/provider names, legal files or endpoint/header identifiers. Remove the About-page Discord/X/GitHub upstream community block. Replace the company/link line there with a plain Nuobao LLM label; retain independent Twemoji attribution. Remove UI clicks that navigate to openwebui.com for models, functions, ratings, feedback or community rather than inventing a Nuobao URL. Set OpenSearch labels to Nuobao LLM and Search Nuobao LLM.

- [ ] **Step 4: Parse translations and prove the scan passes**

Run: npm run i18n:parse

Expected: parser completes and translation JSON is formatted.

Run: uv run pytest backend/tests/test_nuobao_branding.py -q

Expected: PASS. Run a separate case-insensitive rg scan across src, static and backend/open_webui; replace every remaining product-facing match or retain it only where it is an explicit package, protocol, provider or legal compatibility identifier covered by the global constraints.

- [ ] **Step 5: Commit**

~~~powershell
git add src static/opensearch.xml backend/tests/test_nuobao_branding.py
git commit -m "feat: replace Nuobao LLM product copy"
~~~

### Task 4: Verify, push and deploy the branch

**Files:**
- Modify: docs/superpowers/plans/2026-08-24-nuobao-llm-rebrand.md (check completed items only)
- No application source changes expected.

**Interfaces:**
- Consumes: the tested backend defaults, static assets and UI copy from Tasks 1-3.
- Produces: a clean remote branch and a Zeabur deployment running that revision.

- [ ] **Step 1: Run the complete verification set**

~~~powershell
uv run pytest backend/tests/test_nuobao_branding.py -q
npm run check
npm run test:frontend
npm run build
git diff --check
git status --short
~~~

Expected: tests/check/build pass, git diff --check has no output, and status is clean after commits.

- [ ] **Step 2: Smoke-test the local UI**

Start the local application with its normal development command. Verify the tab title, login, splash, sidebar, About, favicon and PWA metadata show Nuobao LLM/NBLLM and the supplied blue logo. Verify Ollama remains labeled Ollama and no default click opens openwebui.com.

- [ ] **Step 3: Push the verified branch**

~~~powershell
git add docs/superpowers/plans/2026-08-24-nuobao-llm-rebrand.md
git commit -m "docs: record Nuobao LLM rebrand verification"
git push -u origin codex/rebrand-nuobao-llm
~~~

Expected: the Zeabur-connected remote can select codex/rebrand-nuobao-llm.

- [ ] **Step 4: Deploy via the authorized Zeabur service**

Confirm kimi-webbridge status reports running:true and extension_connected:true. Open the provided service URL in a dedicated browser session; confirm repository, environment and deployment branch. Select the pushed branch or preview revision and trigger deployment. Do not alter secrets or production environment values unless Zeabur requires a value the user supplies.

- [ ] **Step 5: Verify and hand off**

Wait for a successful Zeabur build/runtime status, then open the deployed URL. Confirm a successful response, page title Nuobao LLM, and new icon assets. Report the deployment URL and revision; close only the deployment browser session.
