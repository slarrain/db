#DO NOT MODIFY THIS FILE
import LobbyDBClient
import pandas
from hdrh import histogram
from datetime import datetime
import random
import numpy
from multiprocessing import Process, Queue

LOADC = 'loadClient'
LOADL = 'loadLobbyist'
LOADE = 'loadEmp'

#The following parameters can be changed for TESTING only
NUM_PROCS = 4 #Amount of parallel processes to do read and write operations
LIMIT_OPS = None #Limit the number of operations
DO_LOAD = True #do the initial loading of clients, lobbyists, and employers
DO_OPERATIONS = True #do the operation phase of reading and writing
DO_ANALYZE = False #TBD

def runLobbyDB():
    dfs = loadDFs()
    procs = []
    dbClients = []
    if DO_LOAD:
        try:
            dbClient = LobbyDBClient.client()
            dbClient.openConnection()
            loadHists = loadInitialData(dfs, dbClient)
        finally:
            dbClient.closeConnection()

    if DO_OPERATIONS:
        try:
            opList = genOpList(dfs)
            if LIMIT_OPS:
                opList= opList[:LIMIT_OPS]
            splitOpList = chunkList(opList, NUM_PROCS)

            q = Queue()
            print "Starting %s processes to read and write lobby activity" %NUM_PROCS
            for i, ops in enumerate(splitOpList):

                _dbC = LobbyDBClient.client()
                _dbC.openConnection
                p = Process(target=runOperations, args=(dfs,_dbC,ops,q,i))
                p.start()
                procs.append(p)
                dbClients.append(_dbC)
            print "Waiting on %s processes to finish "%len(procs)
            for p in procs:
                p.join()
            print "Getting results"
            # get ops
            opHists = {}
            while not q.empty():
                _opHists = q.get()
                for key in _opHists.keys():
                    h = getHist()
                    if key in opHists:
                        #merge
                        opHists[key].add(h.decode(_opHists[key]))
                        pass
                    else:
                        opHists[key] = h.decode(_opHists[key])


            printStats(opHists,loadHists)
        finally:
            for _dbC in dbClients:
                _dbC.closeConnection()

        if DO_ANALYZE:
            try:
                dbClient.openConnection()
                analyzeHists = analyzeData(dfs, dbClient)
            finally:
                dbClient.closeConnection

def printStats(opHists,loadHists):
    print "Load Operation Times"
    for key in loadHists.keys():
        print key, loadHists[key].get_percentile_to_value_dict([50,95,99,100])
    print "Operation Times"
    for key in opHists.keys():
        print key, opHists[key].get_percentile_to_value_dict([50,95,99,100])
