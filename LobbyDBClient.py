import psycopg2

class client:
    def __init__(self):
        self.conn = None
        #self.cur = None
    #open a connection to a psql database
    def openConnection(self):
        conn_string = "host='localhost' dbname='lobbydb' user='postgres' password=''"
        print "Opening a Connection"
        try:
            self.conn = psycopg2.connect(conn_string)
            print "Connected"
            #self.cur = self.conn.cursor()
            #return True
        except:
            print "Connection Failed!"
            #return False

    #Close any active connection(should be able to handle closing a closed conn)
    def closeConnection(self):
        self.conn.close()
        print "Closing Connection"
        #return True

    #Note that a client may be loaded multiple times. Only load once per client_id. optional extra credit: update if value changes
    def loadClient(self, client_id, name, address1, address2, city, state, zip):
        q = """INSERT INTO client (client_id, name, address1, address2, city, state, zip)
            values (%s, %s, %s, %s, %s, %s, %s);"""
        p = (client_id, name, address1, address2, city, state, zip, )
        with self.conn.cursor() as cur:
            cur.execute(q, p)

    #Load an employer.
    #Note that an employer may get loaded multiple times. only load once per employer_id.  Only load once per client_id. optional extra credit: update if value changes
    def loadEmployer(self, employer_id, name, address1, address2, city, state, zip):
        q = '''INSERT INTO employer (employer_id, name, address1, address2, city, state, zip)
            values (%s, %s, %s, %s, %s, %s, %s);'''
        p = (employer_id, name, address1, address2, city, state, zip, )
        with self.conn.cursor() as cur:
            cur.execute(q, p))

    #Loads a lobbyist. Creates a connection for a lobbyist an employer and client
    #Note that this can be called multiple times per lobbyist. Load one Lobbyist per lobbyist_id.
    # Only load once per client_id. optional extra credit: update if value changes
    #Each connection/relationship should be recorded.
    def loadLobbyistAndCreateEmployerClientConnection(self, lobbyist_id, employer_id, client_id, lobbyist_salutation,lobbyist_first_name,lobbyist_last_name):
        return True

    #Insert an expenditure. IDs are ints. amount can be rounded to int.
    #Recipient is a string which can be limited to 250 characters
    def insertExpenditure(self, expenditure_id, lobbyist_id, action, amount, expenditure_date, purpose, recipient, client_id):
        q = '''INSERT INTO expenditure (expenditure_id, lobbyist_id, action, amount, expenditure_date, purpose, recipient, client_id)
            values (%s, %s, %s, %s, %s, %s, %s, %s);'''
        p = (expenditure_id, lobbyist_id, action, amount, expenditure_date, purpose, recipient, client_id,)
        with self.conn.cursor() as cur:
            cur.execute(q, p)

    #Return a record/tuple for expenditure if exists
    def readExpenditureById(self, expenditure_id):
        return True

    #Return all records/tuples for expenditures by a lobbyist_id if exists
    def readExpendituresByLobbyistId(self, lobbyist_id):
        q = '''SELECT * FROM expenditure WHERE LOBBYIST_ID = %s;'''
        p = (lobbyist_id,)
        with self.conn.cursor() as cur:
            cur.execute(q, p)

    #insert a compensation. IDs are ints, amount can be rounded to int.
    def insertCompensation(self, compensation_id, lobbyist_id, compensation_amount, client_id):
        return True

    #Return a record/tuple for compensation if exists
    def readCompensationById(self, compensation_id):
        q = '''SELECT * FROM compensation WHERE COMPENSATION_ID = %s;'''
        p = (compensation_id,)
        with self.conn.cursor() as cur:
            cur.execute(q, p)

    #Return all records/tuples for compensations by a client_id if exists
    def readCompensationsByClientId(self, client_id):
        return True

    #Return all records/tuples for compensations by that are within the amounts (inclusive)
    def readCompensationsInBetween(self, compensation_amount_min,compensation_amount_max):
        q = '''SELECT * FROM compensation WHERE COMPENSATION_AMOUNT >= %s and COMPENSATION_AMOUNT <= %s;'''
        p = (compensation_amount_min, compensation_amount_max,)
        with self.conn.cursor() as cur:
            cur.execute(q, p)

    #Insert a lobbying activity. action sought and department can be truncated to 250 characters
    def insertActivity(self, lobbying_activity_id, action_sought, deparment, client_id, lobbyist_id):
        return True

    #Read a lobbying activity by ID if exists
    def readActivityById(self, lobbying_activity_id):
        q = '''SELECT * FROM activity WHERE LOBBYING_ACTIVITY_ID = %s;'''
        p = (lobbying_activity_id,)
        with self.conn.cursor() as cur:
            cur.execute(q, p)

    #Return the count of lobvying activity on behalf of a client. 0 if none exists
    def countActivityByClientId(self, client_id):
        return True

    #Find the lobbyist (id,name) who has the most level of activity per dollar spent
    def findMostProductiveLobbyist(self):
        q = '''with temp_table as (SELECT LOBBYIST_ID,count(*)/sum(AMOUNT) as act_per_doll
            FROM activity a JOIN expenditures e on a.LOBBYIST_ID=e.LOBBYIST_ID and
            a.CLIENT_ID=e.CLIENT_ID
            GROUP BY LOBBYIST_ID)
            SELECT LOBBYIST_ID,LOBBYIST_FIRST_NAME,LOBBYIST_LAST_NAME FROM temp_table JOIN lobbyist
            on temp_table.LOBBYIST_ID=lobbyist.LOBBYIST_ID WHERE act_per_doll=max(act_per_doll);'''
        p = (lobbying_activity_id,)
        with self.conn.cursor() as cur:
            cur.execute(q, p)

    #Find the client(id) who spent more than the average per client, and received the lowest amount of activity per dollar spent
    def findLeastEfficientClient(self):
        return True
