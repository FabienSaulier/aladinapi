from flask import Flask
from flask_restful import Api

from todo import Todo
from test import Test
from url import Url

app = Flask(__name__)
api = Api(app)

api.add_resource(Todo, "/todo/<int:id>")
api.add_resource(Test, "/test/<int:id>")
api.add_resource(Url, "/url/")



if __name__ == "__main__":
  app.run()