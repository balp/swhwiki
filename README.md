swhwiki
=======


Getting Started
---------------

### Unix/Linux/MacOS/WSL

- Change directory into your newly created project if not already there. Your
  current directory should be the same as this README.txt file and setup.py. 

        cd swhwiki

- Create a Python virtual environment, if not already created.

        python3 -m venv env

- Upgrade packaging tools, if necessary.

        env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

        env/bin/pip install -e ".[testing]"

- Run your project's tests.

        env/bin/pytest --cov

- Set up database.

        env/bin/initialize_tutorial_db development.ini 

- Run your project.

        env/bin/pserve development.ini

### Windows 

- Change directory into your newly created project if not already there. Your
  current directory should be the same as this README.txt file and setup.py. 

        cd swhwiki

- Create a Python virtual environment, if not already created.

        python3 -m venv env

- Upgrade packaging tools, if necessary.

        .\env\Scripts\python -m pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

        .\env\Scripts\python -m pip install -e ".[testing]"

- Run your project's tests.

        .\env\Scripts\python -m pytest --cov

- Set up database.

        .\env\Scripts\initialize_tutorial_db.exe development.ini 

- Run your project.

        .\env\Scripts\pserve .\development.in
