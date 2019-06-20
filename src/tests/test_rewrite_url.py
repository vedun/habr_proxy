from src.html_processing import rewrite_url, LINK_TRANSLATIONS


def test_rewrite_url():
    new_url = rewrite_url(
        'https://habr.com/aaaa/bbbb',
        LINK_TRANSLATIONS,
    )
    assert new_url == 'http://127.0.0.1:8080/aaaa/bbbb'
    #
    new_url = rewrite_url(
        'https://habr.com/aaaa/bbbb/?a=123',
        LINK_TRANSLATIONS,
    )
    assert new_url == 'http://127.0.0.1:8080/aaaa/bbbb/?a=123'
    #
    new_url = rewrite_url(
        'https://habr.com/aaaa/bbbb/?a=123#qwe',
        LINK_TRANSLATIONS,
    )
    assert new_url == 'http://127.0.0.1:8080/aaaa/bbbb/?a=123#qwe'
    #
    new_url = rewrite_url(
        'https://habr.com/aaaa/bbbb/#qwe',
        LINK_TRANSLATIONS,
    )
    assert new_url == 'http://127.0.0.1:8080/aaaa/bbbb/#qwe'
    #
    new_url = rewrite_url(
        'https://habr123.com',
        LINK_TRANSLATIONS,
    )
    assert new_url == 'https://habr123.com'
