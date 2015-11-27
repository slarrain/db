#DB DRIVER CLASS
#IMPLEMENT THESE FUNCTIONS
class client:
    def __init__(self):
        pass
    #open a connection to a psql database
    def openConnection(self):
        print "Opening a Connection"
        return True

    #Close any active connection(should be able to handle closing a closed conn)
    def closeConnection(self):
        print "Closing Connection"
        return True

    #Note that a client may be loaded multiple times. Only load once per client_id
    def loadClient(self, client_id, name, address1, address2, city, state, zip):
        return True

    #Load an employer.
    #Note that an employer may get loaded multiple times. only load once per employer_id
    def loadEmployer(self, employer_id, name, address1, address2, city, state, zip):
        return True

    #Loads a lobbyist. Creates a connection for a lobbyist an employer and client
    #Note that this can be called multiple times per lobbyist. Load one Lobbyist per lobbyist_id
    #Each connection/relationship should be recorded.
    def loadLobbyistAndCreateEmployerClientConnection(self, lobbyist_id, employer_id, client_id, lobbyist_salutation,lobbyist_first_name,lobbyist_last_name):
        return True

    #Insert an expenditure. IDs are ints. amount can be rounded to int.
    #Recipient is a string which can be limited to 250 characters
    def insertExpenditure(self, expenditure_id, lobbyist_id, action, amount, expenditure_date, purpose, recipient, client_id):
        return True

    #Return a record/tuple for expenditure if exists
    def readExpenditureById(self, expenditure_id):
        return True

    #Return all records/tuples for expenditures by a lobbyist_id if exists
    def readExpendituresByLobbyistId(self, lobbyist_id):
        return True

    #insert a compensation. IDs are ints, amount can be rounded to int.
    def insertCompensation(self, compensation_id, lobbyist_id, compensation_amount, client_id):
        return True

    #Return a record/tuple for compensation if exists
    def readCompensationById(self, compensation_id):
        return True

    #Return all records/tuples for compensations by a client_id if exists
    def readCompensationsByClientId(self, client_id):
        return True

    #Return all records/tuples for compensations by that are within the amounts (inclusive)
    def readCompensationsInBetween(self, compensation_amount_min,compensation_amount_max):
        return True

    #Insert a lobbying activity. action sought and department can be truncated to 250 characters
    def insertActivity(self, lobbying_activity_id, action_sought, deparment, client_id, lobbyist_id):
        return True

    #Read a lobbying activity by ID if exists
    def readActivityById(self, lobbying_activity_id):
        return True

    #Return the count of lobvying activity on behalf of a client. 0 if none exists
    def countActivityByClientId(self, client_id):
        return True
