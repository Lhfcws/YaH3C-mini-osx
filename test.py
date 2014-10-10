def _stop():
    import os
    sysout = os.popen("ps -ef | grep 'yah3c.py' | awk '{split($0,a);print a[2];}'")
    for process_id in sysout:
        os.system("kill " + process_id)
        print("Kill YaH3C, process id is " + process_id)
    sysout.close()
try:
    _stop()
except Exception:
    print "Skip stopping yah3c."
finally:
    print "test end."