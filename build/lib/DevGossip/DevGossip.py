from random import randint
import json
from classes.classes import bcolors as bc
from pusher import Pusher
import pysher
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


def verify_username(username):
    username_list = []
    with open("users.txt", "r") as open_file:
        users_file = open_file.read()
    users_list = users_file.splitlines()  # split each lines of the file into a list

    for item in users_list:
        details = json.loads(item)
        username_list.append(details['username'])

    if username in username_list:
        return True
    else:
        return False


class DevGossip:

    chatroom = None
    user = None
    pusher = None
    client_pusher = None
    channel = None

    chatrooms = {'1': 'Office',
                 '2': 'Relationships',
                 '3': 'Sports',
                 '4': 'Movies',
                 '5': 'Music'
                 }
                 
    colors = [bc.LCYAN, bc.LGREEN, bc.YELLOW, bc.LYELLOW, bc.RED,
             bc.LRED, bc.LBLUE, bc.PINK, bc.LGREY]
    user_color = colors[randint(0, 9)]
    END = bc.ENDC

    def homepage(self):

        start_choice = input(f"1. Sign up\n2. Login\n3. Close App\n{bc.YELLOW}Type in option (1,2,3): {self.END}")
        if start_choice == "1":
            print("")
            self.signup()
        elif start_choice == "2":
            print("")
            app.login()
        elif start_choice == "3":
            print("")
        else:
            print(f"{bc.RED}Enter a valid option!{self.END}")
            print("")
            self.homepage()

    def signup(self):

        firstname = input("Enter your first name: ")
        lastname = input("Enter your last name: ")
        fullname = firstname + " " + lastname

        username = input("Enter a Username: ").lower()
        while True:
            if verify_username(username):
                print(f"{bc.RED}Username has been taken! Enter another.{self.END}")
                username = input("Enter a Username: ").lower()
            else:
                break

        password = input("Enter password: ")
        email = input("Enter email: ")

        user = {'username': username, 'password': password, 'email': email, 'fullname': fullname}
        with open("users.txt", 'a') as users_file:
            users_file.write(json.dumps(user))
            users_file.write("\n")
        self.login()

    def login(self):
        proceed = input(f'{bc.YELLOW}Enter "0" to go home, and "1" to proceed: {self.END}')
        if proceed == "0":
            print("")
            self.homepage()
        elif proceed == "1":
            print("")
            pass
        else:
            print(f"{bc.RED}Invalid response!{self.END}")
            print("")
            self.login()

        print("Login to your account")
        username = input("Enter Username: ").lower()
        password = input("Enter password: ")

        with open("users.txt", "r") as open_file:
            users_file = open_file.read()
        users_list = users_file.splitlines()  # split each lines of the file into a list

        new_user_list = [json.loads(user) for user in users_list]  # each item of the users_list is appended as a python
        # readable dictionary into new_user_list, new_user_list is now a list of dictionaries, where each dictionary
        # contains the details of a user as items

        logged = False
        counter = 1  # to represent the number of user(s) the for loop has checked
        for user in new_user_list:
            if username == user['username'] and password == user['password']:
                logged = True
                print(f"{bc.BOLD}Welcome!{self.END}")
                self.user = username
                print("")
                self.select_chatroom()

            if not logged and counter == len(new_user_list):
                print(f"{bc.RED}You are not a registered user\nSign up to create a free account{self.END}")
                print("")
                self.homepage()
            counter += 1  # increment

    def select_chatroom(self):
        print(f"Available chatrooms: ")

        for SN, room in self.chatrooms.items():
            print(f"{SN}. {room}")
        print(f"{bc.YELLOW}\n0. logout{self.END}")
        print("")

        chatroom = input(f"Select a chatroom (Type in option number): ")

        if chatroom == "0":
            self.login()

        elif chatroom in self.chatrooms:
            self.chatroom = self.chatrooms.get(chatroom)
            print(f"You joined {self.chatroom}")
            print(f'{bc.YELLOW}Type "EXIT" to leave room{self.END}')
            self.initiate_pusher()
        else:
            print(f"{bc.RED}chatroom does not exist!{self.END}")
            self.select_chatroom()

    def initiate_pusher(self):
        self.pusher = Pusher(app_id=os.getenv('PUSHER_APP_ID', None),
                             key=os.getenv('PUSHER_APP_KEY', None),
                             secret=os.getenv('PUSHER_APP_SECRET', None),
                             cluster=os.getenv('PUSHER_APP_CLUSTER', None))
        self.client_pusher = pysher.Pusher(key=os.getenv('PUSHER_APP_KEY', None),
                                           cluster=os.getenv('PUSHER_APP_CLUSTER', None))
        self.client_pusher.connection.bind('pusher:connection_established', self.connection_manager)
        self.client_pusher.connect()

    def connection_manager(self, data):
        self.channel = self.client_pusher.subscribe(self.chatroom)
        self.channel.bind(u'newmessage', self.pusher_response)

    def pusher_response(self, message):
        message = json.loads(message)
        if message['user'] != self.user:
            print(f"{self.user_color}{message['user']}: {message['message']}{self.END}")
            print(f"{self.user_color}{self.user}: {self.END}")

    def get_user_input(self):
        message = input(f"{self.user}: ")
        if message == "EXIT":
            self.select_chatroom()
        else:
            self.pusher.trigger(self.chatroom, u'newmessage', {'user': self.user,
                                 'message': message})
