# make absolutely sure to run this with 'python3' and NOT 'python'!!!!!
import RPi.GPIO as GPIO
import time
import socket
import paho.mqtt.client as mqtt

motionCtr = 1

def motion_detected(channel):
        global motionCtr
        print("Motion Detected [", motionCtr, "]")
        # Publish the "ON" message to the topic that
        # the Sonoff S31 plugin is listening on
        mqttClient.publish(mqttTopic, "ON")
        motionCtr += 1

print("sleeping to allow for startup / reboot operations")
time.sleep(30)

#setup MQTT client connection
mqttBrokerAddr = "192.168.1.176"
mqttBrokerPort = 1883
mqttUser = # provide your mqtt user id here
mqttPass = # provide your mqtt password here
mqttTopic = # provide the name of the mqtt topic here
mqttClient = mqtt.Client("MotionDetector")
mqttClient.username_pw_set(mqttUser, mqttPass)
mqttClient.connect(mqttBrokerAddr, mqttBrokerPort)

# setup GPIO wiring for PIR sensor with call back for handling
# the pin rising. We don't really care if it's RISING or
# FALLING, just that it's changing which means that motion has
# been detected. BCM pin #7 is the 26th GPIO pin on the RPi Zero
GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Define the method to callback when the pin goes RISING and
# wait 250ms before possibly calling it again; the PIR has
# delay settings on it, but they're pretty inconsistent.
GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected, bouncetime=250)

try:
        print("PIR module test -- Ctrl-C to quit")
        time.sleep(2)
        print("Ready")

        # call loop_forever() last; it's a blocking operation, so it has to be last
        mqttClient.loop_forever()

except KeyboardInterrupt:
        print("quitting")
        GPIO.cleanup()
        mqttClient.loop_stop()
        mqttClient.disconnect()
