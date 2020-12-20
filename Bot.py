#state format:
#{
#    "jobs": [
#        {
#            "jobname": "<name>",
#            "stack": {
#                "task": "taskname",
#                "prev_task": {...}
#            }
#        }
#    ]
#}

import json
import os

class Bot:
    def __init__(self, cfg):
        self._state=self._default_state()
        self._filename=cfg["state_file_name"]
        try:
            self._load_state()
        except:
            print("fixing state file")
            self._dump_state()
        self._load_state()

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
        if msg[1]:
            self._dump_state()
        return msg

    def Dump(self):
        msg=""
        jobs=self._state["jobs"]
        for i in range(0, len(jobs)):
            j=jobs[i]
            msg+="stack "+ str(i) + ": " + j["jobname"] + "\n" + self._dump_stack(j["stack"], "    ")
        if msg == "":
            msg="empty stack"
        return msg

##################################################################
# private

    def _username(self, author):
        return  author.name + "#" + author.discriminator

# stack commands

    def _stack_new(self, arg, username):
        dsc=arg + " (by " + username + ")"
        self._state["jobs"].append({"jobname": dsc, "stack": None})
        return ("ack", True)
        
    def _stack_rm(self, arg, username):
        try:
            jn=int(arg.split()[0])
        except:
            return ("failed to parse stack number", False)
        if jn < 0 or jn >= len(self._state["jobs"]):
            return ("nack: invalid stack number", False)
        if self._state["jobs"][jn]["stack"] != None:
            return ("nack: stack is not empty", False)
        self._state["jobs"].pop(jn)
        return ("ack", True)

    def _stack_pop(self, arg, username):
        try:
            jn=int(arg.split()[0])
        except:
            return ("failed to parse stack number", False)
        if self._state["jobs"][jn]["stack"]:
            self._state["jobs"][jn]["stack"]=self._state["jobs"][jn]["stack"]["prev_task"]
            return ("ack", True)
        else:
            return ("nack: stack empty", False)

    def _stack_push(self, arg, username):
        words=arg.split()
        if len(words) < 2:
            return ("too little args. usage:\n" + self._stack_usage(), False)
        try:
            jn=int(words[0])
        except:
            return ("failed to parse stack number", False)
        if jn < 0 or jn > len(self._state["jobs"])-1:
            return ("invalid stack number", False)
        task=" ".join(words[1:])  + "(by " + username + ")"
        self._state["jobs"][jn]["stack"]={"task": task, "prev_task": self._state["jobs"][jn]["stack"]}
        return ("ack", True)

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

    def _dump_stack(self, stack, indent):
        if stack:
            return indent + stack["task"] + "\n" + self._dump_stack(stack["prev_task"], indent+"    ")
        else:
            return ""

    def _load_state(self):
        with open(self._filename, "r+") as read_file:
            self._state = json.load(read_file)

    def _dump_state(self):
        with open(self._filename, "w+") as write_file:
            json.dump(self._state, write_file)

    def _default_state(self):
        return {"jobs": []}