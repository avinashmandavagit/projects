import datetime
import re
import pymongo
from flask import Flask, request, render_template , session, redirect
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

from bson import ObjectId
app = Flask(__name__)
app.secret_key = "Sharmi"
my_client = pymongo.MongoClient('mongodb://localhost:27017')
my_db = my_client["House_Management"]
admin_col = my_db['admin']
category_col = my_db['category']
owner_col = my_db['owner']
user_col = my_db['user']
property_col = my_db['property']
rental_col = my_db['rental']
sale_col = my_db['sale']
payment_col = my_db['payment']


count = admin_col.count_documents({})
if count == 0:
    admin = {"Admin_Email": "admin@gmail.com", "Admin_Password": "admin"}
    admin_col.insert_one(admin)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/adminlog")
def adminlog():
    return render_template("adminlog.html")

@app.route("/adminlog1", methods=['post'])
def adminlog1():
    Admin_Email = request.form.get("Admin_Email")
    Admin_Password = request.form.get("Admin_Password")
    query = {"Admin_Email":Admin_Email , "Admin_Password":Admin_Password}
    admin = admin_col.find_one(query)
    if admin != None:
        session['admin_id'] = str(admin['_id'])
        session['role'] = 'Admin'
        return redirect("admin_home")
    else:
        return render_template("message.html" , message="Fail to Log")

@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")

@app.route("/add_category")
def add_category():
    return render_template("add_category.html")

@app.route("/add_category1", methods=['post'])
def add_category1():
    category_name = request.form.get("category_name")
    query = {"category_name":category_name}
    count = category_col.count_documents(query)
    if count == 0:
        category = {"category_name":category_name}
        category_col.insert_one(category)
        return redirect("/view_category")
    else:
        return render_template("amessage.html", message="Fail to Add")

@app.route("/view_category")
def view_category():
    categories = category_col.find()
    return render_template("view_category.html",categories=categories)

@app.route("/ownerlog")
def ownerlog():
    return render_template("ownerlog.html")

@app.route("/ownerlog1", methods=['post'])
def ownerlog1():
    owner_email = request.form.get("owner_email")
    owner_password = request.form.get("owner_password")
    query = {"owner_email": owner_email, "owner_password": owner_password}
    count = owner_col.count_documents(query)
    if count > 0:
        owner = owner_col.find_one(query)
        session['owner_id'] = str(owner['_id'])
        session['role'] = 'owner'
        return redirect("/owner_home")
    else:
        return render_template("omessage.html", message="Fail to Login")

@app.route("/ownerreg")
def ownerreg():
    return render_template("ownerreg.html")

@app.route("/ownerreg1", methods=['post'])
def ownerreg1():
    owner_name = request.form.get("owner_name")
    owner_email = request.form.get("owner_email")
    owner_phone = request.form.get("owner_phone")
    owner_password = request.form.get("owner_password")
    owner_address = request.form.get("owner_address")
    query = {"$or": [{"owner_email": owner_email}, {"owner_phone": owner_phone}]}
    count = owner_col.count_documents(query)
    if count == 0:
        user = {"owner_name": owner_name, "owner_email": owner_email, "owner_phone": owner_phone,
                "owner_password": owner_password, "owner_address": owner_address}
        owner_col.insert_one(user)
        return render_template("message.html", message="Owner Registration Successfully")
    else:
        return render_template("message.html", message="Already Exists")

@app.route("/owner_home")
def owner_home():
    return render_template("owner_home.html")

@app.route("/userlog")
def userlog():
    return render_template("userlog.html")

@app.route("/userlog1", methods = ['post'])
def userlog1():
    user_email = request.form.get("user_email")
    user_password = request.form.get("user_password")
    query = {"user_email": user_email, "user_password": user_password}
    count = user_col.count_documents(query)
    if count > 0:
        user = user_col.find_one(query)
        session['user_id'] = str(user['_id'])
        session['role'] = 'user'
        return redirect("/user_home")
    else:
        return render_template("message.html", message="Fail to Login")

@app.route("/userreg")
def userreg():
    return render_template("userreg.html")

