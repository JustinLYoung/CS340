# -- Citation for code to create the members jinja2 file layout and populated table
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/app.py

import os

from flask_mysqldb import MySQL
from flask import Flask, render_template, json, redirect, request

import database.db_connector as db


app = Flask(__name__)

db_connection = db.connect_to_database()

# Routes

@app.route("/") #changed this from /index so it will be the first page that will be displayed with our url
def home_page():
    return render_template("index.j2")

# @app.route("/index")
# def index():
    # return render_template("index.j2")

# @app.route("/classes")
# def classes_page():
#     return render_template("classes.j2")

# ------------------------------- Trainers Page ------------------------------

@app.route("/trainers")
def trainers_page():
    return render_template("trainers.j2")

# @app.route("/memberships")
# def memberships_page():
#     return render_template("memberships.j2")

# ------------------------------- Members Page -------------------------------

# add and organize data to be displayed on the Members table
@app.route('/members')
def members_page():
    query = """
    SELECT 
    Members.memberID AS 'ID',
    Members.firstName AS 'First Name',
    Members.lastName AS 'Last Name',  
    Members.phoneNumber AS 'Phone Number',
    Members.email AS 'Email',
    Members.joinDate AS 'Join Date',
    Members.birthday AS 'Birthday',
    Members.membershipID AS 'Membership',
    CONCAT(Trainers.firstName, ' ', Trainers.lastName) AS 'Trainer'
    FROM Members
    LEFT JOIN Trainers 
    ON Members.trainerID = Trainers.trainerID;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("members.j2", Members=results);

# -- Citation for code to create the get_add_member method and populated table
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/add_member", methods=["GET"])
def get_add_member():

    # query to populate dropdown menu for trainer
    trainers_query = "SELECT trainerID, CONCAT(firstName, ' ', lastName) AS Trainer FROM Trainers;"
    cursor = db.execute_query(db_connection=db_connection, query=trainers_query)
    trainers = cursor.fetchall()        

    # query to populate dropdown menu for memberships
    memberships_query = "SELECT membershipID FROM Memberships;"
    cursor = db.execute_query(db_connection=db_connection, query=memberships_query)
    memberships = cursor.fetchall()
    cursor.close()
    
    # render add_member form passing our fetched trainers and memberships to the template 
    return render_template("add_member.j2", trainers=trainers, memberships=memberships)

# -- Citation for code to create the add_member method and populated table
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/add_member", methods=["POST"])
# adds a member into the Members table
def add_member():
    if request.method == "POST":
        # grab user form inputs
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        phoneNumber = request.form.get("phoneNumber")
        email = request.form.get("email")
        joinDate = request.form.get("joinDate")
        birthday = request.form.get("birthday")
        membershipID = request.form.get("membershipID")
        trainerID = request.form.get("trainerID", None)

        # query to insert a new member
        query = """
        INSERT INTO Members (
            firstName, 
            lastName, 
            phoneNumber, 
            email, 
            joinDate, 
            birthday, 
            membershipID, 
            trainerID
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            firstName, 
            lastName, 
            phoneNumber, 
            email, 
            joinDate,
            birthday, 
            membershipID, 
            trainerID
        )

        # query to enter a new member that does not have a trainer
        if not trainerID:  
            query = """
            INSERT INTO Members (
                firstName, 
                lastName, 
                phoneNumber, 
                email, 
                joinDate, 
                birthday, 
                membershipID
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                firstName, 
                lastName, 
                phoneNumber, 
                email, 
                joinDate, 
                birthday, 
                membershipID
            )

        # set up cursor to pass through data and commit
        db.execute_query(db_connection = db_connection, query = query, query_params = (data))
        cursor = db_connection.cursor()
        db_connection.commit()
        cursor.close()

    # redirect back to members page
    return redirect("/members")

# -- Citation for code to create the delete_member method
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_member/<int:id>")
def delete_member(id):

    # query to delete a member with our passed id
    query = "DELETE FROM Members WHERE memberID = %s;"

    cursor = db_connection.cursor()
    cursor.execute(query, (id,))
    db_connection.commit()
    cursor.close()
    
    # redirect back to members page
    return redirect("/members")

# -- Citation for code to create the get_edit_member method to populate the dropdown menus 
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/edit_member/<int:memberID>", methods=["GET"])
# add and organize data to be displayed on the Edit Member Form
def get_edit_member(memberID):

    # query to populate dropdown menu for trainer
    trainers_query = "SELECT trainerID, CONCAT(firstName, ' ', lastName) AS Trainer FROM Trainers;"
    cursor = db.execute_query(db_connection=db_connection, query=trainers_query)
    trainers = cursor.fetchall()        

    # query to populate dropdown menu for memberships
    memberships_query = "SELECT membershipID FROM Memberships;"
    cursor = db.execute_query(db_connection=db_connection, query=memberships_query)
    memberships = cursor.fetchall()
    # cursor.close()

    # query to get member's data to pre-populate the form
    member_query = "SELECT * FROM Members WHERE memberID = %s;"
    cursor.execute(member_query, (memberID,))
    member = cursor.fetchone()
    
    # render edit_member form passing our member, trainers, and memberships data to the template 
    return render_template("edit_member.j2", member=member, trainers=trainers, memberships=memberships)

# -- Citation for code to create the edit_member method and populated table 
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/edit_member/<int:memberID>", methods=["POST"])
def edit_member(memberID):
    if request.method == "POST":
        # grab user form inputs
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        phoneNumber = request.form.get("phoneNumber")
        email = request.form.get("email")
        joinDate = request.form.get("joinDate")
        birthday = request.form.get("birthday")
        membershipID = request.form.get("membershipID")
        trainerID = request.form.get("trainerID") or None  
        
        # data tuple for the query execution
        data = (firstName,
                lastName,
                phoneNumber,
                email, 
                joinDate, 
                birthday, 
                membershipID, 
                trainerID, 
                memberID
            )

        # query to update a member
        query = """
        UPDATE Members
        SET firstName = %s,
            lastName = %s,
            phoneNumber = %s,
            email = %s,
            joinDate = %s,
            birthday = %s,
            membershipID = %s,
            trainerID = %s
        WHERE memberID = %s;
        """
        
        # query to enter a new member that does not have a trainer
        if not trainerID or trainerID == None:  
            query = """
            UPDATE Members
            SET firstName = %s,
                lastName = %s,
                phoneNumber = %s,
                email = %s,
                joinDate = %s,
                birthday = %s,
                membershipID = %s,
                trainerID is None
            WHERE memberID = %s;
            """

        # execute the query
        cursor = db_connection.cursor()
        cursor.execute(query, data)
        db_connection.commit()
        cursor.close()

    return redirect("/members")

# ------------------------------ Memberships Page ----------------------------

@app.route("/memberships")
# add and organize data to be displayed on the Memberships table
def memberships_page():
   query = """
   SELECT
   Memberships.membershipID AS 'ID',
   Memberships.price AS 'Price',
   Memberships.details AS 'Details'
   FROM Memberships; 
   """
   cursor = db.execute_query(db_connection=db_connection, query=query)
   results = cursor.fetchall()
   return render_template("memberships.j2", Memberships=results);

# -- Citation for code to create the get_add_member method and populated table
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub:
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/add_membership", methods=["GET"])
def get_add_membership():  
  
   # render add_membership form passing our fetched trainers details to the template
   return render_template("add_membership.j2")

# -- Citation for code to create the add_class method and populated table
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub:
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/add_membership", methods=["POST"])
# adds a membership into the Membership table
def add_membership():
   if request.method == "POST":
       # grab user form inputs
       membershipID = request.form.get("membershipID")
       price = request.form.get("price")
       details = request.form.get("details")

       # query to insert a new membership
       query = """
           INSERT INTO Memberships (
               membershipID,
               price,
               details
       )
       VALUES (%s, %s, %s)
       """
       data = (
           membershipID,
           price,
           details,
       )
       
       # set up cursor to pass through data and commit
       db.execute_query(db_connection = db_connection, query = query, query_params = (data))
       cursor = db_connection.cursor()
       db_connection.commit()
       cursor.close()

   # redirect back to memberships page
   return redirect("/memberships")

@app.route("/delete_membership/<int:id>")
def delete_membership(id):

    # query to delete a membership with our passed id
    query = "DELETE FROM Memberships WHERE membershipID = %s;"

    cursor = db_connection.cursor()
    cursor.execute(query, (id,))
    db_connection.commit()
    cursor.close()
    
    # redirect back to memberships page
    return redirect("/memberships")

# -- Citation for code to create the get_edit_member method to populate the dropdown menus 
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/edit_membership/<int:membershipID>", methods=["GET"])
# add and organize data to be displayed on the Edit Member Form
def get_edit_membership(membershipID):

    # query to get member's data to pre-populate the form
    membership_query = "SELECT * FROM Memberships WHERE membershipID = %s;"
    cursor.execute(membership_query, (membershipID,))
    membership = cursor.fetchone()
    
    # render edit_member form passing our member, trainers, and memberships data to the template 
    return render_template("edit_membership.j2", membership=membership)

# -- Citation for code to create the edit_member method and populated table 
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/edit_membership/<int:membershipID>", methods=["POST"])
def edit_membership(membershipID):
    if request.method == "POST":
        # grab user form inputs
        membershipID = request.form.get("ID")
        price = request.form.get("Price")
        details = request.form.get("Details")
           
        # data tuple for the query execution
        data = (membershipID,
                price,
                details,
            )

        # query to update a memberships
        query = """
        UPDATE Memberships
        SET membershipID = %s,
            price = %s,
            details = %s,
        WHERE membershipID = %s;
        """
        
        # execute the query
        cursor = db_connection.cursor()
        cursor.execute(query, data)
        db_connection.commit()
        cursor.close()

    return redirect("/memberships")
# ------------------------------- Classes Page -------------------------------

@app.route("/classes")
# add and organize data to be displayed on the Classes table
def classes_page():
   query = """
   SELECT
   Classes.classID AS 'ID',
   Classes.classType AS 'Type',
   Classes.schedule AS 'Schedule', 
   CONCAT(Trainers.firstName, ' ', Trainers.lastName) AS 'Trainer'
   FROM Classes
   LEFT JOIN Trainers
   ON Classes.trainerID = Trainers.trainerID;
   """
   cursor = db.execute_query(db_connection=db_connection, query=query)
   results = cursor.fetchall()
   return render_template("classes.j2", Classes=results);

# -- Citation for code to create the get_add_class method and populated table
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub:
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/add_class", methods=["GET"])
def get_add_class():

   # query to populate dropdown menu for trainer
   trainers_query = "SELECT trainerID, CONCAT(firstName, ' ', lastName) AS Trainer FROM Trainers;"
   cursor = db.execute_query(db_connection=db_connection, query=trainers_query)
   trainers = cursor.fetchall()       
  
   # render add_class form passing our fetched trainers details to the template
   return render_template("add_class.j2", trainers=trainers)

# -- Citation for code to create the add_class method and populated table
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub:
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/add_class", methods=["POST"])
# adds a member into the Classes table
def add_class():
   if request.method == "POST":
       # grab user form inputs
       classType = request.form.get("classType")
       schedule = request.form.get("schedule")
       trainerID = request.form.get("trainerID", None) 

       # query to insert a new class
       query = """
           INSERT INTO Classes (
               classType,
               schedule,
               trainerID
       )
       VALUES (%s, %s, %s)
       """
       data = (
           classType,
           schedule,
           trainerID,
       )

       # query to enter a new class that does not have a trainer
       if not trainerID: 
           query = """
           INSERT INTO Classes (
               classType,
               schedule,
               trainerID
           )
           VALUES (%s, %s, %s)
           """
           data = (
               classType,
               schedule,
               trainerID
           )

       # set up cursor to pass through data and commit
       db.execute_query(db_connection = db_connection, query = query, query_params = (data))
       cursor = db_connection.cursor()
       db_connection.commit()
       cursor.close()

   # redirect back to classes page
   return redirect("/classes")

# -- Citation for code to create the get_edit_class method to populate the dropdown menu 
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/edit_class/<int:classID>", methods=["GET"])
# add and organize data to be displayed on the Edit Class Form
def get_edit_class(classID):

    # query to populate dropdown menu for trainer
    trainers_query = "SELECT trainerID, CONCAT(firstName, ' ', lastName) AS Trainer FROM Trainers;"
    cursor = db.execute_query(db_connection=db_connection, query=trainers_query)
    trainers = cursor.fetchall()        

    # query to get class data to pre-populate the form
    class_query = "SELECT * FROM Classes WHERE classID = %s;"
    cursor.execute(class_query, (classID,))
    classes = cursor.fetchone()
    
    # render edit_class form passing our trainers data to the template 
    return render_template("edit_class.j2", classes=classes, trainers=trainers)

# -- Citation for code to create the delete_class method
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

# route for delete functionality, deleting a class from Classes,
# we want to pass the 'id' value of that class on button click (see HTML) via the route
# @app.route("/delete_class/<int:classID>", methods=["POST"])
# def delete_class(classID):

#     # query to delete a member with our passed id
#     query = "DELETE FROM Classes WHERE classID = %s;"

#     cursor = db_connection.cursor()
#     cursor.execute(query, (classID,))
#     db_connection.commit()

@app.route("/delete_class/<int:id>")
def delete_class(id):

    # query to delete a class with our passed id
    query = "DELETE FROM Class WHERE classID = %s;"

    cursor = db_connection.cursor()
    cursor.execute(query, (id,))
    db_connection.commit()
    cursor.close()
    
    # redirect back to classes page
    return redirect("/classes")

# ----------------------------- MemberClasses Page ---------------------------
# @app.route("/members_classes")
# def members_classes_page():
#    return get_member_classes_page()

# add and organize data to be displayed on the Classes table
# @app.route('/members_classes')
# def get_member_classes_page():
#    query = """
#    SELECT
#    Classes.classID AS 'ID',
#    Classes.classType AS 'Type',
#    Classes.schedule AS 'Schedule', 
#    CONCAT(Trainers.firstName, ' ', Trainers.lastName) AS 'Trainer'
#    FROM Classes
#    LEFT JOIN Trainers
#    ON Classes.trainerID = Trainers.trainerID;
#    """
#    cursor = db.execute_query(db_connection=db_connection, query=query)
#    results = cursor.fetchall()
#    return render_template("classes.j2", Classes=results);

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=31311, debug=True)