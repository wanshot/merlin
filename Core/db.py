# SQLAlchemy DB interface

# This file is part of Merlin.
 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

import sys
import sqlalchemy
if float(sqlalchemy.__version__[:3]) < 0.5:
    sys.exit("SQLAlchemy 0.5+ Required")
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, clear_mappers
import sqlalchemy.sql as SQL
import sqlalchemy.sql.functions
SQL.f = sys.modules['sqlalchemy.sql.functions']
from .variables import DBeng

engine = create_engine(DBeng)#, echo='debug')

Session = sessionmaker(bind=engine)

def reload_mappings():
    Maps.Base.metadata.clear()
    clear_mappers()
    reload(Maps)
    Maps.Base.metadata.bind = engine
    Maps.Base.metadata.create_all()
    Maps.Session = Session

import maps as Maps
reload_mappings()