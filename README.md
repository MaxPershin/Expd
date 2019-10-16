# Avocado

Avocado is an App writen in Python3 using Kivy framework + ZBarCam functions + Firebase sync.

App can track shops expiry dates and notify if any off them have to be removed from shelves.

App has ability to track articles by its article number or EAN code which can be scanned using a smartphone camera.
Users can create a custom group to synchronize their database over internet (Firebase implementation).

Any article can be changed manually or deleted. Any info, including expiry dates can be manually managed.

There is currently Russian and English language settings in app (Minor stuff could be not translated yet).

You need to execute main.py in order to launch it on your PC (Python, Kivy and libs should be included)

App is buildable via buildozer, so you can build an APK and try it by yourself.
