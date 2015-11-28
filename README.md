# HW 5

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
