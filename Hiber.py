import time
import os
import datetime
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
time.sleep(300)
os.system("shutdown /h")

