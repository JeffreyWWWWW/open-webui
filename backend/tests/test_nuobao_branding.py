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


def test_manifest_declares_nuobao_brand() -> None:
    manifest = (ROOT / 'static/manifest.json').read_text(encoding='utf-8')

    assert 'Nuobao LLM' in manifest
    assert 'NBLLM' in manifest
