#!/usr/bin/env python

import os
from apps import generate_app

app = generate_app(os.path.abspath('settings.prod.py'))
