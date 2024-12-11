ACCESS_KEY = ""
WORD_DISCOVERER = False


# --------------------------------------------
# Input Functionality
def sinput(ask: str, choices: list = None, valueType: type = None):
    """
    Function to handle user input with optional validation for choices and value type.

    Parameters:
    ask (str): The prompt to display to the user.
    choices (list): A list of valid choices the user can pick from. If provided, user input must match one of these choices.
    valueType (type): The expected type of the user input. If provided, user input must be of this type.

    Returns:
    The validated user input.
    """

    # Ensure all elements in choices are of the specified valueType
    if choices and valueType:
        for c in choices:
            if not isinstance(c, valueType):
                raise Exception("Invalid sinput call: not all elements in choices are of valueType")

    valid = False
    answer = None
    lowerChoices = [str(c).lower() for c in choices] if choices else None
    
    choices_str = {', '.join([str(c) for c in choices])} if choices else None
    while not valid:
        if choices:
            print(f"Valid choices: ({choices_str})")
        
        uncheckedAnswer = input(f"{ask}")

        # Validate the type of the input if valueType is specified
        if valueType:
            try:
                valueType(uncheckedAnswer)
            except ValueError:
                print(f"Invalid. Answer not valid type {valueType}")
                continue

        # Validate the input against the choices if choices are specified
        if choices:
            if uncheckedAnswer.lower() not in lowerChoices:
                print(f"Invalid. Answer not in choices: {choices_str}")
                continue
            answer = choices[lowerChoices.index(uncheckedAnswer.lower())]  # Retrieve the original case-sensitive choice
        else:
            answer = uncheckedAnswer

        valid = True

    return answer

# ------------------------------------------------------
# School compatibility functionality
def ran_in_school():
    import os
    username = os.getlogin()

    import sys
    sys.path.append(f'C:\\Users\\{username}\\AppData\\Roaming\\Python\\Python312\\site-packages')

def first_run():
    import pip
    
    def install(package):
        if hasattr(pip, 'main'):
            pip.main(['install', package])
        else:
            pip._internal.main(['install', package])
    
    install('requests')
    install('threading')
    install('customtkinter')

# ---------------------------------------------------
# Requests stuff
def me_request(requests, access_key : str):

    response = requests.get(
        url='https://user-info.app.senecalearning.com/api/user-info/me',
        headers={
            "accept":"*/*",
            "accept-language":"en-US,en;q=0.9",
            "access-key":access_key,
            "content-type":"application/json",
            "correlationid":"1733947412578::6ed963c8-b4f0-4f87-ae2f-b4c3a16c604e",
            "dnt":"1",
            "origin":"https://app.senecalearning.com",
            "priority":"u=1, i",
            "referer":"https://app.senecalearning.com/",
            "sec-ch-ua":"\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile":"?0",
            "sec-ch-ua-platform":"\"Windows\"",
            "sec-fetch-dest":"empty",
            "sec-fetch-mode":"cors",
            "sec-fetch-site":"same-site",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "user-region":"US",
            "x-amz-date":"20241211T200332Z"
        },
        verify=False
        
    )

    return response.json()

def generate_request(requests, access_key : str):
    response = requests.post(
        url="https://user-info.app.senecalearning.com/api/user-info/me/update",
        headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'access-key': access_key,
        'content-type': 'application/json',
        'correlationid': '1733840258171::56c4e997-4bc1-4730-ae06-4ba0f2b74075',
        'origin': 'https://app.senecalearning.com',
        'priority': 'u=1, i',
        'referer': 'https://app.senecalearning.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'user-region': 'GB',
        'x-amz-date': '20241210T141738Z',
        },

        json = {
            'displayName': '!generate',
        },
        verify=False
    )

    if WORD_DISCOVERER:
        words_discoverer(response.json()["displayName"])

    return response.json()

# ---------------------------------------------------
# Main stuff
def words_discoverer(name : str):
    words = name.split(" ")
    with open("wordlist1.txt", "a+") as f:
        if words[0] not in f.read():
            f.write(words[0] + "\n")
    with open("wordlist2.txt", "a+") as f:
        if words[1] not in f.read():
            f.write(words[1] + "\n")

