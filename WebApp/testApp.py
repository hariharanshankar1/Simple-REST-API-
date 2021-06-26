"""
Test Server
Some test cases which includes some good/bad request.
"""
import unittest
from flask_api import status
import requests


class testApi(unittest.TestCase):

    """Test Case 1 - To check if first value is zero while saving a transaction.
                        ---> StatusCode = 400 BAD REQUEST"""
    def testInitialZeroValue(self):
        response = requests.post('http://127.0.0.1:5000/api/savetransaction',
                                 json={"payer": "DANNON", "points": 0, "timestamp": "10/31 10AM"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """Test Case 2 - To check if first value is negative while saving transaction.
                            ---> StatusCode = 400 BAD REQUEST"""
    def testInitialNegativeValue(self):
        response = requests.post('http://127.0.0.1:5000/api/savetransaction',
                                 json={"payer": "DEANS", "points": -10, "timestamp": "11/5 12AM"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """Test Case 3 - To check if first value is negative while spend points.
                            ---> StatusCode = 400 BAD REQUEST"""
    def testSpendPointsZero(self):
        response = requests.post('http://127.0.0.1:5000/api/spendpoints', json={"points": -10})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """Test Case 4 - Given Example
                            ---> StatusCode = 400 BAD REQUEST"""
    def testExampleGiven(self):
        response5 = requests.post('http://127.0.0.1:5000/api/savetransaction',
                                  json={"payer": "DANNON", "points": 1000, "timestamp": "11/2 2PM"})
        self.assertEqual(response5.status_code, status.HTTP_200_OK)

        response2 = requests.post('http://127.0.0.1:5000/api/savetransaction',
                                  json={"payer": "UNILEVER", "points": 200, "timestamp": "10/31 11AM"})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        response3 = requests.post('http://127.0.0.1:5000/api/savetransaction',
                                  json={"payer": "DANNON", "points": -200, "timestamp": "10/31 3PM"})
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

        response4 = requests.post('http://127.0.0.1:5000/api/savetransaction',
                                  json={"payer": "MILLER COORS", "points": 10000, "timestamp": "11/1 2PM"})
        self.assertEqual(response4.status_code, status.HTTP_200_OK)

        response1 = requests.post('http://127.0.0.1:5000/api/savetransaction',
                                 json= {"payer": "DANNON", "points": 300, "timestamp": "10/31 10AM"})
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response6 = requests.post('http://127.0.0.1:5000/api/spendpoints', json={"points": 5000})
        print(response6.content)
        self.assertEqual(response6.status_code, status.HTTP_200_OK)

        response7 = requests.get('http://127.0.0.1:5000/api/viewbalance')
        print(response7.content)
        self.assertEqual(response7.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    print('test start')
    unittest.main(exit=False)
    print('test end')