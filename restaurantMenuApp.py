from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def restaurantsHome():
	output="You are at Restaurant Home"
	return (output)

@app.route('/restaurant/new/')
def newRestaurant():
	output="Add new restaurant here"
	return (output)

@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	output="Edit restaurant here"
	return (output)

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
	output="Delete restaurant here"
	return (output)

@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def menuHome(restaurant_id):
	output="Menu Home of a particular restaurant here"
	return (output)

@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
	output="new Menu item here"
	return (output)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	output="Edit item details here"
	return (output)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	output="Delete item details here"
	return (output)
	



if __name__ == '__main__':
	app.secret_key = 'my_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
