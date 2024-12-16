# Usage
## venv build
To create the virtual environment, navigate to the source folder and build:
```
python -m venv venv
```
Activate (for macOS):
```
source venv/bin/Activate
```
Double check that the venv filepath is printed:
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

<!-- ## optsound platform
(TODO: write stuff about the interface here) -->

# The Program

## files
### render.py
Handles the frontend, rendering the optsound platform. 

This is where we collect user input and display the optimization model that gets created, along with the link to the optimal solution playlist.

### parse.py
Handles user input.

This is where we parse the user input collected in **render.py**, which is used to model the optimization problem. We then write text file representation of the model (*model.txt*) that **solve.py** can later use to actually construct and solve the problem.

The *model.txt* file format is built as follows:

- **Line 0:** number of constraints listed in the file, list of all decision variable names, separated by commas.
- **Line 1:** type of problem, represented as either 'max' or 'min'.
- **Line 2:** objective function coefficients, separated by commas.
- **Constraint lines:** variable coefficients, operator symbol and the constraint's rhs value, separated by commas.


### solve.py
Interprets *model.txt*.

We read *model.txt* and construct it as an integer programming optimization problem using the **cvxpy** library. We can then solve it and return the objective function, the constraints, and the optimal solution values for the variables.

### playlist.py
Creates and returns the playlist based on the set of optimal values found in **solve.py**. 

## order of events
1. user input is collected **(auth.py)**
2. user input is used to model the corresponding optimization problem **(parse.py)**
3. a representation of the model is written to *models/custom.txt* **(parse.py)**
4. *custom.txt* is used to construct the optimization problem **(solve.py)**
5. the problem is solved **(solve.py)**
6. the constructed objective function, constraints, and optimal values are returned **(solve.py)**
7. the playlist is created based on the optimal values **(playlist.py)**
8. the link to the playlist is displayed **(render.py)**
9. the optimization problem model used to create the playlist is displayed **(render.py)**