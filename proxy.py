import aiohttp
from multidict import CIMultiDict
from bs4 import BeautifulSoup
from src.html_processing import prepare_html, rewrite_url
from aiohttp import web, RequestInfo


async def process_text(request, remote_response, response_headers):
    response_headers.popone('Transfer-Encoding', '')
    response_headers.popone('Content-Encoding', '')
    text = await remote_response.text()
    processed_html = prepare_html(text)
    return web.Response(
        status=remote_response.status,
        text=processed_html,
        headers=response_headers,
    )


async def process_binary(request, remote_response, response_headers):
    response_headers.popone('Content-Encoding', '')
    response = aiohttp.web.StreamResponse(
        status=remote_response.status,
        headers=response_headers,
    )
    await response.prepare(request)
    try:
        while True:
            chunk = await remote_response.content.read(1024)
            if not chunk:
                break
            await response.write(chunk)
    except Exception as e:
        print(e.args)
    return response


async def handle(request):
    async with aiohttp.ClientSession() as session:
        new_url = rewrite_url(
            str(request.url),
            [
                {
                    'src_scheme': 'http',
                    'src_netloc': '127.0.0.1:8080',
                    'dst_scheme': 'https',
                    'dst_netloc': 'habr.com',
                },
            ],
        )
        request_headers = request.headers.copy()
        request_headers['Host'] = 'habr.com'
        async with session.get(new_url) as habr_resp:
            response_headers = habr_resp.headers.copy()
            content_type = response_headers.\
                getone('content-type', 'text/html').\
                split(';')[0]
            if content_type == 'text/html':
                return await process_text(
                    request, habr_resp, response_headers,
                )
            else:
                return await process_binary(
                    request, habr_resp, response_headers,
                )


app = web.Application()
app.add_routes([
    web.get(r'/{p:.*}', handle),
])

web.run_app(app)
