#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
# from utilities import *
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import traceback, json, time, os, sys, pymongo
from Crypto import Random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.dont_write_bytecode = True

clientInstances = {}

profiles_root_dir = "./Profiles/"
default_profile_path = profiles_root_dir + "Default"
file_path = "./profiles.txt"
temp_file_path = "./profiles_temp.txt"
checking_url = "www.whatsapp.com"

chrome_options = Options()
chrome_options.add_argument("--headless")

if os.path.isdir(profiles_root_dir) == False:
    os.system("mkdir " + profiles_root_dir)

class WhatsAppWeb(WebSocket):
    client_remoteJid = None
    client_file = None
    client_tempfile = None
    def sendJSON(self, obj, tag):
        # print("sending " + json.dumps(obj))
        self.sendMessage(json.dumps(obj))

    def sendError(self, reason, tag):
        print("sending error: " + reason)
        self.sendJSON({"type": "error", "reason": reason}, "error")

    
    def appendToFile(self,receiverJid, message, tag):
        file = open(profiles_root_dir + "profiles_temp.txt", "w+")
        file.write(json.dumps(message) + "\n")
        
    def create_profile(self, url, profile_id):
        profile_name = str(profile_id)
        os.system("cp -r " + default_profile_path + " " + profiles_root_dir + profile_id)
        time.sleep(5)
        os.system("google-chrome " + url + " --user-data-dir=" + profiles_root_dir + profile_name + " --no-default-browser-check &")

    def update_file(self, mobile_no, profile_id, status):
        timestamp = int(time.time())
        if 'main' in clientInstances:
            clientInstances['main'].sendMessage(json.dumps([mobile_no, profile_id, status, timestamp]))
        if os.path.isfile(file_path) == True:
            file1 = open(file_path, "r+")
            file2 = open(temp_file_path, "w+")

            update = False

            for line in file1:
                profile_data = json.loads(line.replace("\n", ""))
                if mobile_no == profile_data[0] and profile_id == profile_data[1]:
                    update = True
                    file2.write(json.dumps([mobile_no, profile_id, status, timestamp]) + "\n")
                else:
                    file2.write(line)
            
            if update == False:
                file2.write(json.dumps([mobile_no, profile_id, status, timestamp]) + "\n")

            file1.close()
            file2.close()

            os.system("mv " + temp_file_path + " " + file_path)
        else:
            file1 = open(file_path, "w+")
            file1.write(json.dumps([mobile_no, profile_id, status, timestamp]) + "\n")
    
    def send_users(self):
        users = []
        file = open(file_path, "r")
        for line in file:
            users.append(json.loads(line.replace("\n", "")))
        self.sendMessage(json.dumps(users))

    def open_all_profiles(self, url):
        file = open(file_path, "r")
        for line in file:
            profile_id = json.loads(line.replace("\n", ""))[1]
            chrome_options.add_argument("--user-data-dir=" + profiles_root_dir + profile_id)
            chrome_options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(url)

            # os.system("timeout 1m google-chrome " + url + " --user-data-dir=" + profiles_root_dir + profile_id + " --no-first-run --no-default-browser-check &")
            
        


    def handleMessage(self):
        try:
            request = json.loads(self.data)
            if request[0] == "create_profile":
                self.create_profile(request[1], request[2])
            elif request[0] == "Presence":
                mobile_no = request[1]
                profile_id = request[2]
                status = request[3]
                self.update_file(mobile_no, profile_id, status)
            elif request[0] == "get_users":
                checking_url = request[1]
                clientInstances["main"] = self
                if request[2] == "1":
                    self.send_users()
                self.open_all_profiles(checking_url)
                
        except:
            print(traceback.format_exc())

    def handleConnected(self):
        self.sendJSON({"from": "backend", "type": "connected"}, "connected")
        # for client in self.server.connections.itervalues():
        #     print(client)
        print(self.address, "connected to backend")

    def handleClose(self):
        whatsapp.disconnect()
        print(self.address, "closed connection to backend")


server = SimpleWebSocketServer("", 9011, WhatsAppWeb)
print("whatsapp-web-backend listening on port 9011")
server.serveforever()
