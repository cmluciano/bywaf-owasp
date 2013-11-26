#!/usr/bin/env python2

# standard Python library imports

# secondary Python library imports
# (should be in your distribution's repository)
import sqlite3

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
               hostname  TEXT
               );
        
           CREATE TABLE Ports(
               id        INTEGER PRIMARY KEY,
               portnum   INTEGER CHECK (portnum>0 and portnum<65535),
               protocol  TEXT,
               svcname   TEXT,
               state     TEXT,
               hostip    TEXT,
               foreignid INTEGER,
               
               FOREIGN KEY (foreignid) REFERENCES Hosts(id)
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

       # note: FIXME - skip if this is already in the database
       self.cursor.execute("INSERT INTO Hosts(hostip, hostname) VALUES (?, ?);", (host_ip, host_name))
       

   def get_host_iplist(self):
       results = self.cursor.execute("SELECT hostip from Hosts")
       return results
       
       
   def get_host_id(self, host_ip):
       results = self.cursor.execute("SELECT id from Hosts WHERE hostip=?",[host_ip])
       return results[0]
  
   def add_port(self, portnum, port_protocol, service_name, state, hostip):
       """Database API:  Add port information for a given host to the database, where:
           - host_ip:  a string containing the host's Internet Protocol (IP) number
           - portnum:  a string containing the port number
           - protocol: one of "tcp", "udp"
           - service_name: name of the service or program responding to queries on this port
           - status: can be "Open", "Closed", or "Filered". """
           
       self.cursor.execute("INSERT INTO Ports(portnum, protocol, svcname, state, hostip) VALUES (?, ?, ?, ?, ?);", (portnum, port_protocol, service_name, state, hostip))

   
   def get_host_portinfo(self, host_ip):
       """Database API:  Return all port information for the specified host, where:
           - host_ip: a string containing the host's Internet Protocol (IP) number           
           """
       results = self.cursor.execute("SELECT * From Ports  WHERE Ports.hostip=?", [host_ip])
       return results
   
   
   def list_matching_ports(self, portnum, protocol="TCP", state="open"):
       """Database API:  Return list of all hosts that have this port open, where:
           - portnum:  a string containing the port number
           - protocol: one of "tcp", "udp"
           - service_name: name of the service or program responding to queries on this port
           - status: optional.  Can be "Open", "Closed", or "Filered". """
           
       results = self.cursor.execute("SELECT hostip,portnum,protocol,state FROM Ports WHERE portnum=? AND state=?", [portnum, state])
       return results
           


   
# loads /etc/services and returns dictionary of "ip/port":servicename
def load_service_defs(fname):
    services = parse_service_defs(open(fname).readlines())
    return services

# feed it lines of services definition (like from /etc/services) and it will return a
# dictionary of "ip/port":servicename
def parse_service_defs(lines):
    services = {}
    for _line in lines:
       line = _line.strip()
       if line == '': continue
       if line[0]=='#': continue
       portAndType = line.split()[1]
       serviceName = line.split()[0]
       services[portAndType] = serviceName

    return services



# implement test routines here    
if __name__=='__main__':
    
    db = HostDatabase()
    servicedefs = load_service_defs('/etc/services')
    

    port_protocol = "TCP"    

    # create some example hosts and ports
    IP='1.1.1.1'
    HOSTNAME='www.test123.com'
    db.add_host(host_ip=IP, host_name=HOSTNAME)
    for portnum in range(20, 100):
       try:
           # note: FIXME - skip if this is already in the database
           service_name = servicedefs[portnum]
       except Exception:
           service_name  = "????"
       db.add_port(portnum=str(portnum), port_protocol="TCP", service_name=service_name, state="open", hostip=IP)       

    IP='2.2.2.2'
    HOSTNAME='www.testABC.com'
    db.add_host(host_ip=IP, host_name=HOSTNAME)    
    for portnum in range(10, 30):
       try:
           # note: FIXME - skip if this is already in the database
           service_name = servicedefs[portnum]
       except Exception:
           service_name  = "????"
       db.add_port(portnum=str(portnum), port_protocol="TCP", service_name=service_name, state="open", hostip=IP)

        
    # sift database for all open port 25/TCP
    ports = db.list_matching_ports("25", protocol="TCP", state="open")
    print 'ports is', ports
    for p in ports: 
        print p
