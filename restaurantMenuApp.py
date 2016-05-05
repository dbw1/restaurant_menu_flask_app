from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
import config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

app = Flask(__name__)


#DB importing through sqlalchemy session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/JSON')
def restaurantJSON():
	restaurants = session.query(Restaurant)
	return jsonify(restaurant_list=[i.serialize for i in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def itemMenuJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id=menu_id).one()
	return jsonify(MenuItem=item.serialize)

	# try:
	# 	item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id=menu_id).one()
	# 	return jsonify(MenuItem=item.serialize)
	# except:
	# 	return "No Entry"

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return jsonify(MenuItem=[i.serialize for i in items])


#Actual WebApp routing
@app.route('/')
@app.route('/restaurants/')
def restaurantsHome():
	restaurants = session.query(Restaurant)
	return render_template('restaurantHome.html', restaurant_list=restaurants)

@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
	restaurants = session.query(Restaurant)
	if request.method == "POST":
		if request.form['restaurant_name']:
			newRest = Restaurant(name = request.form['restaurant_name'])
			session.add(newRest)
			session.commit()
			return redirect(url_for('restaurantsHome'))
		else:
			flash("Please Enter Restaurant Name or Press Cancel")
			return redirect(url_for('newRestaurant'))
	else:
		return render_template('newRestaurant.html', restaurant=restaurants)

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == "POST":
		if request.form['restaurant_name']: restaurant.name = request.form['restaurant_name']
		session.add(restaurant)
		session.commit()
		return redirect(url_for('restaurantsHome'))
	else:
		return render_template('editRestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == "POST":
		session.delete(restaurant)
		session.commit()
		return redirect(url_for('restaurantsHome'))
	else:
		return render_template('deleteRestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def menuHome(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menuHome.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == "POST":
		if request.form['name']:
			newItem = MenuItem(name = request.form['name'], restaurant_id= restaurant_id)
			newItem.price = '$' + request.form['price']
			newItem.description = request.form['description']
			session.add(newItem)
			session.commit()
			flash("New Menu Item Created!") #a session based message
			return redirect(url_for('menuHome',restaurant_id=restaurant_id))
		else:
			flash("Please enter an item name")
			return redirect(url_for('newMenuItem',restaurant_id=restaurant_id, buttons=config.item_type))
	else:
		return render_template('newMenuItem.html', restaurant=restaurant, buttons=config.item_type)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	editItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id=menu_id).one()
	if request.method == "POST":
		if request.form['name']: editItem.name = request.form['name']
		if request.form['price']: editItem.price = '$' + request.form['price']
		if request.form['description']: editItem.description = request.form['description']
		if request.form['course']:
			for button in config.item_type:
				if request.form['course'] == button:
					editItem.course = button

		session.add(editItem)
		session.commit()
		return redirect(url_for('menuHome',restaurant_id=restaurant_id))
	else:	
		return render_template('editMenuItem.html', restaurant=restaurant, item=editItem, menuID=menu_id, buttons=config.item_type,
		                 active_btns=[editItem.course])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	deleteItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id=menu_id).one()
	if request.method == "POST":
		session.delete(deleteItem)
		session.commit()
		return redirect(url_for('menuHome',restaurant_id=restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant=restaurant, item=deleteItem, menuID=menu_id)
	



if __name__ == '__main__':
	app.secret_key = 'my_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
