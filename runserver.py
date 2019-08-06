from flask import Flask
from main_view import main_view
from timeseries import timeseries

app = Flask(__name__)
app.register_blueprint(main_view)
app.register_blueprint(timeseries)
if __name__ == "__main__":
    app.run(debug=True)
