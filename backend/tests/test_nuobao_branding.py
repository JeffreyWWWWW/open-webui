from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT / 'static/static'


def test_default_name_and_favicon_are_nuobao() -> None:
    env = (ROOT / 'backend/open_webui/env.py').read_text(encoding='utf-8')

    assert "WEBUI_NAME = os.getenv('WEBUI_NAME', 'Nuobao LLM')" in env
    assert "WEBUI_NAME += ' (Open WebUI)'" not in env
    assert "WEBUI_FAVICON_URL = '/static/favicon.png'" in env


def test_legacy_remote_custom_branding_is_removed() -> None:
    config = (ROOT / 'backend/open_webui/config.py').read_text(encoding='utf-8')

    assert 'api.openwebui.com/api/v1/custom' not in config
    assert 'CUSTOM_NAME = os.getenv' not in config


def test_nuobao_icons_have_declared_sizes() -> None:
    assert Image.open(ASSET_DIR / 'web-app-manifest-192x192.png').size == (192, 192)
    assert Image.open(ASSET_DIR / 'web-app-manifest-512x512.png').size == (512, 512)
    assert Image.open(ASSET_DIR / 'favicon-96x96.png').size == (96, 96)


def test_visible_brand_assets_are_cache_versioned() -> None:
    """Old Open WebUI icons must not survive in browsers' static-asset cache."""
    version = 'v=nuobao-20260825'
    targets = [
        ROOT / 'src/app.html',
        ROOT / 'src/lib/components/layout/Sidebar.svelte',
        ROOT / 'src/lib/components/app/AppSidebar.svelte',
        ROOT / 'backend/open_webui/routers/models.py',
        ROOT / 'backend/open_webui/config.py',
        ROOT / 'backend/open_webui/main.py',
        ROOT / 'static/static/favicon.svg',
        ROOT / 'static/manifest.json',
        ROOT / 'static/static/site.webmanifest',
        ROOT / 'backend/open_webui/static/site.webmanifest',
    ]

    for path in targets:
        assert version in path.read_text(encoding='utf-8'), path.relative_to(ROOT)


def test_manifest_declares_nuobao_brand() -> None:
    manifest = (ROOT / 'static/manifest.json').read_text(encoding='utf-8')
    backend_manifest = (ROOT / 'backend/open_webui/static/site.webmanifest').read_text(encoding='utf-8')

    assert 'Nuobao LLM' in manifest
    assert 'NBLLM' in manifest
    assert 'Nuobao LLM' in backend_manifest


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
        ROOT / 'src/lib/components/workspace/Tools.svelte',
        ROOT / 'src/lib/components/workspace/Tools/ToolMenu.svelte',
        ROOT / 'src/lib/components/workspace/Prompts.svelte',
        ROOT / 'src/lib/components/workspace/Prompts/PromptMenu.svelte',
        ROOT / 'src/lib/components/workspace/Models.svelte',
        ROOT / 'src/lib/components/workspace/Models/ModelMenu.svelte',
        ROOT / 'src/lib/components/chat/ShareChatModal.svelte',
    ]
    offenders = []

    for path in targets:
        text = path.read_text(encoding='utf-8', errors='ignore')
        if 'Open WebUI' in text or 'OpenWebUI' in text or 'openwebui.com' in text:
            offenders.append(str(path.relative_to(ROOT)))

    assert offenders == []
