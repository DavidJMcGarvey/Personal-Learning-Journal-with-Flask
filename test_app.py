"""Tests for Personal Journal Flask Web App"""

import unittest
import models


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.user = models.User.create(
            username='dave',
            email='dave@email.com',
            password='123'
        )

    def test_create_user(self):
        self.assertIs(self.user, models.User.create())
