import requests
import unittest


class TestAPI(unittest.TestCase):
    def test_start(self):
        # ===========================================================================
        print("Testing '/' endpoint")
        r = requests.get("http://127.0.0.1:5000/").text
        self.assertEqual(r, "OK")
