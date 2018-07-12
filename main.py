from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request, abort
from random import randrange
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

os.chdir("/Users/subyadav/Desktop")

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/")
def hello():
	return "Hello World!"
	
@app.route('/v1/recommendations', methods=['POST'])
def get_recommendations():
#	if first_run:
#		train()
#		first_run=False
		
	if not request.json or not 'user' in request.json or not 'user_preferences' in request.json or not 'locations' in request.json:
		abort(400)
	user = request.json['user']
	userpreference = request.json['user_preferences']
	locations = request.json['locations']
	loc_length = len(locations)
	
	print user, request.json['locations'][0]['location_id']
	loc_list=[loc['location_id'] for loc in locations]
	user_list=[user['user_id']]*loc_length
	genderlist=[convert_gender(user['sex'])]*loc_length
	agelist=[user['age']]*loc_length
	rating_list=[loc['rating'] for loc in locations]
	cat_list=[loc['categories'][0] for loc in locations]
	num_list=[loc['popularity'] for loc in locations]
	atlist=[convertAT(loc['area_type']) for loc in locations]
	
	print()
	print loc_list, rating_list, cat_list, genderlist
	print()

	df = pd.DataFrame(data={"LocationIndex": loc_list, "UserID(int)": user_list, "Sex(M=0,F=1)": genderlist, "AgeUser": agelist, "City(use 1)": [1]*loc_length, 
								"Ratings(copy)": rating_list, "Category(use key below)": cat_list, "Number of users visited(copy)": num_list, "AreaType(0=indoor, 1=outdoor)": atlist })
	results = predict(df)
#	results=[1,1]
	loc_arr = []
	for i in xrange(len(locations)):
		loc_arr.append(
			{
				'location_id' : request.json['locations'][i]['location_id'],
				'score' : results[i]
			}
		)
	
	return jsonify({'locations': loc_arr}), 201
				
@app.route('/v1/feedback', methods=['POST'])
def get_feedback():
	if not request.json or not 'feedback' in request.json:
		abort(400)
	feedback = request.json['feedback']
	
#	print user, request.json['locations'][0]['location_id']
	
	return jsonify(''), 200
	
	

data = pd.read_csv("feedback_yourname2.csv")
#	data.head(25)
#data= pd.get_dummies(data)
#	data.iloc[:,5:].head(5)
labels = np.array(data['Score (your rating)'])
data= data.drop('Score (your rating)', axis = 1)
data_list = list(data.columns)
data_arr = np.array(data)
train_features, test_features, train_labels, test_labels = train_test_split(data, labels, test_size = 0.25, random_state = 42)

print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)

rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
rf.fit(train_features, train_labels);

predictions = rf.predict(test_features)
print predictions
# Calculate the absolute errors
errors = abs(predictions - test_labels)
# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(np.mean(errors), 2), 'ratings.')

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / test_labels)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

def predict(df):
#	df= pd.get_dummies(df)
	
	predictions = rf.predict(df)
	return predictions
def convert_gender(s):
	return 1 if s=='F' else 0

def convertAT(s):
	return 1 if s=='OUTDOOR' else 0
 
if __name__ == "__main__":
	app.run()
