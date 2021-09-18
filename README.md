# pizeroMotionDetector
a python script to use a PIR sensor and publish a message to a MQTT topic when triggered

I could have used `systemctl` to ensure this thing is always running, but I elected to just use crontab for it with this entry:
`@reboot python3 /home/pi/pirDetector.py > /home/pi/cronlog.out 2>&1`

When I connect to the device, I try to remember to delete the contents of /home/pi/cronlog.out to save some space and avoid a future problem.