@app.route("/userreg1" , methods = ['post'])
def userreg1():
    user_name = request.form.get("user_name")
    user_email = request.form.get("user_email")
    user_phone = request.form.get("user_phone")
    user_password = request.form.get("user_password")
    user_address = request.form.get("user_address")
    query = {"$or": [{"user_email": user_email}, {"user_phone": user_phone}]}
    count = user_col.count_documents(query)
    if count == 0:
        user = {"user_name": user_name, "user_email": user_email, "user_phone": user_phone,
                "user_password": user_password, "user_address": user_address}
        user_col.insert_one(user)
        return render_template("message.html", message="User Registration Successfully")
    else:
        return render_template("message.html", message="Already Exists")

@app.route("/user_home")
def user_home():
    return render_template("user_home.html")

@app.route("/add_property")
def add_property():
    categories = category_col.find()
    return render_template("add_property.html",categories=categories)

@app.route("/add_property1" , methods = ['post'])
def add_property1():
    category_id = request.form.get("category_id")
    property_title = request.form.get("property_title")
    location = request.form.get("location")
    property_image = request.files.get('property_image')
    path = APP_ROOT + "/static/myfiles/" + property_image.filename
    property_image.save(path)
    description = request.form.get("description")
    features = request.form.get("features")
    amount = request.form.get("amount")
    today = datetime.datetime.now()
    posted_date = str(today.strftime('%Y-%m-%d %H:%M'))
    post_type = request.form.get("post_type")
    carpet_area = request.form.get("carpet_area")
    rooms = request.form.get("rooms")
    advance = request.form.get("advance")
    rent = request.form.get("rent")
    owner_id = session['owner_id']
    query = {"category_id": ObjectId(category_id),"location":location,"owner_id": ObjectId(owner_id),"property_title": property_title,"property_image": property_image.filename,"description": description,"features": features,"amount": amount,"posted_date": posted_date,"post_type":post_type,"status": "Property Posted"}
    result = property_col.insert_one(query)
    if post_type == 'rental':
        query1 = {"carpet_area": carpet_area,"rooms": rooms,"advance": advance,"rent": rent, "property_id": result.inserted_id}
        rental_col.insert_one(query1)
        return render_template("omessage.html", message="Rental Added Successfully")
    return render_template("omessage.html", message="Property Added Successfully")

@app.route("/view_rental_sales")
def view_rental_sales():
    post_type = request.args.get("post_type")
    if session['role'] == 'owner':
        query = {"owner_id": ObjectId(session['owner_id']),"post_type": post_type}
    elif session['role'] == 'user':
        query = {"post_type": post_type}
    print(query)
    properties = property_col.find(query)
    return render_template("view_rental_sales.html",properties=properties,get_category_id=get_category_id,get_owner=get_owner,get_rental_by_property_id=get_rental_by_property_id,is_requested_for_sale=is_requested_for_sale)

def get_category_id(category_id):
    query = {"_id":ObjectId(category_id)}
    category = category_col.find_one(query)
    return category

def get_owner(owner_id):
    query = {"_id": ObjectId(owner_id)}
    owner = owner_col.find_one(query)
    return owner

def get_rental_by_property_id(property_id):
    query = {"property_id": property_id}
    rental = rental_col.find_one(query)
    print(rental)
    return rental

@app.route("/sale_request",methods =['post'])
def sale_request():
    property_id = request.form.get("property_id")
    return render_template("sale_request.html",property_id=property_id)

@app.route("/sale_request1",methods =['post'])
def sale_request1():
    property_id = request.form.get("property_id")
    price = request.form.get("price")
    message = request.form.get("message")
    user_id = session['user_id']
    query = {"property_id": ObjectId(property_id),"price": price,"message": message,"user_id": ObjectId(user_id),"status": "Sale Request Sent"}
    sale_col.insert_one(query)
    return render_template("umessage.html", message="Sale Requested")

def is_requested_for_sale(property_id):
    user_id = session['user_id']
    query = {"property_id": ObjectId(property_id),"user_id": ObjectId(user_id),"status": "Sale Request Sent"}
    count = sale_col.count_documents(query)
    if count == 0:
        return True
    else:
        return False


