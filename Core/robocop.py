# This file is part of Merlin.
# Merlin is the Copyright (C)2008-2009 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

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
 
import socket
import time

from Core.config import Config

class server(object):
    # Robocop server
    sock = None
    socks = []
    clients = []
    
    def connect(self):
        # Configure socket
        port = Config.getint("Misc", "robocop")
        print "%s RoboCop... (%s)" % (time.asctime(), port,)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30)
        self.sock.bind(("127.0.0.1", port,))
        self.sock.listen(5)
        return self.sock
    
    def attach(self, sock=None, socks=[]):
        # Attach the sockets
        self.sock = sock or self.connect()
        self.socks = socks
        self.clients = map(client, socks)
        return self.sock, self.socks
    
    def extend(self, sock):
        # Attach the new client
        self.socks.append(sock)
        self.clients.append(client(sock))
    
    def remove(self, client):
        # Remove the new client
        self.socks.remove(client.sock)
        self.clients.remove(client)
    
    def disconnect(self, line):
        # Cleanly close sockets
        print "%s Resetting RoboCop... (%s)" % (time.asctime(),line,)
        self.close()
        self.sock = None
        return self.sock, self.socks
    
    def read(self):
        # Read from socket
        sock, addr = self.sock.accept()
        self.extend(sock)
        print "%s RoboCop CONNECT (%s)" % (time.asctime(),self.clients[-1].id(),)
    
    def fileno(self):
        # Return act like a file
        return self.sock.fileno()
    
    def close(self):
        # And again...
        return self.sock.close()
    
RoboCop = server()

CRLF = "\r\n"

class client(object):
    # Robocop client
    def __init__(self, sock):
        # Basic attach
        self.sock = sock
        self.file = self.sock.makefile('rb', 0)
    
    def id(self):
        return "%s/%s"%(self.sock.getpeername()[1],self.fileno(),)
    
    def disconnect(self):
        # Cleanly close sockets
        print "%s RoboCop DISCONNECT (%s)" % (time.asctime(),self.id(),)
        self.close()
        RoboCop.remove(self)
    
    def read(self):
        # Read from socket
        line = self.file.readline()
        if line:
            if line[-2:] == CRLF:
                line = line[:-2]
            if line[-1] in CRLF:
                line = line[:-1]
            print "%s RoboCop (%s) <<< %s" % (time.asctime(),self.id(),line,)
        else:
            self.disconnect()
    
    def fileno(self):
        # Return act like a file
        return self.sock.fileno()
    
    def close(self):
        # And again...
        return self.sock.close()
