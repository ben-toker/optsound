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


### Model Text File
Each model is written in a .txt file in the following format:

- **Line 0** num_variables, num_constraints (not including the nonnegativity constraints) 
- **Line 1:** 'max' or 'min' to indicate the type of problem
- **Line 2:** coefficients of the objective function, separated by commas
- **Constraint lines:** variable coefficients, operator, rhs, separated by commas