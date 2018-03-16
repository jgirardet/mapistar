# -*- coding: utf-8 -*-
# Generated by Pony ORM 0.8-dev on 2018-03-16 18:04
from __future__ import unicode_literals

import datetime
from pony import orm

dependencies = []

def define_entities(db):
    class Patient(db.Entity):
        nom = orm.Required(str)
        prenom = orm.Required(str)
        ddn = orm.Required(datetime.date)

    class Bla(db.Entity):
        nom = orm.Required(str)
        prenom = orm.Required(str)
