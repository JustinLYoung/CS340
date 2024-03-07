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

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_youngj9"
app.config["MYSQL_PASSWORD"] = "2754"
app.config["MYSQL_DB"] = "cs340_youngj9"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
@app.route("/index")
def index():
    return render_template("index.j2")

@app.route("/classes")
def classes():
    return render_template("classes.j2")

@app.route("/memberships")
def memberships():
    return render_template("memberships.j2")

@app.route("/members_classes")
def members_classes():
    return render_template("members_classes.j2")




@app.route("/")
def home():
    return get_members()

# add and organize data to be displayed on the members table
@app.route('/members')
def get_members():
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

# -- Citation for code to create the get_add_member_form method and populated table
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/add_member", methods=["GET"])
def get_add_member_form():

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

        # # set up cursor to pass through data and commit
        # db.execute_query(db_connection = db_connection, query = query, query_params = (data))
        # cursor = db_connection.cursor()

        # cursor.execute(query, data)
        # db_connection.commit()
        # cursor.close()

        # set up cursor to pass through data and commit
        cursor = db.execute_query(db_connection = db_connection, query = query, query_params = (data))
        cursor.close()

    # redirect back to memberships page
    return redirect("/memberships")

# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_membership/<string:id>")
def delete_membership(id):

    # query to delete a member with our passed id
    query = "DELETE FROM Memberships WHERE membershipID = %s;"

    # set up cursor to pass through data and commit
    cursor = db.execute_query(db_connection = db_connection, query = query, query_params = (id,))
    cursor.close()
    
    # redirect back to memberships page
    return redirect("/memberships")
# TRY THIS:
# @app.route("/delete_membership", methods=["POST"])
# def delete_membership():
#     membership_id = request.form.get('membership_id')
#     # query to delete a member with our passed id
#     query = "DELETE FROM Memberships WHERE membershipID = %s;"

#     # set up cursor to pass through data and commit
#     cursor = db.execute_query(db_connection = db_connection, query = query, query_params = (membership_id,))
#     cursor.close()
    
#     # redirect back to memberships page
#     return redirect("/memberships")

# -- Citation for code to create the get_edit_membership method to populate the dropdown menus 
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/edit_membership/<membershipID>", methods=["GET"])
# add and organize data to be displayed on the Edit Membership Form
def get_edit_membership(membershipID):

    # query to get class's data to pre-populate the form
    # cursor = db_connection
    # query = "SELECT * FROM membership WHERE membershipID = %s;"
    # cursor.execute(membership_query, (membershipID,))
    # membership = cursor.fetchall()
    # query = "SELECT * FROM membership WHERE membershipID = %s;"
    # cursor = db.execute_query(db_connection = db_connection, query = query, query_params = (*membership_query,))
    # cursor.close()

    #     # query to get member's data to pre-populate the form
    # member_query = "SELECT * FROM Members WHERE memberID = %s;"
    # cursor.execute(member_query, (memberID,))
    # member = cursor.fetchone()
    # # query to populate dropdown menu for memberships
    # memberships_query = "SELECT membershipID FROM Memberships;"
    # cursor = db.execute_query(db_connection=db_connection, query=memberships_query)
    # memberships = cursor.fetchall()
    # # cursor.close()
    
    # query to get member's data to pre-populate the form
    membership_query = "SELECT * FROM Memberships WHERE membershipID = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=membership_query, query_params=(membershipID,))
    # cursor.execute(membership_query, (membershipID,))
    membership = cursor.fetchone()
    
    # render edit_member form passing our member, trainers, and memberships data to the template 
    return render_template("edit_membership.j2", membership=membership)

    # # query to populate dropdown menu for trainer
    # trainers_query = "SELECT trainerID, CONCAT(firstName, ' ', lastName) AS Trainer FROM Trainers;"
    # cursor = db.execute_query(db_connection=db_connection, query=trainers_query)
    # trainers = cursor.fetchall()        

    # # query to get class's data to pre-populate the form
    # membership_query = "SELECT * FROM Memberships WHERE membershipID = %s;"
    # cursor = db.execute_query(db_connection=db_connection, query=membership_query)
    # cursor.execute(membership_query, (membershipID,))
    # membership = cursor.fetchone()
    
    # render edit_membership form passing our class, trainers, and memberships data to the template 
    # return render_template("edit_membership.j2", membership=membership)

# -- Citation for code to create the edit_membership method and populated table 
# -- Date: 2/27/24
# -- Based on OSU Flask Starter App GitHub: 
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/edit_membership/<string:membershipID>", methods=["POST"])
def edit_membership(membershipID):
    if request.method == "POST":
        # grab user form inputs
        membershipID = request.form.get("membershipID")  
        price = request.form.get("price")
        details = request.form.get("details")

        # data tuple for the query execution
        data = (
            price,
            details, 
            membershipID    
            )

        # query to update a membership
        query = """
        UPDATE Memberships
        SET price = %s,
            details = %s
        WHERE membershipID = %s;
        """
        
        # execute the query
        cursor = db_connection.cursor()
        cursor.execute(query, data)
        db_connection.commit()
        cursor.close()

    return redirect("/members")

# Trainers

# Citation for the following: trainers, edit_trainers
# Date: 2/29/2024
# Copied from: Github Flask Starter App
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

@app.route("/trainers", methods=["POST", "GET"])
def trainers():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Trainer"):
            # grab user form inputs
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]

            query = "INSERT INTO Trainers (firstName, lastName) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/trainers")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT * FROM Trainers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("trainers.j2", data=data)


# route for delete functionality, deleting a class from Classes,
# we want to pass the 'id' value of that class on button click (see HTML) via the route
@app.route("/delete_class/<int:id>")
def delete_class(id):

    # query to delete a member with our passed id
    query = "DELETE FROM Classes WHERE classID = %s;"

    # set up cursor to pass through data and commit
    cursor = db.execute_query(db_connection = db_connection, query = query, query_params = (id,))
    cursor.close()

    # redirect back to people page
    return redirect("/trainers")

# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_trainers/<int:id>", methods=["POST", "GET"])
def edit_trainers(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Trainers WHERE trainerID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_trainers.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # grab user form inputs
        classType = request.form.get("classType")
        schedule = request.form.get("schedule")
        trainerID = request.form.get("trainerID")  
        
        # data tuple for the query execution
        data = (
            classType,
            schedule, 
            trainerID, 
            classID    
            )

        # query to update a class
        query = """
        UPDATE Classes
        SET classType = %s,
            schedule = %s,
            trainerID = %s
        WHERE classID = %s;
        """

        # set up cursor to pass through data and commit
        cursor = db.execute_query(db_connection = db_connection, query = query, query_params = (*data,))
        cursor.close()

    return redirect("/classes")
# ----------------------------- MemberClasses Page ---------------------------
# @app.route("/members_classes")
# def members_classes_page():
#    return get_member_classes_page()

# KEEP JUST IN CASE:

        # execute the query
        # cursor = db_connection.cursor()
        # cursor.execute(query, data)
        # db_connection.commit()
        # cursor.close()

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=31311, debug=True)