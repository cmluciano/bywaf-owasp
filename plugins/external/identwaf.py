# identwaf:  wrapper around WafW00F, provides 'identwaf' command
#
# - Requires WafW00f.py in the same plugin directory
# - Additionally, wafw00f requires evillib.

options = {

   # name : (value, default_value, required, description)

   # native wafw00f options
   'TARGET_HOST': ('', '', 'yes', 'Target host on which to identify WAF; list of hosts separated by spaces'),
   'VERBOSE': ('', '1', 'no', 'Specify verbosity (1-3)'),
   'FIND_ALL': ('', 'yes', 'yes', 'Continue identifying WAFs after finding the first one'),
   'DISABLE_REDIRECT': ('', 'yes', 'yes', 'Do not follow redirections given by 3xx responses'),

   # bywaf options 
   'USE_HOSTDB': ('', 'yes', 'yes', 'Use the HostDB to store information about hosts'),

   # unused options
#   'LIST': ('', 'yes','yes', 'List all WAFs that we are able to detect'),   
#   'USE_XMLRPC': ('','yes', 'yes', 'Switch on the XML-RPC interface instead of CUI'),
#   'XMLRPC_PORT': ('', '8001', 'yes', 'Specify an alternative port to listen on, default 8001'),
#   'TARGET_PORT': ('', '', 'yes', 'Target port on which to identify WAF'),
#   'USE_SSL': ('', 'no', 'yes', 'Enable SSL for scanning this host'),
#   'HOSTFILE': ('', '', 'no', 'list of hosts to identify; specify one host:port per line'),
}



# if True, then plugin options will be simulated
SIMULATE_USER_INPUT = True
        
# idea: be able to specify TARGET_HOST on the bywaf command line; i.e. "identwaf TARGET_HOST=... TARGET_PORT=..."
# as well as through plugin options.  Options on the commandline override settings specified in the plugin options.
def do_identwaf(args):
    
    #params = args.split()

    # simulate user command-line settings
    if SIMULATE_USER_INPUT:
        app.set_option('TARGET_HOST', '1.1.1.1 2.2.2.2 3.3.3.3')
        app.set_option('VERBOSE', '3')
        app.set_option('DISABLE_REDIRECT', 'no')
        app.set_option('FIND_ALL', 'yes')
       
    # set up parameters for calling WafW00F
    params = 'wafw00f ' + ' '.join([
       '-' + 'v' * int(options['VERBOSE'][0]),  # interpret verbosity
         '--findall=' + options['FIND_ALL'][0],
         '--disableredict=' + options['DISABLE_REDIRECT'][0],
         '--xmlrpc=no',
         options['TARGET_HOST'][0],
         ])

    # run wafwoof
    try:
        import os.path
        import imp

        # load wafwoof and import it
        wafwoof_path = os.path.join(os.path.dirname(plugin_path), 'wafw00f.py')
        wafw00f_module = imp.load_source('wafw00f', wafwoof_path)
        print('executing {}'.format(params))
        
        # call its main with the parameters we set above
        wafw00f_module.main(params)
        
    except Exception as e:
        import traceback as t
        exc_msg = t.format_exc()
        print('could not load wafw000f: {}'.format(exc_msg))
        return        
