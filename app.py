from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from todo import Todo
from url import Url

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Todo, "/todo/<int:id>")
api.add_resource(Url, "/")



if __name__ == "__main__":
  app.run()