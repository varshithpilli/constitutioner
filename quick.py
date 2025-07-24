import subprocess
import time
msg = input("Commit message: ")

commands = [
    "pip freeze > requirements.txt",
    "git add .",
    f'git commit -m "{msg}"',
    "git push origin master",
]

for cmd in commands:
    time.sleep(3)
    subprocess.run(cmd, shell=True)