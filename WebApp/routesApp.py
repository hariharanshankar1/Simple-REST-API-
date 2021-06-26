"""
Python Flask Server
This server is implemented with three simple endpoints.
"""

from flask import request, json
from datetime import datetime
import flask
from collections import defaultdict

"""
Initializing the application called as app.
"""

app = flask.Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config["DEBUG"] = True
"""
There are some global variables used.
historyTransaction --- Array --- Stores the memory of every transaction ordered by Date and Time.  
historyAccount  --- Hashmap --- Stores the total balance for each payer.
sumPoints --- A variable to keep record or total money.
statusCode --- To represent status code for each response.
"""
historyTransactions = []
historyAccount = {}
sumPoints = 0
statusCode = 200
"""
toDatetime --- A function to convert the date time string into to datetime format.
"""


def toDatetime(date):
    today = datetime.today()
    return datetime.strptime(date + '2021', '%m/%d  %I%p%Y')


"""
SAVETRANSACTIONS
First Endpoint for the server. 
The purpose of this endpoint is mainly to 
save the transaction that is passed as a JSON arguments.
example request call --- requests.post('http://127.0.0.1:5000/api/savetransaction',
                                 json={"payer": "DANNON", "points": 10, "timestamp": "10/31 10AM"})
returns Valid transaction [status_code = 200]

Condition where it may throw error
1. Points should not be zero.
2. Points should not be a negative number at first, 
    because basically account can't be negative. 
3. When points is a negative number and when added 
    into account it sums to a negative number.
"""


@app.route('/api/savetransaction', methods=['POST'])
def savetransaction():
    req = request.json
    payer = str(req['payer'])
    points = int(req['points'])
    timestamp = toDatetime(req['timestamp'])
    global sumPoints
    global statusCode

    if points == 0:
        statusCode = 400
        return ("Invalid Transaction Record", int(statusCode))
    elif points < 0:
        if payer not in historyAccount:
            statusCode = 400
            return ("Invalid Transaction Record", int(statusCode))
        elif payer in historyAccount and (historyAccount[payer] - points < 0):
            statusCode = 400
            return ("Invalid Transaction Record", int(statusCode))
        elif payer in historyAccount and historyAccount[payer] - points > 0:
            historyAccount[payer] += points
            sumPoints += points
            historyTransactions.append([payer, points, timestamp])
    else:
        sumPoints += points
        historyTransactions.append([payer, points, timestamp])
        if payer in historyAccount:
            historyAccount[payer] += points
        else:
            historyAccount[payer] = points

    # Sorting the historytransaction based on date and time.

    historyTransactions.sort(key=lambda x: x[2], reverse=True)
    print(historyTransactions)
    return ("Valid Transaction.", int(statusCode))

"""
SPENDPOINTS
Second EndPoint of the server to get.
json input of points to spend. In return,
a response with list of payer and points  
deducted from their balance. 

example output: [{"payer": "DANNON", "points": -100}, {"payer": "UNILEVER", "points": -200}, {"payer": "MILLER COORS", "points": -4700}]

Condition when it may fail:
1. Spendpoints is greater than total available balance.
2. Spendpoints is a negative number because it not specified
    that points can recieved or credited to the account. 
"""


@app.route('/api/spendpoints', methods=['POST'])
def spendPoints():
    global sumPoints
    global statusCode
    historyDebit = defaultdict()

    req = request.json
    pointsRemaining = req['points']
    pointsDebited = 0
    pointsToDebit = pointsRemaining

    if sumPoints < pointsRemaining:
        statusCode = 400
        return ("Insufficient Balance to spend points", int(statusCode))
    elif pointsRemaining < 0:
        statusCode = 400
        return ("Invalid Request.", int(statusCode))
    else:
        while pointsDebited < pointsRemaining:
            transaction = historyTransactions.pop()
            if transaction[1] + pointsDebited < pointsRemaining:
                pointsDebited = transaction[1] + pointsDebited

                if transaction[0] in historyDebit:
                    historyDebit[transaction[0]] += transaction[1]
                else:
                    historyDebit[transaction[0]] = transaction[1]
            else:
                pointsDebited = pointsRemaining

                if transaction[0] in historyDebit:
                    historyDebit[transaction[0]] += pointsRemaining
                else:
                    historyDebit[transaction[0]] = pointsRemaining
            pointsRemaining = pointsToDebit - pointsDebited

    result = []
    for key, value in historyDebit.items():
        line = {'payer': key, 'points': -value}
        historyAccount[key] -= value
        result.append(line)

    return json.dumps(result)

"""
VIEWBALANCE
Third endpoint, it just displays the 
balance of each payer in the server.

exmaple output: {"DANNON": 1000, "MILLER COORS": 5300, "UNILEVER": 0}
"""
@app.route('/api/viewbalance', methods=['GET'])
def viewBalance():
    return json.dumps(historyAccount)


if __name__ == "__main__":
    app.run(debug=True)
