from flask import Flask, render_template
from solve import solve


app = Flask(__name__)

@app.route("/")
def index():
    model_obj, model_constraints, opt_val, x_solutions = solve('models/test.txt')
    # Example: Procedurally generate LP model components
    objective_function = model_obj
    constraints = model_constraints

    # Use align* for proper line breaks in LaTeX
    
    lp_model_latex = r"""
    \begin{{aligned}}
    \text{{Maximize:}} & \quad {} \\
    \text{{Subject to:}} & \quad {} \\
    & \quad {}
    \end{{aligned}}
    """.format(
        objective_function,
        constraints[0],  # First constraint
        " \\\\ & \\quad ".join(constraints[1:]))

    return render_template("index.html", lp_model_latex=lp_model_latex)

if __name__ == "__main__":
    app.run(port=3000,debug=True)

