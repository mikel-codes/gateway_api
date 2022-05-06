![ci/cd](https://github.com/mikel-codes/gateway_api/actions/workflows/ci.yml/badge.svg)    [![codecov](https://codecov.io/gh/mikel-codes/gateway_api/branch/main/graph/badge.svg)](https://codecov.io/gh/mikel-codes/gateway_api) ![License](https://img.shields.io/github/license/mikel-codes/gateway_api)


# gateway_api sample application

## Setup

The first thing to do is to clone the repository:
github repo -> https://github.com/mikel-codes/gateway_api/
```sh
$ git clone https://github.com/mikel-codes/gateway_api.git
$ cd gateway_api
```

##Optional
Create a virtual environment to install dependencies in and activate it:
You can google this if you need a virtualenv setup for this project
```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

# The examples below assume you decided to use the virtual env approach for django install
# you can still carry out the commands below without that
Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd gateway_api
(env)$ python manage.py runserver
```
### Set up a Django superuser
```sh
(env)$ cd gateway_api
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.



## Tests

To run the tests, `cd` into the directory where `manage.py` is:

#### with pytest recommended
cd into the gateway folder and run this command
```sh
(env)$ pytest
```
#### default approach | NOT recommended for this project
```sh
(env)$ python manage.py test
```
