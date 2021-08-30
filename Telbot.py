import pyautogui
import sys, time
import os
import argparse
from datetime import datetime

class Bot:
    def __init__(self, group_file="Groups.txt", advert_link=""):
        self.position = pyautogui.position()
        self.picture_path = "./Images/"
        self.groups = self.get_groups(group_file)
        self.advert_link = advert_link
        self.log = open('log.txt','w')

    def log_(self, string):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.log.write(dt_string + ' : ' + string)

    def sleep(self, seconds):
        time.sleep(seconds)

    def reset_position(self):
        pyautogui.moveTo(100,100)

    def locate_position(self, element):
        position = pyautogui.locateCenterOnScreen(self.picture_path + element)
        if position == None:
            self.log_('Could not locate ' + element + ' on screen')
        return position

    def check_position(self, element):
        if self.position == self.locate_position(element):
            return True
        else:
            return False

    def move_to_position(self, element):
        if self.locate_position(element) != None:
            self.position = pyautogui.moveTo(self.locate_position(element))
            return True
        else:
            return False

    def click(self, element):
        self.sleep(1)
        if self.move_to_position(element):
            pyautogui.click()
            return True
        else:
            self.log_('Could not click ' + element)
            return False

    def write(self, text, element):
        if self.click(element):
            pyautogui.typewrite(text)
            self.sleep(1)
            pyautogui.typewrite('\n')
            return True
        else:
            self.log_('Could not write to ' + element)
            return False

    def send_link(self, link):
        self.click("Message_Board.png")
        for letter in link:
            if letter == '/':
                pyautogui.keyDown('shift')
                pyautogui.press(letter)
                pyautogui.keyUp('shift')
            else:
                pyautogui.press(letter)
        pyautogui.press('enter')

    def remove_advert_bar(self):
        self.click("Advert_Bar.png")

    def get_groups(self, group_file):
        arr = []
        with open(group_file) as groups:
            for line in groups:
                arr.append(line)
        return arr

    def search_group(self, group):
        if self.write(group,"Search_Bar.png"):
            return True
        else:
            self.log_('Could not search group ' + group)
            return False

    def clear_search(self):
        self.click("clear_search2.png")
        self.click("clear_search.png")

    def join_group(self, group):
        if self.click("Group_Bar.png"):
            return True
        else:
            self.log_('Could not join Group')
            return False

    def remove_no_privilege_bar(self):
        self.click("No_privilege_OK.png")

    def leave_group(self):
        if self.click("People.png") and self.click("Leave.png") and self.click("Confirm_Leave.png"):
            return True
        else:
            self.log_('Could not leave group')
            return False

    def advertise(self, time=None):
        if time != None:
            timeout_start = time.time()
            while time.time() < timeout_start + time*60:
                if self.locate_position("init.png"):
                    if self.locate_position("Advert_Bar.png"):
                        self.remove_advert_bar()
                    for group in self.groups:
                        self.advertise_group(group)
        else:
            while 1:
                if self.locate_position("init.png"):
                    if self.locate_position("Advert_Bar.png"):
                        self.remove_advert_bar()
                    for group in self.groups:
                        self.advertise_group(group)

    def advertise_group(self, group):
        self.search_group(group)
        self.join_group(group)
        self.send_link(self.advert_link)
        if self.locate_position("No_privilege_OK.png"):
            self.remove_no_privilege_bar()

def get_args():
    parser = argparse.ArgumentParser(description="Welcome to Telbot 1.0")
    parser.add_argument('-f',help="File with groups to advertise (default is Groups.txt)",metavar='File',default="Groups.txt")
    parser.add_argument('-t',help="Minutes until Telbot terminates (default is never)",metavar='Timeout',default=None)
    parser.add_argument('-l',help="Advertisement link (default is nothing)",metavar='Link',default="")
    args = parser.parse_args()
    return args.f,args.t,args.l

def run(delay):
    file, timeout, link = get_args()
    time.sleep(delay)
    bot = Bot(file, link)
    bot.advertise(timeout)

run(5)
