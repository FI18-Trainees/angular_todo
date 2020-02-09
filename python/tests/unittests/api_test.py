import requests
import unittest
import os
import json

url = "http://127.0.0.1:5000"
user = "dummy"
password = "dummy"


def read_json(path):
    with open(path, 'r', encoding="utf-8") as fh:
        return json.load(fh)


class TestAPI(unittest.TestCase):
    def test_start(self):
        # ===========================================================================
        print("Trying to get access_token.")
        r = requests.get(url + "/login", auth=(user, password))
        self.assertEqual(r.status_code, 200)
        access_token = r.json()["access_token"]
        cookies = {"access_token": access_token}
        # ===========================================================================
        print("Testing POST '/api/todolist' endpoint")
        print("Testing generation with different inputs.")
        data = read_json(os.path.join("mock_jsons", "todolist_input_200.json"))
        expecting_length = len(data) + 1  # +1 for default list created by sql script.
        for d in data:
            print(f"Testing data: {d}")
            r = requests.post(url + "/api/todolist", cookies=cookies, data=json.dumps(d))
            self.assertEqual(r.status_code, 200)
        # ===========================================================================
        print("Testing POST '/api/todolist' endpoint")
        print("Testing generation with different inputs.")
        data = read_json(os.path.join("mock_jsons", "todolist_input_400.json"))
        for d in data:
            print(f"Testing data: {d}")
            r = requests.post(url + "/api/todolist", cookies=cookies, data=json.dumps(d))
            self.assertIn(r.status_code, [400, 500])
        # ===========================================================================
        print("Testing GET '/api/todolist' endpoint")
        r = requests.get(url + "/api/todolist", cookies=cookies)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json(), list)
        self.assertEqual(len(r.json()["data"]), expecting_length)
        # ===========================================================================
        print("Testing GET '/api/todolist?list_id=1' endpoint")
        r = requests.get(url + "/api/todolist?list_id=1", cookies=cookies)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json(), dict)

        # ===========================================================================
        print("Testing POST '/api/todo' endpoint")
        print("Testing generation with different inputs.")
        data = read_json(os.path.join("mock_jsons", "todo_input_200.json"))
        expecting_length = len(data)
        for d in data:
            print(f"Testing data: {d}")
            r = requests.post(url + "/api/todo", cookies=cookies, data=json.dumps(d))
            self.assertEqual(r.status_code, 200)
        # ===========================================================================
        print("Testing POST '/api/todo' endpoint")
        print("Testing generation with different inputs.")
        data = read_json(os.path.join("mock_jsons", "todo_input_400.json"))
        for d in data:
            print(f"Testing data: {d}")
            r = requests.post(url + "/api/todo", cookies=cookies, data=json.dumps(d))
            self.assertIn(r.status_code, [400, 500])
        # ===========================================================================
        print("Testing GET '/api/todo' endpoint")
        r = requests.get(url + "/api/todo", cookies=cookies)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json(), list)
        self.assertEqual(len(r.json()["data"]), expecting_length)
        # ===========================================================================
        print("Testing GET '/api/todo?list_id=1' endpoint")
        r = requests.get(url + "/api/todo?list_id=1", cookies=cookies)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json(), list)
        # ===========================================================================
        print("Testing GET '/api/todo?item_id=1' endpoint")
        r = requests.get(url + "/api/todo?list_id=1", cookies=cookies)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json(), dict)