def get_current_name(requests, access_key : str):
    return me_request(requests, access_key=access_key)["displayName"]

def ensure_access_key():
    global ACCESS_KEY
    import os

    def helpful():
        print("Could not find access_key.txt! Please paste access key inside.")
        print("Steps to finding access key:")
        print("1. Ensure you are logged into senecalearning")
        print("2. Open inspect element menu (f12)")
        print("3. Click requests")
        print("4. Do anything until it adds a new request to requests bar")
        print("5. Click on request then go to headers -> access_key -> copy as value")
        print("6. Paste the value into access_key.txt")
        print("Then rerun the program!")
        with open("access_key.txt", "w") as f:
            f.write("")

        exit()

    if not os.path.exists("access_key.txt"):
        helpful()
    else:
        with open("access_key.txt", "r", encoding="utf-8") as f:
            ACCESS_KEY = f.read()
            if ACCESS_KEY == "":
                helpful()


def main_program():
    global ACCESS_KEY
    import customtkinter
    import requests
    import threading
    import os
    class SenecaNamerApp(customtkinter.CTk):
        def __init__(self):
            self.get_settings()
            
            super().__init__()
            self.geometry("400x400")
            self.title("Seneca Namer")

            self.label_title = customtkinter.CTkLabel(self, text="Name")
            self.label_title.pack(pady=10)

            self.seneca_name = customtkinter.StringVar()
            self.seneca_name.set(get_current_name(requests, ACCESS_KEY))
            self.label_name = customtkinter.CTkLabel(self, textvariable=self.seneca_name, font=("Arial", 20), text_color="blue")
            self.label_name.pack(pady=10)

            self.status_var = customtkinter.StringVar()
            self.status_var.set("None")
            self.status_label = customtkinter.CTkLabel(self, textvariable=self.status_var, text_color="green")
            self.status_label.pack(pady=5)

            self.button_roll_new = customtkinter.CTkButton(self, text="Roll Once", command=self.roll_once)
            self.button_roll_new.pack(pady=20)
            self.rollers()
        
        def get_settings(self):
            self.settings = {
                "names": ["dark men"],
                "keywords": [],
                "banned_keywords": [],
                "banned_names": []
            }

            possible_settings = list(self.settings.keys())
            for setting in possible_settings:
                file = f"{setting}.txt"
                if not os.path.exists(file): continue
                with open(file, "r", encoding="utf-8") as f:
                    self.settings[setting] = self.settings[setting] + f.read().splitlines()


        def roll_once(self):
            self.seneca_name.set(generate_request(requests, ACCESS_KEY)["displayName"])

        def rollers(self):
            self.running = False

            def roll_until_thread():
                while self.running:
                    self.status_var.set("Rolling...")
                    name = generate_request(requests, ACCESS_KEY)["displayName"].lower()
                    self.seneca_name.set(name)
                    self.update()
                    if name in self.settings["names"]:
                        self.status_var.set("Name found")
                        self.update()
                        self.running = False
                        break
                    for keyword in self.settings["keywords"]:
                        if keyword in name:
                            self.status_var.set(f"Keyword found: {keyword}")
                            self.update()
                            self.running = False
                            break

            self.roll_thread = threading.Thread(target=roll_until_thread)

            def start_rolling():

                if not self.running:
                    self.running = True
                    self.roll_thread = threading.Thread(target=roll_until_thread)
                    self.roll_thread.start()

            def stop_rolling():
                self.running = False

            self.button_start_roll = customtkinter.CTkButton(self, text="Start Rolling", command=start_rolling)
            self.button_start_roll.pack(pady=5)

            self.button_stop_roll = customtkinter.CTkButton(self, text="Stop Rolling", command=stop_rolling)
            self.button_stop_roll.pack(pady=5)

    app = SenecaNamerApp()
    app.mainloop()

if __name__ == "__main__":
    firstrun = sinput("Is this the first time you are running this program? (y/n)", ['y', 'n'])
    if firstrun == "y":
        first_run()
        print("Now rerun this program.")
        exit()
    
    in_school = sinput("Are you running this program in school? (y/n)", ['y', 'n'])
    if in_school == "y":
        ran_in_school()

    ensure_access_key()

    from requests.packages import urllib3
    urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
    main_program()
    
