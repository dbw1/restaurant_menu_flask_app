from flask import Flask, render_template
import FakeMenuItems 
app = Flask(__name__)

#test restaurants and menus because we don't have an actual db yet

restaurants = FakeMenuItems.restaurants
restaurant = FakeMenuItems.restaurant

items = FakeMenuItems.items
item = FakeMenuItems.item

@app.route('/')
@app.route('/restaurants/')
def restaurantsHome():
	# new home logic
	return render_template('restaurantHome.html', restaurant_list=restaurants)

@app.route('/restaurant/new/')
def newRestaurant():
	
	return render_template('newRestaurant.html', restaurant=restaurants)

@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	
	return render_template('editRestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
	
	return render_template('deleteRestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def menuHome(restaurant_id):
	
	return render_template('menuHome.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
	
	return render_template('newMenuItem.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	
	return render_template('editMenuItem.html', restaurant=restaurant, item=item, menuID=menu_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	
	return render_template('deleteMenuItem.html', restaurant=restaurant, item=item, menuID=menu_id)
	



if __name__ == '__main__':
	app.secret_key = 'my_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
