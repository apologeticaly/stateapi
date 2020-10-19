from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from states import states
from json import *
from flask_cors import CORS, cross_origin

# States Data
# 0: Abbreviation
# 1: Population
# 2: Main Export
# 3: Average Age
# 4: Flag
# 5: Date of Joining Union
# 6: Median Salary
# 7: Capital
# 8: Last 5 Elections

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def abort_if_todo_doesnt_exist(state):
    if state.upper() not in states:
        abort(404, message="That state does not exist")

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, state):
        abort_if_todo_doesnt_exist(state.upper())
        return states[state.upper()]

    def delete(self, state):
        abort_if_todo_doesnt_exist(state.upper())
        del states[state]
        return '', 204

    def put(self, state):
        args = parser.parse_args()
        task = {'task': args['task']}
        states[state] = task
        return task, 201

class Home(Resource):
    def get(self):
        return jsonify(states)

    def post(self):
        return jsonify(states)



# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return states

    def post(self):
        args = parser.parse_args()
        state = int(max(states.keys()).lstrip('todo')) + 1
        state = 'todo%i' % state
        states[state] = {'task': args['task']}
        return states[state], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/states')
api.add_resource(Todo, '/<state>')
api.add_resource(Home, '/')


if __name__ == '__main__':
    app.run(debug=True)