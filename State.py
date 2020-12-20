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

class State:
    def __init__(self, filename):
        self._state=self._default_state()
        self._filename=filename
        try:
            self._load_state()
        except:
            print("fixing state file")
            self._dump_state()
        self._load_state()

    def Dump(self):
        msg=""
        jobs=self._state["jobs"]
        for i in range(0, len(jobs)):
            j=jobs[i]
            msg+="stack "+ str(i) + ": " + j["jobname"] + "\n" + self._dump_stack(j["stack"], "    ")
        if msg == "":
            msg="empty stack"
        return msg

    def Stack_new(self, arg, username):
        dsc=arg + " (by " + username + ")"
        self._state["jobs"].append({"jobname": dsc, "stack": None})
        self._dump_state()
        return ("ack", True)

    def Stack_rm(self, jn, username):
        if jn < 0 or jn >= len(self._state["jobs"]):
            return ("nack: invalid stack number", False)
        if self._state["jobs"][jn]["stack"] != None:
            return ("nack: stack is not empty", False)
        self._state["jobs"].pop(jn)
        self._dump_state()
        return ("ack", True)

    def Stack_push(self, jn, msg, username):
        if jn < 0 or jn > len(self._state["jobs"])-1:
            return ("invalid stack number", False)
        task=" ".join(msg)  + " (by " + username + ")"
        self._state["jobs"][jn]["stack"]={"task": task, "prev_task": self._state["jobs"][jn]["stack"]}
        self._dump_state()
        return ("ack", True)

    def Stack_pop(self, jn, username):
        if self._state["jobs"][jn]["stack"]:
            self._state["jobs"][jn]["stack"]=self._state["jobs"][jn]["stack"]["prev_task"]
            self._dump_state()
            return ("ack", True)
        else:
            return ("nack: stack empty", False)

    def _default_state(self):
        return {"jobs": []}

    def _load_state(self):
        with open(self._filename, "r+") as read_file:
            self._state = json.load(read_file)

    def _dump_state(self):
        with open(self._filename, "w+") as write_file:
            json.dump(self._state, write_file)

    def _dump_stack(self, stack, indent):
        if stack:
            return indent + stack["task"] + "\n" + self._dump_stack(stack["prev_task"], indent+"    ")
        else:
            return ""

        