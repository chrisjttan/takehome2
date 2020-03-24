# Step 01: import necessary libraries/modules
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# your code begins here 

# Step 02: initialize flask app here 
app = Flask(__name__)
app.debug = True

# Step 03: add database configurations here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://asm02user:password@localhost:5432/asm02db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Step 04: import models
from models import User, Temperature

# Step 05: add routes and their binded functions here
@app.route('/user/', methods=['POST']) 
def create_user():
	print('create_user')

	# start your code after this line

	#check if name and contact in request.json
	if 'name' not in request.json:
		return 'Error, <name> parameter is mandatory'
	if 'contact' not in request.json:
		return 'Error, <contact> parameter is mandatory'

	new_name = request.json['name']
	new_contact_number = request.json['contact']

	#check type(name) and if name is unique
	if type(new_name) != str:
		return 'Error, name entered must be a string'

	if User.query.filter_by(name=new_name).first() != None:
		return 'Error, name already exists in database'


	#check type(contact_number), len(contact_number) == 8 and if contact_number is unique
	if type(new_contact_number) != int:
		return 'Error, contact number entered must be an integer'

	if len(str(new_contact_number)) != 8:
		return 'Error, contact number not 8 digits'

	if User.query.filter_by(contact_number=new_contact_number).first() != None:
		return 'Error, contact number already exists in database'

	#add user into database, should have no error from here alr, delete the try&except?
	try:
		new_user = User(name = new_name, contact_number = new_contact_number)
		db.session.add(new_user)
		db.session.commit()
		return jsonify('new user {} was created with id {}'.format(new_name, new_user.id))
	except Exception as e:
		return (str(e))	

	# end your code before this line

@app.route('/temp/', methods=['POST']) 
def create_temp():
	print('create_temp')

	# start your code after this line

	#check if name and temp_value in request.json
	if 'name' not in request.json:
		return 'Error, <name> parameter is mandatory'
	if 'temp' not in request.json:
		return 'Error, <temp> parameter is mandatory'


	#check type(name) and if name exists in database
	thisuser = request.json['name']
	if type(thisuser) != str:
		return 'Error, name entered must be a string'

	if User.query.filter_by(name=thisuser).first() == None:
		return 'Error, name entered does not exist in database'

	#check type(temp)
	new_temp_value = request.json['temp']
	try:
		new_temp_value = float(new_temp_value)
	except:
		return 'Error, temperature value entered must be a float'

	try:
		new_temp_input = Temperature(temp_value = new_temp_value, user_name = thisuser)
		db.session.add(new_temp_input)
		db.session.commit()
		return jsonify('new temp record {} was created for user {}'.format(new_temp_value, thisuser))
	except Exception as e:
		return (str(e))
	# end your code before this line

@app.route('/friend/', methods=['PUT']) 
def update_friend():
	print('update_friend')

	# start your code after this line

	# end your code before this line

@app.route('/user/', methods=['GET']) 
def get_user():
	print('get_user')

	# start your code after this line

	all_user = User.query.all()
	# all_temp = Temperature.query.all()
	if all_user is None:
		return 'Error, you have added in any of your friends\' information yet.'

	return jsonify([u.serialize() for u in all_user])

	# end your code before this line

@app.route('/temp/', methods=['GET']) 
def get_temp():
	print('get_temp')

	# start your code after this line
	if 'name' in request.args: 
		name = request.args.get('name')
		person = Temperature.query.filter_by(user_name=name)
		if person.first() is not None:
			return jsonify([t.serialize() for t in person])
		else:
			return "You have entered an invalid name."

	all_temp = Temperature.query.all()
	if all_temp is None:
		return 'Error, no one has inputted any temperature reading yet.'
		
	return jsonify([t.serialize() for t in all_temp])
	# end your code before this line

# your code ends here 




if __name__ == '__main__':
	app.run(debug=True)
