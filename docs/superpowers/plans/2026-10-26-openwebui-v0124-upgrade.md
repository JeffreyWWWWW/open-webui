# Nuobao Infinity v0.12.4 Upgrade Implementation Plan

> **For agentic workers:** Execute inline with the executing-plans workflow; do not delegate this live production change.

**Goal:** Upgrade nbllm.zeabur.app from v0.11.0 to stable v0.12.4 while retaining the Nuobao identity, models, OJ MCP and persisted user data.

**Architecture:** Merge the pinned upstream release in an isolated checkout. Keep deployment pinned to a commit-tagged GHCR image, back up the live database before migration, then replace the Zeabur image and verify the live instance.

**Tech Stack:** Svelte, Python, SQLite, Docker, GitHub Actions, Zeabur.

## Global Constraints

- Preserve the primary checkout's uncommitted package-lock.json.
- Keep the current image-2 icon; icon redesign is cancelled.
- Preserve the four approved OJ readers and the revoked student state.
- Never print or commit credentials, exported databases or runtime secrets.
- Retain the old image tag and database backup for rollback.

### Task 1: Prepare release and validate branding

- [ ] Install pytest/Pillow in this checkout's local virtual environment and run `python -m pytest backend/tests/test_nuobao_branding.py -q` (six tests must pass on the existing baseline).
- [ ] Merge upstream `v0.12.4` with upstream conflict preference, then restore the intentional Nuobao display identity and cache-versioned assets while keeping upstream behavior changes.
- [ ] Run the six branding checks, Python syntax checks and `git diff --check`; inspect every unresolved conflict.

### Task 2: Build and preserve rollback

- [ ] Make the existing nuobao-image workflow runnable on this upgrade branch, commit only upgrade files, push to the Nuobao fork and dispatch the image build.
- [ ] Download and verify an authenticated live database backup through the admin UI, store outside Git, and retain the old deployment image reference.
- [ ] Wait for the container build to succeed and record the immutable new image tag.

### Task 3: Deploy and verify

- [ ] Replace the Zeabur image tag with the verified immutable build tag, preserving the persistent volume and environment.
- [ ] Confirm live version v0.12.4, administrator access, 10 user accounts, teacher membership and OJ teacher-only connection access.
- [ ] Verify DeepSeek default, Claude adapter/model list, Chinese suggestions, and one minimal model reply plus OJ tool health.
- [ ] On a failed migration/start, restore the old image with the matching database backup before further traffic.
