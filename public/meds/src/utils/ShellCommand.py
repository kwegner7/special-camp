import shlex, subprocess, os

### instantiable classes
__all__ = ["ShellCommand"]

###############################################################################
# ShellCommand
###############################################################################
class ShellCommand:
    """
    Convenience class for executing shell commands.

    Attributes:
        text_of_command -- command ascii text
    """

    ### private data
    class Private:
        def __init__(self): pass
        text_of_command = None;

    ### constructor
    def __init__(self, command):
        self.private = self.Private();
        self.private.text_of_command = command

    ### method execute
    def execute(self):
        args = shlex.split(self.private.text_of_command)
        return_code = subprocess.call(args) 
        return return_code

    ### method check_execute
    def checkExecute(self):
        args = shlex.split(self.private.text_of_command)
        result = subprocess.check_output(args)
        os.wait()
        return result

    ### method redirect
    def redirect(self, to_file):
        args = shlex.split(self.private.text_of_command)
        result = subprocess.Popen(args, stdout=open(to_file, mode='wb'))
        os.wait()
        return result

