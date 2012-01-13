#!/usr/bin/env python

import unittest

from experientiarum import generate_app
from experientiarum.extensions import db
from experientiarum.helpers import markdown, slugify, domain, gistcode, \
    code_highlight, code2html, ip2long, long2ip

class ExperientiarumTest(unittest.TestCase):

    def create_app(self):
        app = generate_app('experientiarum.config.TestConfig')
        return app

    def setUp(self):
        ''' Set up a test database.
        connect
        create everything '''
        app = self.create_app()
        app.init_db()
        
    def tearDown(self):
        ''' Tear down test database. 
        delete everything
        disconnect'''
        db.disconnect()

if __name__ == '__main__':
    unittest.main()