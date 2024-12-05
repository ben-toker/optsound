from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Example: Procedurally generate LP model components
    objective_function = r"3x_1 + 5x_2"
    constraints = [
        r"x_1 + 2x_2 \leq 6",
        r"3x_1 + 2x_2 \leq 12",
        r"x_1, x_2 \geq 0"
    ]

    # Use align* for proper line breaks in LaTeX
    lp_model_latex = r"""
    \text{{Maximize:}}  \quad {} \\
    \text{{Subject to:}}  \\
    """.format(objective_function)
    
    for constraint in constraints:
        lp_model_latex += constraint + r" \\"  # Add line breaks

    return render_template("index.html", lp_model_latex=lp_model_latex)

if __name__ == "__main__":
    app.run(debug=True)

