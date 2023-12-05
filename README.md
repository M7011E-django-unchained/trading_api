# trading_api
An API for trading and buying products from one another. Assignment for course M7011E on LTU.


## Get started with the project dev environment
### Prerequisites
- python 3.x.x
- pyenv (optional)
- Django (if not running with pyenv)

### Cloning the repo
Create a folder, for example `M7011E`, then enter it and run:
```bash
git init
git clone https://github.com/M7011E-django-unchained/trading_api
```
in the terminal.

The project is now cloned but if you want to have a unique development environment for the project (which is recommended) you need to setup an environment using pyenv.

### Setting up pyenv (optional)
Make sure you have `pyenv` installed before starting this steps. This creates the unique environment for the project and starts it. This can be checked with:
```cmd
pyenv --version
```

If you have `pyenv` installed correctly then you will have to choose your python version for the project environment, anything in the later stages of python3 should work. To check for the available python releases run:
```cmd
pyenv install -l
```

Then, install one of choice (preferable the latest stable version). For example:
```cmd
pyenv install 3.12.0
```

**For windows users:** Enter the project root folder `trading_api` and run:
```cmd
pyenv local 3.12.0 #Same as one you've installed earlier
python -m venv .env
.env\Scripts\activate.bat
```

_Not tested!!_ **For linux/unix users** Enter the project root folder `trading_api` and run:
```bash
python -m venv .env
source .virtenv/bin/activate
```

#### Install required packages on environment (if not on env, packages needs to be installed globally)
Just run:
```cmd
pip install -r requirements.txt
```

in the project root folder and check that the installation was correct with:
```cmd
pip freeze
```

which should return something like:
```cmd
asgiref==3.7.2
Django==4.2.7
sqlparse==0.4.4
tzdata==2023.3
```

### Run the project in dev mode
Run the Django-server from the project root-folder in a terminal with:
```cmd
python manage.py runserver
```
