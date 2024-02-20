from website import create_app
from flask import Flask, render_template
from website import create_app as create_streamlit_app

app = Flask(__name__)

st_app = create_streamlit_app()

# @app.route('/travelplanner', methods=["GET", "POST"])
# def travel_planner():
#     return render_template('travel_planner.html')

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)