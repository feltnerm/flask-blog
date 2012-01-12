#!/usr/bin/env python

from experientiarum import generate_app
from flaskext.testing import TestCase

class ExperientiarumTest(TestCase):

    def create_app(self):
        app = generate_app('experientiarum.config.TestConfig')
        return app

    def setUp(self):
        ''' Set up a test database. '''
        pass

    def tearDown(self):
        ''' Tear down test database. '''
        pass