#from http://stackoverflow.com/questions/2130016/splitting-a-list-of-arbitrary-size-into-only-roughly-n-equal-parts
def chunkList(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0
  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg
  return out

def loadDFs():
    dfs = {}
    dfs['client'] = pandas.read_csv('data/Lobbyist_Data_-_Clients.csv')
    dfs['emp'] = pandas.read_csv('data/Lobbyist_Data_-_Employers.csv')
    dfs['lobbyist_emp_client'] = pandas.read_csv('data/Lobbyist_Data_-_Lobbyist__Employer__Client_Combinations.csv')
    dfs['lob_expend'] = pandas.read_csv('data/Lobbyist_Data_-_Expenditures_-_Large.csv')
    dfs['lob_expend']['AMOUNT'] = dfs['lob_expend']['AMOUNT'].map(lambda x: x.strip('$'))
    dfs['lob_comp'] = pandas.read_csv('data/Lobbyist_Data_-_Compensation.csv')
    dfs['lob_comp']['COMPENSATION_AMOUNT'] = dfs['lob_comp']['COMPENSATION_AMOUNT'].map(lambda x: x.strip('$'))
    dfs['lob_activity'] = pandas.read_csv('data/Lobbyist_Data_-_Lobbying_Activity.csv')
    return dfs

def getHist():
    return histogram.HdrHistogram(1,1000*60*60,2)

def genOpList(dfs):
    ops = []
    lobbyist_ids = dfs['lobbyist_emp_client'].LOBBYIST_ID.values
    client_ids = dfs['client'].CLIENT_ID.values
    #keys for expend
    exp_write_ids = dfs['lob_expend'].index.values
    exp_read_ids = numpy.random.choice(exp_write_ids, len(exp_write_ids)/3)
    exp_by_lobbyist = numpy.random.choice(lobbyist_ids, 400)
    #keys for comp
    lob_comp_ids = dfs['lob_comp'].index.values
    comp_read_ids = numpy.random.choice(lob_comp_ids, len(lob_comp_ids)/5)
    comp_by_client = numpy.random.choice(client_ids, 500)
    comp_amounts = numpy.random.choice(dfs['lob_comp'].COMPENSATION_AMOUNT.values,100)
    #keys for activity
    lob_act_ids = dfs['lob_activity'].index.values
    act_read_ids = numpy.random.choice(lob_act_ids, len(lob_act_ids)/2)
    act_client_ids = numpy.random.choice(dfs['lob_activity'].CLIENT_ID, 1000)

    ops.extend(('INSERT_EXPEND','lob_expend', x) for x in exp_write_ids )
    ops.extend(('READ_EXPEND_BY_ID','lob_expend', x) for x in exp_read_ids )
    ops.extend(('READ_EXPEND_BY_LOBBYIST_ID','lob_expend', x) for x in exp_by_lobbyist)
    ops.extend(('INSERT_COMP','lob_comp', x) for x in lob_comp_ids )
    ops.extend(('READ_COMP_BY_ID','lob_comp', x) for x in comp_read_ids )
    ops.extend(('READ_COMP_BY_CLIENT_ID','lob_comp', x) for x in comp_by_client )
    ops.extend(('READ_COMP_BY_GREATER_THAN_COMPENSATION','lob_comp', x) for x in comp_amounts )
    ops.extend(('INSERT_ACTIVITY','lob_activity', x) for x in lob_act_ids )
    ops.extend(('READ_ACTIVITY_BY_ID','lob_activity', x) for x in act_read_ids )
    ops.extend(('COUNT_ACTIVITY_BY_CLIENT_ID','lob_activity', x) for x in act_client_ids )

    random.shuffle(ops)
    return ops


def loadInitialData(dfs, dbClient):
    print "Loading Initial Data"
    start = datetime.now()
    hists = {}
    #load clients
    loadc= getHist()
    for i, c in  dfs['client'].iterrows():
        s = datetime.now()
        dbClient.loadClient(c['CLIENT_ID'], c['NAME'], c['ADDRESS_1'], c['ADDRESS_2'], c['CITY'], c['STATE'], c['ZIP'])
        e = datetime.now()
        time = e - s
        loadc.record_value(time.total_seconds() * 1000)
    hists[LOADC] = loadc


    #load employees
    loade = getHist()
    for i, r in  dfs['emp'].iterrows():
        s = datetime.now()
        dbClient.loadEmployer(r['EMPLOYER_ID'], r['NAME'], r['ADDRESS_1'], r['ADDRESS_2'], r['CITY'], r['STATE'], r['ZIP'])
        e = datetime.now()
        time = e - s
        loade.record_value(time.total_seconds() * 1000)
    hists[LOADE] = loade

    #load lobbyist and connections
    loadl = getHist()
    for i, r in  dfs['lobbyist_emp_client'].iterrows():
        s = datetime.now()
        dbClient.loadLobbyistAndCreateEmployerClientConnection(r['LOBBYIST_ID'], r['EMPLOYER_ID'], r['CLIENT_ID'], r['LOBBYIST_SALUTATION'],r['LOBBYIST_FIRST_NAME'],r['LOBBYIST_LAST_NAME'])
        e = datetime.now()
        time = e - s
        loade.record_value(time.total_seconds() * 1000)
    hists[LOADL] = loadl
    end = datetime.now()
    time = end - start
    print "Time to load base tables :%s (sec) " % time.total_seconds()
    return hists

def runOperations(dfs, dbClient, ops, q, i):
    print "Running Operations"

    hists = {}
    for o in ops:
        #print i,o
        op = o[0]
        if op not in hists:
            hists[op] = getHist()

        s = datetime.now()
        if op == 'INSERT_EXPEND':
            r = dfs[o[1]].ix[o[2]]
            dbClient.insertExpenditure(r['EXPENDITURE_ID'], r['LOBBYIST_ID'], r['ACTION'], r['AMOUNT'], r['EXPENDITURE_DATE'], r['PURPOSE'], r['RECIPIENT'], r['CLIENT_ID'])
        elif op == 'READ_EXPEND_BY_ID':
            dbClient.readExpenditureById(o[2])
        elif op == 'READ_EXPEND_BY_LOBBYIST_ID':
            dbClient.readExpendituresByLobbyistId(o[2])
        elif op == 'INSERT_COMP':
            r = dfs[o[1]].ix[o[2]]
            dbClient.insertCompensation(r['COMPENSATION_ID'], r['LOBBYIST_ID'], r['COMPENSATION_AMOUNT'], r['CLIENT_ID'])
        elif op == 'READ_COMP_BY_ID':
            dbClient.readCompensationById(o[2])
        elif op == 'READ_COMP_BY_CLIENT_ID':
            dbClient.readCompensationsByClientId(o[2])
        elif op == 'READ_COMP_BY_GREATER_THAN_COMPENSATION':
            dbClient.readCompensationsInBetween(o[2],float(o[2])+1000)
        elif op == 'INSERT_ACTIVITY':
            r = dfs[o[1]].ix[o[2]]
            dbClient.insertActivity(r['LOBBYING_ACTIVITY_ID'], r['ACTION_SOUGHT'], r['DEPARTMENT'], r['CLIENT_ID'], r['LOBBYIST_ID'])
        elif op == 'READ_ACTIVITY_BY_ID':
            dbClient.readActivityById(o[2])
        elif op == 'COUNT_ACTIVITY_BY_CLIENT_ID':
            dbClient.countActivityByClientId(o[2])
        else:
            print "Unknown operation:",o
            continue
        e = datetime.now()
        time = e - s
        hists[op].record_value(time.total_seconds() * 1000)
    enc_hists = {}
    for h in hists.keys():
        enc_hists[h] = hists[h].encode()
    q.put(enc_hists)

def analyzeData(dfs, dbClient):
    print "Analyzing Data"
    hists = {}
    #COMING IN A PATCH
    return hists

if __name__ == "__main__":
    runLobbyDB()
