import psycopg2
import sys

class client:
    def __init__(self):
        self.conn = None
        self.cur = None

    #open a connection to a psql database
    def openConnection(self):
        conn_string = "dbname='lobbydb' user='santiago' password=''"
        print "Opening a Connection"
        try:
            self.conn = psycopg2.connect(conn_string)
            print "Connected"
            self.cur = self.conn.cursor()
        except:
            print "Connection Failed!"
            sys.exit(1)


    #Close any active connection(should be able to handle closing a closed conn)
    def closeConnection(self):
        if self.conn.closed==0:
            self.cur.close()
            self.conn.close()
            print "Closing Connection"
        else:
            print "Connection already closed"

    def execute(self, q, p):
        try:
            self.cur.execute(q, p)
            self.conn.commit()
        except psycopg2.IntegrityError:
            self.conn.rollback()

    #Note that a client may be loaded multiple times. Only load once per client_id. optional extra credit: update if value changes
    def loadClient(self, client_id, name, address1, address2, city, state, zip):
        q = """INSERT INTO client values (%s, %s, %s, %s, %s, %s, %s);"""
        p = (client_id, name, address1, address2, city, state, zip)
        self.execute(q, p)

    #Load an employer.
    #Note that an employer may get loaded multiple times. only load once per employer_id.  Only load once per client_id. optional extra credit: update if value changes
    def loadEmployer(self, employer_id, name, address1, address2, city, state, zip):
        q = '''INSERT INTO employer values (%s, %s, %s, %s, %s, %s, %s);'''
        p = (employer_id, name, address1, address2, city, state, zip, )
        self.execute(q, p)

    #Loads a lobbyist. Creates a connection for a lobbyist an employer and client
    #Note that this can be called multiple times per lobbyist. Load one Lobbyist per lobbyist_id.
    # Only load once per client_id. optional extra credit: update if value changes
    #Each connection/relationship should be recorded.
    def loadLobbyistAndCreateEmployerClientConnection(self, lobbyist_id, employer_id, client_id, lobbyist_salutation,lobbyist_first_name,lobbyist_last_name):
        q = '''INSERT INTO lobbyist values (%s, %s, %s, %s)'''
        p = (lobbyist_id, lobbyist_salutation, lobbyist_first_name, lobbyist_last_name, )
        self.execute(q, p)

        q2 = '''INSERT INTO connection values (%s, %s, %s)'''
        p2 = (lobbyist_id, employer_id, client_id,)
        self.execute(q2, p2)

    #Insert an expenditure. IDs are ints. amount can be rounded to int.
    #Recipient is a string which can be limited to 250 characters
    def insertExpenditure(self, expenditure_id, lobbyist_id, action, amount, expenditure_date, purpose, recipient, client_id):
        q = '''INSERT INTO expenditures values (%s, %s, %s, %s, %s, %s, %s, %s);'''
        p = (expenditure_id, lobbyist_id, action, amount, expenditure_date, purpose, recipient, client_id,)
        self.execute(q, p)

    #Return a record/tuple for expenditure if exists
    def readExpenditureById(self, expenditure_id):
        q = '''SELECT * FROM expenditures WHERE expenditure_id = (%s);'''
        p = (expenditure_id,)
        self.execute(q, p)
        try:
            records = self.cur.fetchall()
            return records
        except:
            return False

    #Return all records/tuples for expenditures by a lobbyist_id if exists
    def readExpendituresByLobbyistId(self, lobbyist_id):
        q = '''SELECT * FROM expenditures WHERE LOBBYIST_ID = %s;'''
        p = (lobbyist_id,)
        self.execute(q, p)
        try:
            records = self.cur.fetchall()
            return records
        except:
            return False

    #insert a compensation. IDs are ints, amount can be rounded to int.
    def insertCompensation(self, compensation_id, lobbyist_id, compensation_amount, client_id):
        q = '''INSERT INTO compensation values (%s, %s, %s, %s);'''
        p = (compensation_id, lobbyist_id, (compensation_amount), client_id)
        self.execute(q, p)


    #Return a record/tuple for compensation if exists
    def readCompensationById(self, compensation_id):
        q = '''SELECT * FROM compensation WHERE COMPENSATION_ID = %s;'''
        p = (compensation_id,)
        self.execute(q, p)
        try:
            records = self.cur.fetchall()
            return records
        except:
            return False

    #Return all records/tuples for compensations by a client_id if exists
    def readCompensationsByClientId(self, client_id):
        q = '''SELECT * FROM compensation WHERE client_id = %s;'''
        p = (client_id,)
        self.execute(q, p)
        try:
            records = self.cur.fetchall()
            return records
        except:
            return False

    #Return all records/tuples for compensations by that are within the amounts (inclusive)
    def readCompensationsInBetween(self, compensation_amount_min,compensation_amount_max):
        q = '''SELECT * FROM compensation WHERE COMPENSATION_AMOUNT >= %s and COMPENSATION_AMOUNT <= %s;'''
        p = (compensation_amount_min, compensation_amount_max,)
        self.execute(q, p)
        try:
            records = self.cur.fetchall()
            return records
        except:
            return ()

    #Insert a lobbying activity. action sought and department can be truncated to 250 characters
    def insertActivity(self, lobbying_activity_id, action_sought, deparment, client_id, lobbyist_id):
        q = '''INSERT INTO activity values (%s, %s, %s, %s, %s);'''
        p = (lobbying_activity_id, action_sought, deparment, client_id, lobbyist_id,)
        self.execute(q, p)

    #Read a lobbying activity by ID if exists
    def readActivityById(self, lobbying_activity_id):
        q = '''SELECT * FROM activity WHERE LOBBYING_ACTIVITY_ID = %s;'''
        p = (lobbying_activity_id,)
        self.execute(q, p)
        # try:
        #     records = self.cur.fetchall()
        #     return records
        # except:
        #     return False

    #Return the count of lobvying activity on behalf of a client. 0 if none exists
    def countActivityByClientId(self, client_id):
        q = ''' SELECT COUNT (LOBBYING_ACTIVITY_ID)
                FROM activity
                WHERE client_id=(%s);'''
        p = (client_id,)
        self.execute(q, p)
        try:
            records = self.cur.fetchall()
            return records
        except:
            return 0

    #Find the lobbyist (id,name) who has the most level of activity per dollar spent
    def findMostProductiveLobbyist(self):
        q = '''with temp_table as (SELECT a.LOBBYIST_ID,count(*)/sum(AMOUNT) as act_per_doll
           FROM activity a JOIN expenditures e on a.LOBBYIST_ID=e.LOBBYIST_ID and
           a.CLIENT_ID=e.CLIENT_ID
           GROUP BY a.LOBBYIST_ID)
           SELECT lobbyist.LOBBYIST_ID,LOBBYIST_FIRST_NAME,LOBBYIST_LAST_NAME FROM temp_table JOIN lobbyist
           on temp_table.LOBBYIST_ID=lobbyist.LOBBYIST_ID ORDER BY act_per_doll DESC LIMIT 1;'''
        self.execute(q, ())
        # try:
        #     records = self.cur.fetchall()
        #     return records
        # except:
        #     print "Error. There should be one"

    #Find the client(id) who spent more than the average per client, and received the lowest amount of activity per dollar spent
    def findLeastEfficientClient(self):
        q = '''SELECT t1.CLIENT_ID, count_act/spent as ratio
               FROM (SELECT CLIENT_ID, SUM (AMOUNT) as spent
                   FROM expenditures
                   GROUP BY CLIENT_ID
                   HAVING sum(AMOUNT) > (SELECT AVG (AMOUNT) as expAvg FROM expenditures)) t1
               INNER JOIN (SELECT CLIENT_ID, COUNT(LOBBYING_ACTIVITY_ID) as count_act
                           FROM activity
                           GROUP BY CLIENT_ID) t2
               on t1.CLIENT_ID=t2.CLIENT_ID
               ORDER BY ratio ASC
               LIMIT 1;'''
        self.execute(q, ())
        # try:
            #records = self.cur.fetchall()
            #return records
        # except:
        #   print "Error. There should be one"
