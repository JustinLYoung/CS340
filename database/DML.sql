-- Group 30: Justin Young and Olivia Cruz

-- These are some Database Manipulation queries for the Elite Fitness Project Website

-- SELECT query for every table
-- ADD query for Classes, Members, Trainers, Memberships tables
-- DELETE query for Classes, Members, Trainers, Memberships tables 
-- UPDATE query for Classes, Members, Trainers, Memberships tables 
-- Use of JOINs in SELECT query for MembersClasses, Classes, and Members tables

-- Query for user input will use : character to denote the variables 
-- that will have data from the backend programming language.

-- # Citation for the following queries:
-- # Date: 02/14/2024
-- # Based on cs340 Course Module Database Application Design: 
-- # URL: https://canvas.oregonstate.edu/courses/1946034/pages/exploration-database-application-design?module_item_id=23809325 


--------------------- Classes page ---------------------

  -- populate all details of Classes in the Classes page
SELECT 
    Classes.classID AS "ID",
    Classes.classType AS "Type", 
    Classes.schedule AS "Schedule",
    CONCAT(Trainers.firstName, ' ', Trainers.lastName) AS "Trainer"
FROM Classes
LEFT JOIN Trainers ON Classes.trainerID = Trainers.trainerID;

  -- add a new class (classType and trainerID value comes from a dropdown list)
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

  -- update a class (classType and trainerID value comes from a dropdown list)
UPDATE Classes
SET classType = :classTypeInput, 
    schedule = :scheduleInput, 
    trainerID = :trainerIDInput
WHERE classID = :selected_id_by_the_user;

  -- delete a class
DELETE FROM Classes
WHERE classID = :selected_id_by_the_user;

--------------------- Memberships page ---------------------

  -- populate all details of Memberships in the Memberships page
SELECT     
    Memberships.membershipID AS "ID", 
    Memberships.price AS "Price", 
    Memberships.details AS "Details" 
FROM Memberships;

  -- add a new membership based on the Add Membership form
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

  -- update a membership's data based on the Update Membership form
UPDATE Memberships
SET membershipID = :membershipIDInput, 
    price = :priceInput, 
    details = :detailsInput
WHERE membershipID = :selected_id_by_the_user;

  -- delete a membership
DELETE FROM Memberships
WHERE membershipID = :selected_id_by_the_user;  

--------------------- Members page ---------------------

  -- populate all details of Members in the Members page
SELECT 
    Members.memberID AS "ID",
    Members.firstName AS "First Name",
    Members.lastName AS "Last Name",  
    Members.phoneNumber AS "Phone Number",
    Members.email AS "Email",
    Members.joinDate AS "Join Date",
    Members.birthday AS "Birthday",
    Members.membershipID AS "Membership",
    CONCAT(Trainers.firstName, ' ', Trainers.lastName) AS "Trainer"
FROM Members
LEFT JOIN Trainers ON Members.trainerID = Trainers.trainerID;

  -- add a new member based on the Add Member form
  -- (membershipID and trainerID values come from a dropdown list)
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

  -- update a member's data based on the Update Member form
  -- (membershipID and trainerID values come from a dropdown list)
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
SELECT 
    Trainers.trainerID AS "ID",
    Trainers.firstName AS "First Name",
    Trainers.lastName AS "Last Name"
FROM Trainers;

  -- add a new trainer based on the Add Trainer form
INSERT INTO Trainers (
    firstName, 
    lastName
)
VALUES (
    :firstNameInput, 
    :lastNameInput
);

  -- update a trainer's data based on the Update Trainer form
UPDATE Trainers
SET firstName = :firstNameInput, 
    lastName = :lastNameInput 
WHERE trainerID = :selected_id_by_the_user;

  -- delete a trainer
DELETE FROM Trainers
WHERE trainerID = :selected_id_by_the_user;

--------------------- MemberClasses page ---------------------

  -- retrieve member names with the class type they participate in, 
  -- and their member class ID in the MemberClasses page 
SELECT 
    MemberClasses.memberClassesID AS "ID", 
    CONCAT(Members.firstName, ' ', Members.lastName) AS "Member",
    Classes.classType AS "Class Type"
FROM MemberClasses
INNER JOIN Members ON Members.memberID = MemberClasses.memberID
INNER JOIN Classes ON MemberClasses.classID = Classes.classID;
