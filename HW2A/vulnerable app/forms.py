#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField

class ping_form(FlaskForm):
    ip_addr = StringField('IP Address')