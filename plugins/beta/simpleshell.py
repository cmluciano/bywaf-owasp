# exampleplugin.py: a model plugin implementing an array of simple shells for
# local and remote POSIX systems.  Users can open, close and select among local 
# and remote SSH shells.

print "loaded simple shell"

# required dictionary
# read when creating new shells
options = {
    # <name>    <value>    <default value>   <required>  <description>
    'RHOST':     ('',            '',         'yes',     'IP address of the remote host'),
    'PORT':      ('',            '22/tcp',   'no',      'Port/protocol of the remote host'),
    'CWD':       ('',            '',         'no',      'Current working directory to set on the remote host account'),
    'USERNAME':  ('',            '',         'yes',     'User name of remote host account'),
    'PASSWORD':  ('',            '',         'yes',     'User password of remote host account'),
    'TITLE':     ('',            '',         'no',      'Title of the new shell'),
    }

  
# abstract shell-like class
class SimpleShell:
    
    # open a new shell-like object, with current_working_directory defaulting to None
    def __init__(self, title=None, current_working_directory=None):
        self.cwd = current_working_directory
        self.title = ''
    
    def setcwd(self, newcwd):
        self.cwd = newcwd
    
    def getcwd(self):
        return self.cwd
    
    def send(self, text):
        pass
    
    def receive(self):
        pass

# FIXME: implement this    
class SimpleSSHShell(SimpleShell):

    def __init__(self, title, current_working_directory, remote_host, remote_port, username, password):
        #initialize parent(SimpleShell) in portable manner
        try:
            super().__init__(title,current_working_directory)
        except TypeError:
            print('python 3 convention failed, resorting to python 2.x')
            SimpleShell.__init__(self,title,current_working_directory)
        
        self.rhost = remote_host
        self.rport = remote_port.split('/')[0]
        self.protocol = remote_port.split('/')[1]
        self.username = username
        self.pw = password
        
        # fixme: implement the rest:  open an SSH connection, etc. 
        # Maybe use pexpect module?  Fabric?
        

# FIXME:  implement this        
class SimpleLocalShell(SimpleShell):
    pass


# a list of SimpleShell instances
shell_sessions = []

# a reference to an element in shell_sessions
current_shell_session = None
    
# utility function to set the prompt to reflect the current working directory  
def set_prompt():
    cwd = current_shell_session.getcwd()
    title = current_shell_session.title
    app.set_prompt('exampleshell[{}]: {}'.format(title, cwd))
    
def shell_input_handler(line):
    """simulate the system shell"""
    
    # insert code here to run a command through the open shell object, assumes
    try:
        response = current_shell_session.run(line)
        print(response)
        
    except TypeError: # shellobject==None
        print("no shells currently open")
        return
        
    print(output)    
    set_prompt()

    
def do_cd(line):
    """change the current working directory"""
    
    newcwd = line.split(0)
    
    try:
        current_shell_session.setcwd(newcwd)
        
    except TypeError: # shellobject==None
        print("no shells currently open")
        
    except IOError: # target dir not found
        print("target directory not found")

def do_cwd(line):
    if current_shell_session:
        print(current_shell_session.getcwd())
        
# FIXME:  Implement this
# note, this is a multi-level command
def do_shell(line):
    global shell_sessions
    global current_shell_session
    from os import getcwd
    from socket import gethostname
    from getpass import getuser
    from fabric.api import run,sudo
    
    """open, select and close multiple local and remote shells"""

    # subcommands to expose to the user:
    
    params = line.split()
    
    if 'new' in params:
        #create a new shell
        ssh_params = ['RHOST','PORT','USERNAME','PASSWORD']        
        for i in range(len(ssh_params)):
            try: 
                #try to get parameters from shell, we skip the -new- shell argument
                ssh_params[i] = params[i+1]      
            #the parameter was not defined, fill in from options
            except IndexError:
                #if no specific parameters exist in options, resort to default parameters
                ssh_params[i] = options[ssh_params[i]][1] if options[ssh_params[i]][0]=='' else options[ssh_params[i]][0]
        
        current_shell_session = SimpleSSHShell("{}@{} {}".format(getuser(),gethostname(),len(shell_sessions)),getcwd(),remote_host=ssh_params[0],remote_port=ssh_params[1],username=ssh_params[2],password=ssh_params[3])
        shell_sessions.append(current_shell_session)
        app.set_prompt(current_shell_session.title)
            
    elif 'local' in params:
        pass 
        #spawn local
    elif 'remote' in params:
        pass
        #exec remote cmd
    elif 'select' in params:
        if not params:
            print('no shells spawned')
        else:
            print ('Avalible Sessions:')
            print(' | '.join([session.title for session in shell_sessions]))
        #TODO if there is a numeric parameter in input, 
        #pick the shell with the matching shell id
        #select
    elif 'close' in params:
        pass
        #close
    else:
        print('select new | local | remote | select | close')

        
        
        
        
        
        
        
           
        # subcommands to expose to the user:
            
        # new       - creates a new shell, assigning it a numeric title if one is not provided
        #   local   
        #   remote  - takes optional remote host, remote port, username, 
        #             password (also settable through options{})
        # select    - takes shell title or number to switch focus to
        #              calls app.set_delegate_input_handler(shell_input_handler)
        #              calls set_prompt()
        # close     - takes shell title or number to switch focus to
        
def complete_shell(self,text,line,begin_idx,end_idx):
    pass

def do_back_to_bywaf(self):
    """cancel input delegation"""
    app.unset_delegate_input_handler()
    app.set_prompt(app.current_plugin_name)
    
    
def do_bw(line):
    """executes a command in bywalf"""
    # note: get completion to work for this.  Tried overriding 
    # Cmd.complete() to get past its reliance on
    # readline.get_line_buffer(), but things got hairy (and
    # overriding complete() is too much anyway)
       
    # Inject the rest of the command into the Bywaf command queue.    
    # what I really want is to have working tab completion for this.
    # note, this won't happen since delegate gets called regardless...fix this
    app.cmdqueue.append(line[3:]) # skip past the 'bw '
