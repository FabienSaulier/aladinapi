from flask_restful import Resource

tests = {}

class Test(Resource):
    def get(self, id):
        return {id: tests[id]}

    def put(self, id):
        tests[id] = request.form['data']
        return {id: tests[id]}