from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.secret_key = "C4XXQmDJns"

api = Api(app)

import geoapi.resources.sale
import geoapi.resources.user


if __name__ == '__main__':
    app.run(debug=True)