import requests
import unittest
import json

import pyotp

url = "http://127.0.0.1:5000"
user = "dummy"
password = "dummy"


class TestAuthenticationAccess(unittest.TestCase):
    def test_a(self):
        print("Testing non 2fa authentication")
        # ===========================================================================
        print("Testing access to GET '/' endpoint")
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        # ===========================================================================
        print("Testing access to GET '/api/todo' endpoint")
        r = requests.get(url + "/api/todo")
        self.assertNotEqual(r.status_code, 200)
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
        r = requests.get(url + "/api/todo", cookies=cookies)
        self.assertEqual(r.status_code, 200)

    def test_b(self):
        print("Testing 2fa authentication")
        # ===========================================================================
        print("Testing access to GET '/login' endpoint")
        print("Trying to get access_token.")
        r = requests.get(url + "/login", auth=(user, password))
        self.assertEqual(r.status_code, 200)
        access_token = r.json()["access_token"]
        cookies = {"access_token": access_token}
        print(f"Received token '{access_token}'")
        # ===========================================================================
        print("Initialize 2fa setup.")
        r = requests.post(url + "/login/2fa/new", cookies=cookies)
        self.assertEqual(r.status_code, 200)
        token = r.json()["token"]
        self.assertTrue(len(token) >= 16)
        print(f"Totp secret: {token}")
        totp = pyotp.TOTP(token)
        # ===========================================================================
        print("Validating 2fa setup.")
        data = {"totp_token": totp.now()}
        r = requests.post(url + "/login/2fa/validate", data=json.dumps(data), cookies=cookies)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "success")
        # ===========================================================================
        print("Authenticating with 2fa")
        data = {"token_2fa": totp.now()}
        r = requests.get(url + "/login/2fa", data=json.dumps(data), cookies=cookies, auth=(user, password))
        self.assertEqual(r.status_code, 200)
        access_token = r.json()["access_token"]
        cookies = {"access_token": access_token}
        print(f"Received token '{access_token}'")
        # ===========================================================================
        print("Testing access to GET '/login/2fa/link' endpoint")
        r = requests.get(url + "/login/2fa/link", cookies=cookies)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(token in r.json()["message"])
