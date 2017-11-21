# Design

## Architecture
* Python Flask server generating form based HTML pages via templating engine
* The initial DB will sqllite for simplicity, but care will be take code designed to be able to run with another DB
    * Possibly able to be configured with a config file at startup that indicates the connector to use and the DBs
     url/filepath?
* Not thinking about making it pretty until after basic functionality is done (CSS etc)

## Site Layout

### Home
* Simple page containing a rules explanation, a login form (user,password), and a register button

### Create User
* Forms for Email, Password, First and Last
    * First and Last are not required, used for display only

### User Home
* List of group invites with join button
* List of active groups (links to group home)
* Button to Crate a group
* Button to view old groups

### Old Groups
* List of old groups (link to group home)

### Create Group
* Form for Group Name, Start Date, and place to add 6 member emails

### Group Home (PreLock)
* Group Name, start date and Group Owner at top
* List of the Beers you've added (with button to remove)
* Forms for Brewery and Beer with Add and Check Duplicate buttons
* Group Owner will have a manage group button

### Manage Group
* List of Users with Remove button
* Email form with a Add User button next to it
* Form to select a new start date
* Access to this page is not allowed PostLock

### Group Home (PostLock)
--------------------------
* Group Name, Start Date and Group Owner at the top
* List of all 24 Beers and who provided them

## Database Design

### User
* Email
    * Primary Key
* Password
    * Password will not be stored plain text, I need to do more research on proper design for user/password data
* First
    * Null allowed
* Last
    * Null allowed

### Group
* ID
    * Auto Incremented
    * Primary Key
* Name
* Start Date
* Creator
    * Foreign Key to User.Email

### GroupMembers
* GroupID
    * Foreign Key to Group.ID
* Email
    * Not a ForeignKey because could be non registered user (Could change)
* HasAccepted

### Beer
* Brewery
* Beer
* GroupID
    * Foreign Key to Group.ID
* AddingUser
    * Foreign Key to User.Email


## Group Locking
The items above talk about group locking. A group is locked once both the start date is passed, there are 6 participants
who have accepted, and all participants have entered 4 beers that they are bringing.

## Possible/Future Features
* A persistent chat on the Group Home (pre and post lock)
* Untappped integration for beer look up and rating display
* Activity feed on PostLock group home with user untapped checkins of the beers on the list
* Current Day tracker on PostLock Home
* Email notification about group invites
* Optional Email notifications about group activity (Event Begin, Failure to lock w/ reasons why, etc)
