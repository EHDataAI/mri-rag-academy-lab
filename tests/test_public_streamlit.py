"""Public educational interface integration tests (no external model)."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def test_public_app_bootstrap():
    app = AppTest.from_file(ROOT / "streamlit_public.py", default_timeout=40).run()
    assert not app.exception
    assert not app.error
    assert len(app.text_input) == len(app.button) == 1
    assert len(app.selectbox) == 0


def test_public_app_academic_question():
    app = AppTest.from_file(ROOT / "streamlit_public.py", default_timeout=40).run()
    app.text_input[0].input("¿Qué diferencia existe entre DWI y ADC?")
    app.button[0].click()
    app.run(timeout=40)
    assert not app.exception
    assert not app.error
    headers = {item.value for item in app.subheader}
    assert {"Respuesta documental", "Referencias"} <= headers
