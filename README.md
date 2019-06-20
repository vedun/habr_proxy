Habr proxy server
=================

Requirements for runing localy: `python 3.5+`.


Runing localy
-------------

Clone repository and run next commands in the project root directory:

* `python -m venv ve`
* `source ve/bin/activate`
* `pip install -r ./requirements.txt`
* `python proxy.py`
* open `http://127.0.0.1:8080` url in web browser

For runing tests exec next command in the project
root directory (inside venv shell): `python -m pytest ./src/tests`.


Runing in Docker
----------------

Clone repository and run next commands in the project root directory:

* `docker image build --no-cache -t "habr_proxy:latest" .` - building image
* `docker container run --name habr -p 8080:8080 -d habr_proxy:latest` - runing container
* open `http://127.0.0.1:8080` url in web browser
