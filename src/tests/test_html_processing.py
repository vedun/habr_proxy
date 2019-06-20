import pytest
from src.html_processing import prepare_html, TM_SYMBOL


def test_html_not_processed():
    text = '<html><head><title>Test56</title></head></html>'
    result = prepare_html(text)
    assert result == text


def test_html_with_single_tag():
    result = prepare_html('<html><body><br d="12"/></body></html>')
    assert result == '<html><body><br d="12"/></body></html>'


def test_html_processed():
    result = prepare_html('<html><body>123456</body></html>')
    assert result == '<html><body>123456{symbol}</body></html>'.format(
        symbol=TM_SYMBOL,
    )


def test_links_converting():
    result = prepare_html('<html><body><a href="https://habr.com/123">123</a></body></html>')  # noqa
    assert result == '<html><body><a href="http://127.0.0.1:8080/123">123</a></body></html>'  # noqa


def test_use_converting():
    result = prepare_html('<html><body><use xlink:href="https://habr.com/images/1560786911/common-svg-sprite.svg#globus"/></body></html>')  # noqa
    assert result == '<html><body><use xlink:href="http://127.0.0.1:8080/images/1560786911/common-svg-sprite.svg#globus"></use></body></html>'  # noqa
