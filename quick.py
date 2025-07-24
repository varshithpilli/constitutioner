import subprocess
import time
msg = input("Commit message (no): ")

commands = [
    "pip freeze > requirements.txt",
    "git add .",
    f'git commit -m "{msg}"',
    "git push origin master",
]

for cmd in commands:
    subprocess.run(cmd, shell=True)
    time.sleep(3)