import re
from typing import List, Dict
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4.element import NavigableString


SIX_CHARACTER_WORD = re.compile(r'\b[\S]{6}\b')

TAGS_WITH_LINKS = {
    'a': 'href',
    'use': 'xlink:href',
}

TAGS_PROTECTED_FROM_SUBSTITUTION = ['script', 'style']

LINK_TRANSLATIONS = [
    {
        'src_scheme': 'https',
        'src_netloc': 'habr.com',
        'dst_scheme': 'http',
        'dst_netloc': '127.0.0.1:8080',
    },
]

TM_SYMBOL = '™'


def prepare_html(
    text: str,
    link_translations: List[Dict[str, str]]=LINK_TRANSLATIONS,
    tags_with_links: Dict[str, str]=TAGS_WITH_LINKS,
    tags_protected_from_substitution: List[str]=TAGS_PROTECTED_FROM_SUBSTITUTION  # noqa
)-> str:
    '''
    convert links according with LINK_TRANSLATIONS and
    append '™' symbol to six length words
    '''
    soup = BeautifulSoup(text, 'html.parser')
    for tag, attr in tags_with_links.items():
        page_tags = soup.find_all(tag)
        for page_tag in page_tags:
            attr_value = page_tag.get(attr)
            if attr_value is not None:
                new_url = rewrite_url(attr_value, link_translations)
                page_tag[attr] = new_url
    body_tags = soup.find_all('body')
    if len(body_tags) > 0:
        body = body_tags[0]
        text_nodes = []
        for tag in body.descendants:
            if isinstance(tag, NavigableString) and tag.parent.name not in tags_protected_from_substitution:  # noqa
                text_nodes.append(tag)
        for text_node in text_nodes:
            text_node.replace_with(convert_six_length_words(str(text_node)))
    return str(soup)


def rewrite_url(
    url: str,
    link_translations: List[Dict[str, str]],
) -> str:
    o = urlparse(url)
    scheme = o.scheme
    netloc = o.netloc
    for link in link_translations:
        if o.scheme == link['src_scheme'] and o.netloc == link['src_netloc']:
            scheme = link['dst_scheme']
            netloc = link['dst_netloc']
            break
    path = o.path
    params = o.params
    if o.query == '':
        query = ''
    else:
        query = '?{}'.format(o.query)
    if o.fragment == '':
        fragment = ''
    else:
        fragment = '#{}'.format(o.fragment)
    return '{scheme}://{netloc}{path}{params}{query}{fragment}'.format(
        scheme=scheme, netloc=netloc, path=path, params=params,
        query=query, fragment=fragment,
    )


def convert_six_length_words(text: str) -> str:
    word_list = text.split(' ')
    for idx, word in enumerate(word_list):
        if len(word) == 6 and SIX_CHARACTER_WORD.match(word):
            word_list[idx] = '{word}{symbol}'.format(
                word=word, symbol=TM_SYMBOL,
            )
    return ' '.join(word_list)
