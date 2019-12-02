from flask import Flask
from api import api

from flask_cors import CORS


app = Flask(__name__)

cors = CORS(app, resources={"/api/*": {"origins": "http://localhost:3000"}})


app.register_blueprint(api)

if __name__ == "__main__":
    app.run() # host='0.0.0.0', debug=False
