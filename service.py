from jnius import autoclass, cast
from time import sleep

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)

Context = autoclass('android.content.Context')
UsageStatsManager = autoclass('android.app.usage.UsageStatsManager')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
context = PythonActivity.mActivity.getApplicationContext()

while True:
    print('service running...')
    sleep(5)


