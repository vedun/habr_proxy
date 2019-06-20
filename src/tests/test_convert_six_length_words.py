import re
from src.html_processing import convert_six_length_words, TM_SYMBOL


def test_convert_six_length_words():
    res = convert_six_length_words('111 123456 12345. 123456. ')
    assert res == '111 123456{} 12345. 123456. '.format(
        TM_SYMBOL,
    )
