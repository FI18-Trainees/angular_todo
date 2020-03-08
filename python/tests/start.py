import unittest
import time

from unittests import TestAPI as test_a
from unittests import TestAuthenticationAccess as test_z
# TODO: import new unittests in alphabetical order


if __name__ == '__main__':
    seconds = 10
    print(f"Waiting {seconds} seconds for server to start.")
    time.sleep(seconds)
    unittest.main()
