from flask import Flask
from flask_restful import Api

from todo import Todo
from urlScrapper import urlScrapper

app = Flask(__name__)
api = Api(app)

api.add_resource(Todo, "/todo/<int:id>")

api.add_resource(urlScrapper, "/scrap/url/<string:url>")


if __name__ == "__main__":
  app.run()