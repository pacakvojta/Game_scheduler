# Script requires libraries that are not installed with python by default (pandas, Flask)- see requierements.txt file
# You can install these libraries with following command:
    # pip install -r requirements.txt

from flask import Flask, render_template, request
from main_scheduler import create_game_schedule # Function with game scheduling

app = Flask(__name__)


# Flask Defining for user's input interactively (Names, number of rounds)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the input values from the form
        player_inputs = {}
        for i in range(1, 15):
            player_inputs[f'player{i}'] = request.form.get(f'player{i}')
        rounds = int(request.form["rounds"])
        text_ouput, matrix_teammates, matrix_opponents = create_game_schedule(**player_inputs, rounds=rounds)

        return render_template("result.html", text_output=text_ouput,  df1=matrix_teammates, df2=matrix_opponents) # Run the function with user's inputs
    else:
        # Render the form template
        return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)