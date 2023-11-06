# trading_api
An API for trading and buying products from one another. Assignment for course M7011E on LTU.


## Get started with the project dev environment
### Prerequisites
- python 3.x.x
- pyenv (optional)
- Django (if not running with pyenv)

### Cloning the repo
Create a folder, for example `M7011E-project`, then enter it and run:
```bash
git init
git clone https://github.com/casperlundberg/trading_api.git
```
in the terminal.

The project is now cloned but if you want to have a unique development environment for the project (which is recommended) you need to setup an environment using pyenv.

### Setting up pyenv (optional)
Make sure you have `pyenv` installed before starting this steps. This creates the unique environment for the project and starts it. This can be checked with:
```cmd
pyenv --version
```

If you have `pyenv` installed correctly then you will have to choose your python version for the project environment, anything in the later stages of python3 should work. To check for the available python releases run:
`pyenv install -l`
Then, install one of choice (one of the stable ones), for example:
`pyenv install 3.12.0`

Enter the project root folder `trading_api` and run:
```cmd
pyenv local 3.12.0 #Same as one you've installed earlier
python -m venv .env
.env\Scripts\activate.bat
```
in the terminal for windows users.

For linux/unix users run:
```bash
python -m venv .env
XXXXXXXXXXXXXXXXXXXXX
```

#### Install Django on environment (if not on env, django needs to be installed globally)
Just run:
`pip install django`
in the project root folder and check that the installation was correct with:
`pip freeze`
which should return something like:
```cmd
asgiref==3.7.2
Django==4.2.7
sqlparse==0.4.4
tzdata==2023.3
```

### Run the project in dev mode
Run the Django-server in terminal with:
`python manage.py runserver`
