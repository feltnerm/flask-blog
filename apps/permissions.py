#!/usr/bin/env python

from flask.ext.principal import RoleNeed, Permission

admin = Permission(RoleNeed(2))
moderator = Permission(RoleNeed(1))
auth = Permission(RoleNeed(0))

null = Permission(RoleNeed(None))
