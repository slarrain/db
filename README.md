# HW 5
This HW is due Thurs 12/10 at 11:59 AM (i.e. noon). Partners can only use late days based on the min of the group (ie I have 1 slack day left and Adam has 3, we can only use 1). HWs after 
Sunday will not be accepted. Please commit and push to your github.  When you are submitting your HW do the following

 - Create a tag `git tag -a hw5 -m "My HW5 Submssion - Aaron and Adam"` Don't forget to push.
 - Email Adam and myself your commit hash for the submitted version.


## To run
 - python driver.py

## Requirments
 - Install Python 2.7
 - Install PostgreSQL
 - Install python pandas
 - Install python hdrhistogram
 - Install python numpy
 - Install python to postgresql library

## Tasks

### Step 1
 - Look at the function calls in LobbyDBClient, design an E-R diagram to satisfy the data requirements.
 - Create the physical schema with a set of DDL statements in a file called createDB1.sql (make sure this file is what you use
   to create your database) *do not optimize the schema at all outside of primary keys*
 - Place both files in hwfiles directory.

### Step 2
 - Implement the functions in LobbyDBClient
 - You can disable operations for testing load operations only by setting DO_OPERATIONS = False in driver.py
 - Run the full database driver and save the output via python driver.py | tee hwfiles/out1.log

### Step 3
 - Optimize the database by adding indexes or other optimizations (don't worry about tuning dbms settings or isolation levels)
 - Create a new DDL file with the optimizations in hwfiles/createDB2.sql
 - Run the full database driver and save the output via python driver.py | tee hwfiles/out2.log
