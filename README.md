# Current project state

We have resumed development with a new approach. Instead of relying on Spotify’s API for feature classification, we now train and use an in-house machine learning model to classify tracks based on audio features. These predicted classifications serve as inputs to the optimization model. The optimization workflow and platform remain the same, but all feature data now comes from our own models rather than external APIs.

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

# The Program

## files

### render.py

Handles the frontend, rendering the optsound platform.
Collects user inputs and displays the final optimization model and resulting playlist.

### parse.py

Processes user input and prepares the optimization model.
After gathering the track-level data (including ML-derived feature classifications), we translate the modeling choices into a text representation (_model.txt_) that **solve.py** uses to construct the optimization problem.

The _model.txt_ file format:

- **Line 0:** decision variable names, comma-separated
- **Line 1:** problem type: `max` or `min`
- **Line 2:** objective coefficients, comma-separated
- **Constraint lines:** variable coefficients, operator symbol, and RHS value, comma-separated

### solve.py

Reads _model.txt_ and builds the optimization problem using **cvxpy**.
Returns the constructed objective, constraints, and optimal variable assignments.

### playlist.py

Builds the playlist based on the optimal variable values produced by **solve.py**.
(Uses the selected tracks from the ML+optimization pipeline rather than relying on Spotify feature metadata.)

### ml_model/ (new conceptual component)

Contains the machine learning pipeline for track classification.
This includes data preprocessing, model training, and exporting predictions for use in **parse.py**.

## order of events

1. user input is collected **(auth.py)**
2. track data is passed through the ML classification model **(ml_model/)**
3. user input + ML-derived features are used to build the optimization model **(parse.py)**
4. the model specification is written to _models/custom.txt_ **(parse.py)**
5. _custom.txt_ is interpreted into a cvxpy problem **(solve.py)**
6. the problem is solved **(solve.py)**
7. objective, constraints, and optimal values are returned **(solve.py)**
8. playlist is constructed from the optimal set of tracks **(playlist.py)**
9. the playlist link and optimization model summary are displayed **(render.py)**
