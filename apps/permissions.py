#!/usr/bin/env python

from flask.ext.principal import RoleNeed, Permission

admin = Permission(RoleNeed('admin'))
moderator = Permission(RoleNeed('moderator'))
auth = Permission(RoleNeed('authenticated'))

null = Permission(RoleNeed('null'))
