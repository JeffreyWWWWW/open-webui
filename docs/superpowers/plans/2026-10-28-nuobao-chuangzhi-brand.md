# 诺宝创智 LLM branding deployment

**Goal:** Apply the user-approved folded-N icon and brand name to nbllm.zeabur.app.

**Architecture:** Build the current frontend with the approved images and a new cache version. Reuse the exact currently deployed backend image, copying only the three backend files whose asset URL version changes. Keep normal full-image publishing available through the existing workflow.

**Tech Stack:** Svelte/Vite, Node/sharp for icon format packaging, existing Python branding checks, GitHub Actions/BuildKit, Zeabur.

## Constraints

- Running base is `ghcr.io/jeffreywwwww/open-webui:git-89aadda4972191e2bf4846a9c011c0a614d2f6da`.
- Keep this application version, database schema, dependencies, persistent volume, identity configuration and MCP connection.
- Brand display name: `诺宝创智 LLM`; short name: `诺宝创智`.
- Static asset version: `nuobao-20261028`.
- Existing uncommitted `package-lock.json` belongs to prior work and must not be staged or altered.
- The user approved the generated artwork and asked to continue applying it. Execute inline.

## Task 1: Package and verify brand resources

- [x] Run `.venv/Scripts/python.exe -m pytest backend/tests/test_nuobao_branding.py -q` on the unchanged base: 6 passed.
- [ ] Package approved PNG into current browser/PWA/splash PNG sizes and ICO sizes 16, 32, 48. Copy into `static/static`, backend static and the root favicon. Preserve alpha; copy the horizontal wordmark as `brand-logo-horizontal.png`.
- [ ] Update existing cache-version strings, `WEBUI_NAME` default, frontend default/title and manifest/OpenSearch display metadata. Adjust the existing branding checks to the new display values.
- [ ] Run the same six branding checks, verify all icon dimensions, ICO entries, mirror equality and alpha; run `git diff --check`.

## Task 2: Build an immutable deployment image

- [ ] Add `Dockerfile.branding`: reuse the normal frontend build stage; final stage is the exact running image, with newly built frontend and only `config.py`, `main.py`, `routers/models.py` copied. Set the display name with `ENV WEBUI_NAME="诺宝创智 LLM"`. No dependency installation or migrations are added to the final stage.
- [ ] Add optional boolean `branding_only` to the existing image workflow. Its default remains false; when true, use the branding Dockerfile. Retain `git-${github.sha}` immutable image tags.
- [ ] Commit only this task's files, push the branch, and dispatch the existing image workflow with `branding_only=true`. Inspect the build result and image tag.

## Task 3: Apply and verify production

- [ ] Record rollback image and verify persistent volume before updating the Zeabur Source image to the tested immutable tag.
- [ ] Wait for running/healthy status, inspect public health/version and brand metadata, compare served favicon bytes to packaged assets, and reload the UI.
- [ ] Save a browser screenshot showing the new icon/name; recheck that the teacher skill is still present. Record deployed revision and verification in this document.
