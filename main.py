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
	
@app.route('/v1/recommendations', methods=['POST'])
def get_recommendations():
	if not request.json or not 'user' in request.json or not 'user_preferences' in request.json or not 'locations' in request.json:
		abort(400)
	user = request.json['user']
	userpreference = request.json['user_preferences']
	locations = request.json['locations']
	
	print user, request.json['locations'][0]['location_id']
	
	return jsonify({'locations': [
						{
							'locaction_id' : request.json['locations'][0]['location_id'],
							'score' : 21
						}
					]				
				  }), 201
				
@app.route('/v1/feedback', methods=['POST'])
def get_feedback():
	if not request.json or not 'feedback' in request.json:
		abort(400)
	feedback = request.json['feedback']
	
#	print user, request.json['locations'][0]['location_id']
	
	return jsonify(''), 200
 
if __name__ == "__main__":
	app.run()
