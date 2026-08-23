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
