import os
from State import State

class Bot:
    def __init__(self, cfg):
        self._state=State(cfg["state_file_name"])

##################################################################
# public

    def Handle(self, message):
        msg=(None, False)
        username=self._username(message.author)
        if message.content.startswith(".stack new"):
            msg=self._stack_new(message.content[10:], username)
        elif message.content.startswith(".stack rm"):
            msg=self._stack_rm(message.content[9:], username)
        elif message.content.startswith(".stack pop"):
            msg=self._stack_pop(message.content[10:], username)
        elif message.content.startswith(".stack push"):
            msg=self._stack_push(message.content[11:], username)
        elif message.content.startswith(".help"):
            msg=self._print_help()
        elif message.content.startswith(".state"):
            msg=(self.Dump(), False)
        return msg

    def Dump(self):
        return self._state.Dump()

##################################################################
# private

    def _username(self, author):
        return  author.name + "#" + author.discriminator

# stack commands

    def _stack_new(self, arg, username):
        return self._state.Stack_new(arg, username)

    def _stack_rm(self, arg, username):
        try:
            jn=int(arg.split()[0])
        except:
            return ("failed to parse stack number", False)
        return self._state.Stack_rm(jn, username)

    def _stack_pop(self, arg, username):
        try:
            jn=int(arg.split()[0])
        except:
            return ("failed to parse stack number", False)
        return self._state.Stack_pop(jn, username)

    def _stack_push(self, arg, username):
        words=arg.split()
        if len(words) < 2:
            return ("too little args. usage:\n" + self._stack_usage(), False)
        try:
            jn=int(words[0])
        except:
            return ("failed to parse stack number", False)
        return self._state.Stack_push(jn, words[1:], username)

# other
    
    def _print_help(self):
        return (
            (
                ".help - print this help.\n.state - print jobs\n" + 
                ".stack new <stack description> - start new stack\n.stack rm <stack number> - remove stack at given number\n" +
                ".stack push <stack number> <task description> - add task to stack\n.stack pop <stack number> - pop task from stack\n"
            )
            , False
        )    
