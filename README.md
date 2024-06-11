# DSU GenCyber Auto Elective Script

### I'm pretty much done developing this script for the GenCyber DSU camp. If I attend the camp in 2025, I will update it to be in a web portal.

What Does It Do?
  - This script allows the user to select their desired electives for the next elective phase in the Dakota State University GenCyber Camp. Then it automatically waits for the electives to open (usually either 7:30 AM OR 9:45 PM). At the exact elective time, it registers all the electives for the user, assuming the user is sleeping ;)

Why?
  - I was tired that all the electives would fill up immediately at 6:35-40 and I too wanted the best electives so I made this to combat that.

Prerequisites:

1. Go to https://go.gencyber.camp/login
2. Press "Remember Me"
3. Enter login credentials.
   3.5. Username and password should be information card given at the beginning of camp.
4. Log In!
5. CLOSE ALL GOOGLE CHROME BROWSER SESSIONS!

Info:

All google chrome browser sessions should be closed while the script is running. 
Laptop should not go to sleep while the script is running. 

Makeshift Installation:

1. Git clone or download: https://github.com/byrchbaker/DSU-GenCyber

2. Get-Item requirements.txt | Get-Content | % {$p= $_.split(); py -m pip install $p}

3. py main.py

4. Enjoy.

Intended Result:
![image](https://github.com/byrchbaker/DSU-GenCyber-Enroll/assets/62627217/2b30d646-7a35-4705-8e9e-f2e23b54eb47)





Copyright 2024 © Byrch Baker
