import requests
import unittest

url = "http://127.0.0.1:5000"
user = "dummy"
password = "dummy"


class TestAuthenticationAccess(unittest.TestCase):
    def test_start(self):
        # ===========================================================================
        print("Testing access to GET '/' endpoint")
        r = requests.get(url).status_code
        self.assertEqual(r, 200)
        # ===========================================================================
        print("Testing access to GET '/api/todo' endpoint")
        r = requests.get(url + "/api/todo").status_code
        self.assertNotEqual(r, 200)
        # ===========================================================================
        print("Testing access to GET '/login' endpoint")
        print("Trying to get access_token.")
        r = requests.get(url + "/login", auth=(user, password))
        self.assertEqual(r.status_code, 200)
        access_token = r.json()["access_token"]
        cookies = {"access_token": access_token}
        print(f"Received token '{access_token}'")
        # ===========================================================================
        print("Testing access to GET '/api/todo' endpoint")
        r = requests.get(url + "/api/todo", cookies=cookies).status_code
        self.assertEqual(r, 200)
