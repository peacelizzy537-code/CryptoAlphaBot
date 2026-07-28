import time
from datetime import datetime

# Write to a file to debug
with open('/tmp/debug.log', 'w') as f:
    f.write(f"Bot started at {datetime.now()}\n")

print("BOT IS RUNNING!")
print("Current time:", datetime.now())

counter = 0
while True:
    counter += 1
    print(f"[{datetime.now()}] Heartbeat #{counter}")
    time.sleep(10)
