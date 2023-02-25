# IMG2PDF
[![gif with examples][examples-link]][examples-link]
# Installation

## Env

(*REQUIRED*)

- SECRET_KEY
- DEBUG

## Docker Image
```
docker pull gexilable/img2pdf
```
## Docker Local
```bash
docker build -t img2pdf .
docker run --rm -p 8000:8000 -e SECRET_KEY=7 -e DEBUG=1 img2pdf 
```


## Local

```bash
git clone https://github.com/Gexilable/IMG2PDF
python3 -m venv venv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
[examples-link]:   ./example.gif