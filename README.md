# watermark
Add watermark to *.epub files

# How to run

  1. Clone the repository using ssh:

```sh
$ git clone https://github.com/taysoh/watermark.git
$ cd watermark/
```
  2. Create new environment and install depends

```sh
$ virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

```
  3. Create database database.
```sh
$ python manage.py migrate
```
  4. Run project
```sh
$ python manage.py runserver
```
  - Open the project in browser on **http://127.0.0.1:8000/add_mark/?url=<url>&order_hash=<hash>**

  Replace **<url>** and **<hash>** with real data

