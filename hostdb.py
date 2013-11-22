#!/usr/bin/python
# standard Python library imports

# secondary Python library imports
# (should be in your distribution's repository)
import sqlite

# Implements a database of host and port information, with API calls for plugins
class HostDatabase:
    
   def __init__(self):
       self.db = self._create_database()

   def _create_database(self):
       """Private method: create an empty database"""
       
       self.db = sqlite3.connect(':memory:')
       self.cursor = self.db.cursor()
       self.cursor.executescript("""

           CREATE TABLE Hosts(
               id        INTEGER PRIMARY KEY,
               hostip    TEXT UNIQUE,
               hostname  TEXT,
               );
        
           CREATE TABLE Ports(
               id        INTEGER PRIMARY KEY,
               portnum   INTEGER CHECK (portnum>0 && portnum<65535),
               protocol  TEXT,
               state     TEXT,
               
               FOREIGN KEY (hostid) REFERENCES Hosts(id),
               );

           """)
           

   # ----------- API and Utility Methods ----------------------------------------------
   #
   # These methods are exposed to the plugins and may be overriden by them.
   #
   #-----------------------------------------------------------------------------------   

   def add_host(self, host_ip, host_name):
       """Database API:  Add a host to the database, where:
           - host_ip: a string containing the host's Internet Protocol (IP) number
           - host_name: the name associated with this host"""
           
        # not there already?  Then add it
       self.cursor.execute("INSERT INTO Hosts(hostip, hostname) VALUES (?, ?);", (hostip, hostname))
       
       pass
   
   def add_port(self, host_ip, port_number, port_protocol, service_name, status):
       """Database API:  Add port information for a given host to the database, where:
           - host_ip:  a string containing the host's Internet Protocol (IP) number
           - port_number:  a string containing the port number
           - port_protocol: one of "tcp", "udp"
           - service_name: name of the service or program responding to queries on this port
           - status: can be "Open", "Closed", or "Filered". """
       pass
   
   def get_host_portinfo(self, host_ip):
       """Database API:  Return all port information for the specified host, where:
           - host_ip: a string containing the host's Internet Protocol (IP) number           
           """
       pass
   
   def list_matching_ports(self, port_number, port_protocol, status="Open"):
       """Database API:  Return list of all hosts that have this port open, where:
           - port_number:  a string containing the port number
           - port_protocol: one of "tcp", "udp"
           - service_name: name of the service or program responding to queries on this port
           - status: optional.  Can be "Open", "Closed", or "Filered". """

       # fix this
       results = self.cursor.execute('
           SELECT *
           FROM Ports
           LEFT JOIN Hosts ON Hosts.ID=Ports.HostID
           
           WHERE Orders.ID = port_protocol
           WHERE status="open"
           WHERE port_protocol=port_protocol'
           )
           
        return results

    
# implement test routines here    
if __name__=='__main__':
    pass

           
