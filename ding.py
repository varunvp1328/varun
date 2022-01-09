import subprocess import psycopg2 conn = psycopg2.connect( host="localhost", database="postgres", user="postgres", password="1234")

cur = conn.cursor() def db_create(): cur1 = conn.cursor() cur1.execute('CREATE TABLE public.devicetest1 (device text NOT NULL,test text NOT NULL,status bpchar(10) NULL,api int4 NULL,datetime timestamp NULL)') conn.commit() cur1.close()

def vet(db=False): if db: db_create()

path = input('path')

try:
    subprocess.check_call(f"/home/{path}/Android/Sdk/emulator/emulator -avd {device}_{api} -no-snapshot-save -memory 2048",shell=True,timeout=60)
except subprocess.TimeoutExpired:
    subprocess.run(f"/home/{path}/Android/Sdk/platform-tools/adb install ./app/build/outputs/apk/debug/app-debug.apk; /home/{path}/Android/Sdk/platform-tools/adb install ./app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk",shell=True)
proc = subprocess.Popen(f"/home/{path}/Android/Sdk/platform-tools/adb shell am instrument -w -m -e debug false -e class 'com.cyberxpert.android.app.bum.PhotoActivityTest3' com.cyberxpert.android.app.bum.test/androidx.test.runner.AndroidJUnitRunner", stdout=subprocess.PIPE, shell=True)
output = proc.stdout.read()
d=output.decode(encoding = 'ISO-8859-1').split('\n')
if'FAILURES!!!' in d:
    print('true') 
    status = 'fail'
    cur.execute(f"insert into public.devicetest (device, test, status, api, datetime) values ('{device}','{test}','{status}','{api}','02/01/2022' )")
    conn.commit()
    cur.close()
subprocess.check_call(f"/home/{path}/Android/Sdk/platform-tools/adb -s emulator-5554 emu kill",shell=True)
vet(db=True)
