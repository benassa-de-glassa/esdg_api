from flask import Flask
from api import api

from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(api)

cors = CORS(app, resources={"/api/*": {"origins": "http://localhost:3000"}})



if __name__ == "__main__":
    app.run()
