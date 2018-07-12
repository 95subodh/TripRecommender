from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request, abort


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
 
@app.route("/")
def hello():
	return "Hello World!"

@app.route('/response')
def get_current_user():
	return jsonify(
		a="1",
		b="2",
		c="3"
	)

@app.route('/cakes')
def cakes():
	return "Yummy cakes!"

tasks = [
	{
		'id': 1,
		'title': u'Buy groceries',
		'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
		'done': False
	},
	{
		'id': 2,
		'title': u'Learn Python',
		'description': u'Need to find a good Python tutorial on the web', 
		'done': False
	}
]
	
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
		abort(400)
	task = {
		'id': tasks[-1]['id'] + 1,
		'title': request.json['title'],
		'description': request.json.get('description', ""),
		'done': False
	}
	tasks.append(task)
	return jsonify({'task': task}), 201
 
if __name__ == "__main__":
	app.run()
