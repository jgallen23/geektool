#!/usr/bin/env python
from rtm import RTM
import sys
import os

token_path = os.path.expanduser("~/.geektool_rtm")

def read_token():
    if os.path.exists(token_path):
        f = open(token_path, 'r')
        token = f.read()
        f.close()
        return token
    return None

def write_token(token):
    f = open(token_path, 'w')
    f.write(token)
    f.close()

def main(args):
    secret = "7a69d867fcdc2f0d"
    api_key = "44c0313c5aa5c16cf47ee93b1c4595c7"
    token = read_token()

    rtm = RTM(api_key, secret, token)

    if token is None or rtm.auth.checkToken().stat != "ok":
        import webbrowser
        import time
        url = rtm.getAuthURL()
        print url
        webbrowser.open(url)
        time.sleep(15)
        write_token(rtm.getToken())


    search = args[0]
    tasks = rtm.tasks.getList(filter = search)
    print "RTM - %s" % (search)
    if hasattr(tasks.tasks, 'list'):
        lists = tasks.tasks.list if isinstance(tasks.tasks.list, list) else [tasks.tasks.list]
        for task_list in lists:
            for taskseries in task_list.taskseries:
                completed = False
                if isinstance(taskseries.task, list):
                    for task in taskseries.task:
                        if task.completed:
                            completed = True
                            break
                else:
                    completed = taskseries.task.completed
                if not completed:
                    print taskseries.name

if __name__ == "__main__": main(sys.argv[1:])
