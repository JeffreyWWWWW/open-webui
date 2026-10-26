from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT / 'static/static'


def test_default_name_and_favicon_are_nuobao_infinity() -> None:
    env = (ROOT / 'backend/open_webui/env.py').read_text(encoding='utf-8')

    assert "WEBUI_NAME = os.getenv('WEBUI_NAME', 'Nuobao Infinity')" in env
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
    version = 'v=nuobao-20261025'
    targets = [
        ROOT / 'src/app.html',
        ROOT / 'src/routes/+layout.svelte',
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


def test_manifest_declares_nuobao_infinity_brand() -> None:
    manifest = (ROOT / 'static/manifest.json').read_text(encoding='utf-8')
    backend_manifest = (ROOT / 'backend/open_webui/static/site.webmanifest').read_text(encoding='utf-8')

    assert 'Nuobao Infinity' in manifest
    assert '诺宝无限' in manifest
    assert 'Nuobao Infinity' in backend_manifest


def test_runtime_identity_preserves_brand_and_upstream_attribution() -> None:
    # Newer upstream includes license comments and copyright attribution.
    # Those are deliberately retained; the application identity stays Nuobao.
    constants = (ROOT / 'src/lib/constants.ts').read_text(encoding='utf-8')
    assert "export const APP_NAME = 'Nuobao Infinity'" in constants
    about = (ROOT / 'src/lib/components/chat/Settings/About.svelte').read_text(encoding='utf-8')
    assert '$WEBUI_NAME' in about
    assert 'Open WebUI Inc.' in about
    license_text = (ROOT / 'LICENSE').read_text(encoding='utf-8')
    assert 'Copyright (c) 2023- Open WebUI Inc.' in license_text
