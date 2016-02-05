#!/usr/bin/python

import subprocess
import time
import datetime
import csv


# **********************************************************************************************************************
#
# functions called in this script
#
# **********************************************************************************************************************


# checks if the ip address of the device is responding

def check_if_home(ip):

    output = subprocess.Popen(["ping", "-c", "1", ip], stdout=subprocess.PIPE, shell=False)
    check = output.communicate()[0]
    check = output.returncode

    return check


# **********************************************************************************************************************


# turn the lights on

def lights_on():
    return


# **********************************************************************************************************************


# turn the lights off

def lights_off():
    return


# **********************************************************************************************************************


# get the day of the year - jan 1st is day zero
# note: this is probably wrong in leap years...

def get_day():

    day_num = datetime.datetime.now().timetuple().tm_yday

    return day_num


# **********************************************************************************************************************


# compares the current time to sunrise/sunset to determine if it is dark

def check_if_dark(s_up, s_down, day_n):

    now = datetime.datetime.now().time()

    if now < s_up[day_n - 1]:

        check = 1

    elif now > s_down[day_n - 1]:

        check = 1

    else:

        check = 0

    if check == 1:
        print('Dark outside')
    else:
        print('Light outside')

    return check  # returns a 1 if it is dark


# **********************************************************************************************************************


# reads data from a csv to get the sunrise and sunset times

def rise_set_times():

    light_file = open('SunriseTimesWorcester.csv', "rt")
    reader = csv.reader(light_file)

    all_data = list(reader)

    sunrise = [None] * len(all_data)
    sunset = [None] * len(all_data)

    for i in range(0, len(all_data)):

        sunrise[i] = datetime.datetime.strptime(all_data[i][1], "%H:%M:%S").time()
        sunset[i] = datetime.datetime.strptime(all_data[i][2], "%H:%M:%S").time()

    return sunrise, sunset


# **********************************************************************************************************************
#
# loop of the program
#
# **********************************************************************************************************************

ip_address = "192.168.1.177"  # phone ip address to check

sleepTime = 5  # time between end of one ping and the next (seconds)
absentTime = 20  # this is more how many times can it fail, quite a long time
absentCheck = 0  # initialise this at zero to begin with

sSet, sRise = rise_set_times()

run = True  # continually run this script

try:
    while run:

        residentHome = check_if_home(ip_address)

        if residentHome == 0:

            absentCheck = 0  # reset this back to zero

            print("Home")

            darkCheck = check_if_dark(sSet, sRise, get_day())

        else:

            if absentCheck > absentTime:

                print("Not home")

                lights_off()

                print("Lights turned off")

            else:

                absentCheck += 1  # add one each time until it reaches the threshold

                print("Grace period")

        print("*******************************************************************************************************")
        time.sleep(sleepTime)

except KeyboardInterrupt:
    print("Stopping python script")
