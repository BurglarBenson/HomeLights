#!/usr/bin/python

import csv
import datetime
import os
import subprocess
import time


# **********************************************************************************************************************
#
# functions called in this script
#
# **********************************************************************************************************************


# checks if the ip address of the device is responding

def check_if_home(ip):

    if os.name == 'nt':

        ping = subprocess.Popen(["ping", "-n", "1", ip], stdout=subprocess.PIPE)  # windows

    else:

        ping = subprocess.Popen(["ping", "-c", "1", ip], stdout=subprocess.PIPE, shell=False)  # linux


    check = ping.communicate()[0]
    check = ping.returncode

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

def get_day(list_of_days):

    d_today = datetime.datetime.strptime(time.strftime("%d/%m/%y"), "%d/%m/%y").date()

    day_num = None

    for i in range(0, len(list_of_days)):  # this
        if d_today == list_of_days[i]:
            day_num = i
            break

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
    days = [None] * len(all_data)

    for i in range(0, len(all_data)):

        days[i] = datetime.datetime.strptime(all_data[i][0], "%d/%m/%y").date()

        sunrise[i] = datetime.datetime.strptime(all_data[i][1], "%H:%M:%S").time()
        sunset[i] = datetime.datetime.strptime(all_data[i][2], "%H:%M:%S").time()

    return days, sunrise, sunset


# **********************************************************************************************************************
#
# loop of the program
#
# **********************************************************************************************************************

ip_address = "192.168.1.177"  # phone ip address to check

sleepTime = 1  # time between end of one ping and the next (seconds)
absentTime = 20  # this is more how many times can it fail, quite a long time
absentCheck = 0  # initialise this at zero to begin with

dayList, sSet, sRise = rise_set_times()

run = True  # continually run this script

try:
    while run:

        residentHome = check_if_home(ip_address)

        if residentHome == 0:

            absentCheck = 0  # reset this back to zero

            print("Home")

            darkCheck = check_if_dark(sSet, sRise, get_day(dayList))

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
