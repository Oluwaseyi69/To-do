import unittest

from app import User, signup
from flask import url_for


class TestTodo(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.app = None

    def setUp(self):
        self.user = User(username="", password="<PASSWORD>")
        self.new_password = "<PASSWORD>"
        self.app.testing = True

    def test_valid_signup(self):
        with self.app as client:
            response = client.post('/signup', data={'username': 'testuser', 'password': 'strongpassword',
                                                    'confirm_password': 'strongpassword'})
            self.assertEqual(response.status_code, 302)

    # def test_valid_signup(self):
    #     result = signup()
    #     self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
