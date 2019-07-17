from flask_restful import Resource

urls = [
  {
    "id": 1,
    "item": "Create sample app",
    "status": "Completed"
  },
  {
    "id": 2,
    "item": "Deploy in Heroku",
    "status": "Open"
  },
  {
    "id": 3,
    "item": "Publish",
    "status": "Open"
  }
]

class UrlScrapper(Resource):
  def get(self, id):
    for todo in todos:
      if(id == todo["id"]):
        return todo, 200
    return "Item not found for the id: {}".format(id), 404

  def put(self, id):
    for todo in todos:
      if(id == todo["id"]):
        todo["item"] = request.form["data"]
        todo["status"] = "Open"
        return todo, 200
    return "Item not found for the id: {}".format(id), 404