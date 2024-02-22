-- Group 30: Justin Young and Olivia Cruz

-- These are some Database Manipulation queries for the Elite Fitness Project Website

-- SELECT query for every table
-- ADD query for Classes, Members, Trainers, Memberships tables
-- DELETE query for Classes, Members, Trainers, Memberships tables 
-- UPDATE query for Classes, Members, Trainers, Memberships tables  
-- Queries for retrieving members based on membership level
-- Query to retrieve the classes that a specific trainer teaches

-- Query for user input will use : character to denote the variables 
-- that will have data from the backend programming language.

-- # Citation for the following queries:
-- # Date: 02/14/2024
-- # Based on cs340 Course Module Database Application Design: 
-- # URL: https://canvas.oregonstate.edu/courses/1946034/pages/exploration-database-application-design?module_item_id=23809325 


--------------------- Classes page ---------------------

  -- get all details of Classes to populate in the Classes page
SELECT * FROM Classes;

  -- add a new class (classType value comes from a dropdown list)
INSERT INTO Classes (
    classType, 
    schedule, 
    trainerID
) 
VALUES(
    :classTypeInput, 
    :scheduleInput, 
    :trainerIDInput
);

  -- update a class (classType value comes from a dropdown list)
UPDATE Classes
SET classType = :classTypeInput, 
    schedule = :scheduleInput, 
    trainerID = :trainerIDInput
WHERE classID = :selected_id_by_the_user;

  -- delete a class
DELETE FROM Classes
WHERE classID = :selected_id_by_the_user;

--------------------- Memberships page ---------------------

  -- get all details of Memberships to populate in the Memberships page
SELECT * FROM Memberships;

  -- add a new membership
INSERT INTO Memberships (
    membershipID, 
    price, 
    details
) 
VALUES(
    :membershipIDInput, 
    :priceInput, 
    :detailsInput
);

  -- update a Memberships
UPDATE Memberships
SET membershipID = :membershipIDInput, 
    price = :priceInput, 
    details = :detailsInput
WHERE membershipID = :selected_id_by_the_user;

  -- delete an Memberships
DELETE FROM Memberships
WHERE membershipID = :selected_id_by_the_user;  

--------------------- Members page ---------------------

  -- get all details of Members to populate in the Members page
SELECT * FROM Members;

  -- add a new member
INSERT INTO Members (
    lastName, 
    firstName, 
    phoneNumber, 
    email, 
    joinDate, 
    birthday, 
    membershipID, 
    trainerID 
) 
VALUES(
    :lastNameInput, 
    :firstNameInput, 
    :phoneNumberInput,
    :emailInput,
    :joinDateInput,
    :membershipIDInput,
    :trainerIDInput
);

  -- update a member's data based on Update Member form
UPDATE Members
SET lastName = :lastNameInput, 
    firstName = :firstNameInput, 
    phoneNumber = :phoneNumberInput,
    email = :emailInput,
    joinDate = :joinDateInput,
    membershipID = :membershipIDInput,
    trainerID = :trainerIDInput
WHERE memberID = :selected_id_by_the_user;

  -- delete a member
DELETE FROM Members
WHERE memberID = :selected_id_by_the_user;

--------------------- Trainers page ---------------------

  -- get all details of Trainers to populate in the Trainers page
SELECT * FROM Trainers;

  -- add a new trainer based on Add Trainer form
INSERT INTO Trainers (
    firstName, 
    lastName, 
    specialization
)
VALUES (
    :firstNameInput, 
    :lastNameInput
);

  -- update a trainer's data based on Update Trainer form
UPDATE Trainers
SET firstName = :firstNameInput, 
    lastName = :lastNameInput 
WHERE trainerID = :selected_id_by_the_user;

  -- delete a trainer
DELETE FROM Trainers
WHERE trainerID = :selected_id_by_the_user;

--------------------- MemberClasses page ---------------------

  -- get all details for MemberClasses to populate in the MemberClasses page
SELECT * FROM MemberClasses;

--------- Queries for retrieving members based on membership level ---------

  -- get all members with MembershipID = 'Gold'
SELECT lastName, firstName, phoneNumber, email
FROM Members
WHERE MembershipID = 'Gold';

  -- get all members with MembershipID = 'Diamond'
SELECT lastName, firstName, phoneNumber, email
FROM Members
WHERE MembershipID = 'Diamond';

  -- get all members with MembershipID = 'Platinum'
SELECT lastName, firstName, phoneNumber, email
FROM Members
WHERE MembershipID = 'Platinum';

--------- Query to retrieve the classes that a specific trainer teaches ---------

  -- get all classes and schedules for a specific trainer 
SELECT Classes.classType, Classes.schedule
FROM Classes
JOIN Trainers ON Classes.trainerID = Trainers.trainerID
WHERE Trainers.trainerID = :selected_trainer_id;  
