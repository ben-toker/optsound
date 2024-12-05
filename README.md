### venv build
To create the virtual environment, navigate to the source folder and build:
```
python -m venv venv
```
Activate (this is for macOS):
```
source venv/bin/Activate
```
Double check, should print venv filepath
```
which python3
```
To install requirements:
```
pip install -r requirements.txt
```

To render the flask app:
```
python3 render.py
```
