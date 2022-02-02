import subprocess
import sqlalchemy
import datetime


with open('instruction.txt') as lines:
    details= [line.strip() for line in lines]

conn=sqlalchemy.create_engine(details[0])      
cur = conn.cursor()
def db_create():
    cur1 = conn.cursor()
    cur1.execute('CREATE TABLE public.devicetest1 (device text NOT NULL,test text NOT NULL,status bpchar(10) NULL,api int4 NULL,datetime timestamp NULL)')
    conn.commit()
    cur1.close()


def basefun(db=False):
    if db:
        db_create()
    try:
        subprocess.check_call(f"{details[1]} -avd {device}_{api} -no-snapshot-save -memory 2048",shell=True,timeout=60)
    except subprocess.TimeoutExpired:
        subprocess.run(f"{details[1]} ./app/build/outputs/apk/debug/app-debug.apk; {details[2]} install ./app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk",shell=True)
    proc = subprocess.Popen(f"{details[2]} shell am instrument -w -m -e debug false -e class 'com.cyberxpert.android.app.bum.PhotoActivityTest3' com.cyberxpert.android.app.bum.test/androidx.test.runner.AndroidJUnitRunner", stdout=subprocess.PIPE, shell=True)
    output = proc.stdout.read()
    d=output.decode(encoding = 'ISO-8859-1').split('\n')
    if'FAILURES!!!' in d:
        print('true') 
        status = 'fail'
        cur.execute(f"insert into public.devicetest (device, test, status, api, datetime) values ('{device}','{test}','{status}','{api}','{datetime.datetime.now().strftime(format='%y-%m-%d %H:%M:%S')}' )")
        conn.commit()
        cur.close()
    subprocess.check_call(f"{details[2]} -s emulator-5554 emu kill",shell=True)
basefun(db=True)
