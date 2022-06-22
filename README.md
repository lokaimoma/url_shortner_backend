<h3 style='color: #5754FE'>Linksly</h3>
Linksly is a lite url shortening application. This is the backend part of the application built with Django. The frontend can be found [here.](https://github.com/lokaimoma/url-shotner-frontend)

![Test_Work_Flow](https://github.com/lokaimoma/url_shortner_backend/actions/workflows/test_runner.yml/badge.svg)

## Demo

Click on the image to watch a demo of the application
[![THe video image](https://github.com/lokaimoma/url-shotner-frontend/blob/main/images/thumb.png)](https://youtu.be/82kETKDubrU)

## Requirements

+ [Python 3.8 +](https://www.python.org/downloads/)
+ [Poetry 1.0.0 +](https://python-poetry.org/docs/#installation)

## Quickstart

+ Clone the project

```bash
git clone https://github.com/lokaimoma/url_shortner_backend
cd url_shortner_backend
```

+ Install app dependencies

```bash
poetry install --no-root
```

+ By default an sqlite database will be used. But if you want to
  use your own database you can set it up by using a `.env` in the
  root directory with the following keys and their correct values.

```bash
DATABASE_HOST=localhost
DATABASE_NAME=linksly
DATABASE_USER=wordpress
DATABASE_PASSWORD=password
```

+ If you choose to use a database other than sqlite, and you don't
  go with `MySQL` you will have to change the default database backend.
  [You can follow this link to know how to change the database backend to your preferred one.](https://docs.djangoproject.com/en/4.0/ref/databases/)
+ Run this command in the project root to create all the database tables

```bash
poetry run python3 manage.py migrate
```

+ Run the project with the command

```bash
poetry run python3 manage.py runserver
```

## WebRoutes

The runs by default on `localhost:8000`. To see all the available routes go
to `locahost:8000/api/` or check `urls.py` file.

## Tests

All tests are in the `tests` directory. To run the tests run the command

```bash
poetry run python3 manage.py test
```

## Technologies & Libraries Used

+ [Django](https://www.djangoproject.com/)
+ [Django Rest Framework](https://www.django-rest-framework.org/)
+ [Django Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
+ Etc...

## License

```
      
MIT License

Copyright (c) 2022 Owusu Kelvin Clark

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
