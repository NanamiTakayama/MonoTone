import sys,os
sys.path.append('/home/pi/')

from pi import aieye

print("__started__")

a = "ok"
i = 0
while a == 'ok':
    print("__loopstarted__")
    print("[{0}]times is ok".format(i))
    test = aieye.shoot()
    i = i + 1
