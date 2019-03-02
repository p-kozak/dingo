import os
import time

cmdStash = "git stash"
cmdPull = "git pull"
cmdLaunch = "sudo python3 app.py"
os.system(cmdStash)
os.system(cmdPull)
time.sleep(15)
os.system(cmdLaunch)
