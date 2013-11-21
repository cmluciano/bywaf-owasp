import sqlite

class HostDatabase:
    
   def __init__(self):
       self.db = self._create_database()

   def _create_database(self):
       """Private method: create an empty database"""
       pass

   def add_host(self, host_ip, host_name):
       """Database API:  Add a host to the database, where:
           - host_ip: a string containing the host's Internet Protocol (IP) number
           - host_name: the name associated with this host"""
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
       """Database API:  Return all hosts who have this port open, where:
           - port_number:  a string containing the port number
           - port_protocol: one of "tcp", "udp"
           - service_name: name of the service or program responding to queries on this port
           - status: optional.  Can be "Open", "Closed", or "Filered". """

           
"""
       pass
   
