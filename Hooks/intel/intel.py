# Intel

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

from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class intel(loadable):
    """View or set intel for a planet. Valid options: """
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = self.coordre
        self.usage += " x.y[.z] [option=value]+"
        self.options = ['alliance', 'nick', 'fakenick', 'defwhore', 'covop', 'scanner', 'dists', 'bg', 'gov', 'relay', 'reportchan', 'comment']
        self.__doc__ += ", ".join(self.options)
    
    @loadable.run_with_access(access.get('hc',0) | access.get('intel',access['member']))
    def execute(self, message, user, params):
        
        if params.group(3) is None:
            galaxy = M.DB.Maps.Galaxy.load(*params.group(1,2))
            if galaxy is None:
                message.alert("No galaxy with coords %s:%s" % params.group(1,2))
                return
            session = M.DB.Session()
            session.add(galaxy)
            reply = []
            for planet in galaxy.planets:
                if planet.intel is not None:
                    intel = "Information stored for %s:%s:%s -"% (planet.x, planet.y, planet.z,) +str(planet.intel) if str(planet.intel) else None
                    if intel:
                        reply.append(intel)
            if reply:
                message.reply("\n".join(reply))
            else:
                message.reply("No information stored for %s:%s" % (galaxy.x, galaxy.y,))
            session.close()
            return
        
        planet = M.DB.Maps.Planet.load(*params.group(1,2,3))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,2,3))
            return
        
        session = M.DB.Session()
        session.add(planet)
        if planet.intel is None:
            planet.intel = M.DB.Maps.Intel()
        
        params = self.split_opts(message.get_msg())
        for opt, val in params.items():
            if opt == "alliance":
                if val in self.nulls:
                    planet.intel.alliance = None
                    continue
                alliance = M.DB.Maps.Alliance.load(val)
                if alliance is None:
                    message.alert("No alliances match %s" % (val,))
                    continue
                planet.intel.alliance = alliance
            if (opt in self.options) and (val in self.nulls):
                setattr(planet.intel, opt, None)
                continue
            if opt in ("nick","fakenick","bg","gov","reportchan"):
                setattr(planet.intel, opt, val)
            if opt in ("defwhore","covop","scanner","relay"):
                if val in self.true:
                    setattr(planet.intel, opt, True)
                if val in self.false:
                    setattr(planet.intel, opt, False)
            if opt == "dists":
                try:
                    planet.intel.dists = int(val)
                except ValueError:
                    pass
            if opt == "comment":
                planet.intel.comment = message.get_msg().split("comment=")[1]
        session.commit()
        message.reply(("Information stored for %s:%s:%s -"+str(planet.intel) if str(planet.intel) else "No information stored for %s:%s:%s") % (planet.x, planet.y, planet.z,))
        session.close()