@app.route("/view_sale_request")
def view_sale_request():
    property_id = request.args.get('property_id')
    if session['role'] == "owner":
        if property_id != None:
            query = {"property_id": ObjectId(property_id)}
        else:
            properties = property_col.find({"owner_id": ObjectId(session['owner_id'])})
            property_ids = []
            for property in properties:
                property_ids.append({"property_id": property['_id']})
                if len(property_ids) == 0:
                    return render_template("umessage.html", message="No Sale Requests")
                query = {"$or": property_ids}
    elif session['role'] == "user":
        if property_id != None:
            query = {"property_id": ObjectId(property_id),"user_id": ObjectId(session['user_id'])}
        else:
            query = {"user_id": ObjectId(session['user_id'])}
    sales = sale_col.find(query)
    return render_template("view_sale_request.html",sales=sales,get_user_id_by_sale=get_user_id_by_sale,property_id=property_id,get_property_id_by_sale=get_property_id_by_sale,get_owner_id_by_property=get_owner_id_by_property)

def get_user_id_by_sale(user_id):
    query = {"_id": ObjectId(user_id)}
    user = user_col.find_one(query)
    return user

def get_property_id_by_sale(property_id):
    query = {"_id": ObjectId(property_id)}
    property = property_col.find_one(query)
    return property

def get_owner_id_by_property(owner_id):
    query = {"_id": ObjectId(owner_id)}
    owner = owner_col.find_one(query)
    return owner

@app.route("/reject")
def reject():
    sale_id = request.args.get("sale_id")
    query = {"_id": ObjectId(sale_id) }
    query1 = {"$set": {"status":"Sale Request Rejected"}}
    sale_col.update_one(query,query1)
    return render_template("omessage.html", message="Sale Request Rejected")

@app.route("/accept")
def accept():
    sale_id = request.args.get("sale_id")
    query = {"_id": ObjectId(sale_id)}
    query1 = {"$set": {"status":"Sale Request Accepted"}}
    sale_col.update_one(query,query1)
    sale = sale_col.find_one(query)
    query = {"property_id": sale['property_id'], "status": "Sale Request Sent"}
    sales = sale_col.find(query)
    for sale in sales:
        query = {"_id":sale['_id']}
        query2 = {"$set": {"status":"Sale Request Rejected"}}
        sale_col.update_one(query,query2)
    return render_template("omessage.html", message="Sale Request Accepted")

@app.route("/cancel")
def cancel():
    sale_id = request.args.get("sale_id")
    query = {"_id": ObjectId(sale_id) }
    query1 = {"$set": {"status":"Sale Request Cancelled"}}
    sale_col.update_one(query,query1)
    return render_template("umessage.html", message="Sale Request Cancelled")

@app.route("/payNow")
def payNow():
    user_id = session['user_id']
    sale_id = request.args.get("sale_id")
    query = {"_id": ObjectId(sale_id) }
    sale = sale_col.find_one(query)
    return render_template("payNow.html",sale=sale,user_id=user_id)

@app.route("/payNow2")
def payNow2():
    price = request.args.get("price")
    user_id = request.args.get("user_id")
    payment_mode = request.args.get("payment_mode")
    today = datetime.datetime.now()
    paid_date = str(today.strftime('%Y-%m-%d %H:%M'))
    sale_id = request.args.get("sale_id")
    query = {"_id": ObjectId(sale_id) }
    query1 = {"$set": {"status":"Property Sold"}}
    sale_col.update_one(query,query1)
    sale = sale_col.find_one(query)
    query = {"_id": sale['property_id']}
    query2 = {"$set": {"status":"Property Sold"}}
    property_col.update_one(query, query2)
    query3 = {"price": price, "user_id": ObjectId(user_id), "payment_mode": payment_mode, "paid_date": paid_date,
              "sale_id": ObjectId(sale_id)}
    payment_col.insert_one(query3)
    return render_template("umessage.html", message="You Owned Property Successfully")

@app.route("/make_as_rented")
def make_as_rented():
    property_id = request.args.get("property_id")
    query = {"_id": ObjectId(property_id)}
    query1 = {"$set": {"status": "Property Rented"}}
    property_col.update_one(query, query1)
    return render_template("omessage.html", message="Property Marked as Rented")
@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


app.run(host='0.0.0.0', port=2023, debug=True)

