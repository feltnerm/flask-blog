#!/usr/bin/env python

from flaskext.principal import RoleNeed, Permission

admin = Permission(RoleNeed('admin'))
auth = Permission(RoleNeed('authenticated'))

# this is assigned when you want to block a permission to all
# never assign this role to anyone !
null = Permission(RoleNeed('null'))