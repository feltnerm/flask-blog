#!/usr/bin/env python

import os
from apps import generate_app

config = os.path.abspath('settings.py')
app = generate_app(config)
app.run()
