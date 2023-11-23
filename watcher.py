"""Watch for a 42 correction slot. Author: tmarx."""

if (__name__ != "__main__"):
    exit(1)
from sys import platform
if platform == 'win32':
    from win10toast import ToastNotifier
elif platform == 'darwin':
    import pync
elif platform == "linux":
    import notify2
import time
import requests
import datetime
import pickle

# Time waited between every check, in seconds
WAIT_TIME = 15

def get_params():
    """Get the last params saved on the disk. Return None if no params saved."""
    try:
        with open("./params.pkl", "rb") as file:
            url, team_id, token, api, forktime = pickle.load(file)
            return (url, team_id, token, api, forktime)
    except:
        return (None, None, None, None)

def save_params(url, team_id, token, api, forktime):
    """Save params on the disk."""
    with open("./params.pkl", "wb+") as file:
        pickle.dump((url, team_id, token, api, forktime), file)

def notify(title, message):
    """Send a desktop notification."""
    if platform == 'darwin':
        pync.notify(message, title=title, contentImage="./logo.png", sound="default")
    elif platform == 'win32':
        toast = ToastNotifier()
        toast.show_toast(title, message, duration=0)
    elif platform == "linux":
        notify2.init("42 School Correction")
        n = notify2.Notification(title, message)
        n.show()

def get_slots(project_url, team_id, days_to_begin, days_to_watch):
    """Send a request to 42 intra."""
    today = datetime.date.today()
    start = today + datetime.timedelta(days=days_to_begin)
    end = start + datetime.timedelta(days=days_to_watch)
    print(f"Getting slots from {start} to {end}")
    request = requests.get(
        f"https://projects.intra.42.fr/projects/{project_url}/slots.json?team_id={team_id}&start={start}&end={end}",
        headers={
            "Host": "projects.intra.42.fr",
            "Cookie": f"_intra_42_session_production={token};"
        }
    )
    response = request.json()
    # print(response)
    if ("error" in response):
        print("Unable to connect, check the token!")
        exit(0)
    return response

# Do the callback if specified
def call_api(message):
    try:
        requests.get(api.format(message))
    except Exception as e:
        print(e)

def get_time(slot):
    # Récupération de l'heure de début
    start_datetime_str = slot[0]['start']
    start_datetime = datetime.datetime.fromisoformat(start_datetime_str[:-6])  # Conversion en objet datetime
    start_time = start_datetime.time()  # Récupération de l'heure
    return (start_time)

# Check if we previously saved params
previous_url, previous_team_id, previous_token, previous_api, previous_forktime = get_params()

url_placeholder = ""
team_id_placeholder = ""
token_placeholder = ""
api_placeholder = ""
forktime_placeholder_start = ""
forktime_placeholder_end = ""

if (not previous_url is None):
    url_placeholder = f" (default {previous_url})"
if (not previous_team_id is None):
    team_id_placeholder = f" (default {previous_team_id})"
if (not previous_token is None):
    token_placeholder = f" (default {previous_token})"
if (not previous_api is None):
    api_placeholder = f" (default {previous_api} or Ńone to del API)"
if (not previous_forktime is None):
    forktime_placeholder_start = f" (default {previous_forktime[0].strftime('%H:%M')})"
    forktime_placeholder_end = f" (default {previous_forktime[1].strftime('%H:%M')})"

# Get variables
print("Refer to ReadMe.md to help you find the following data.")

project_url = input(f"Project URL{url_placeholder}: ")
if (project_url == ""):
    project_url = previous_url

team_id = input(f"Team ID{team_id_placeholder}: ")
if (team_id == ""):
    team_id = previous_team_id

token = input(f"Session token{token_placeholder}: ")
if (token == ""):
    token = previous_token

api = input(f"API callback (optional){api_placeholder}: ")
if (api == ""):
    api = previous_api
elif api == "None":
    api = None
try:
    days_to_watch = int(input("Number of days you want to watch (default 1): "))
except:
    days_to_watch = 1

try:
    days_to_begin = int(input("Number of days to start (default 0): "))
except:
    days_to_begin = 0

start_time_str = input(f"Please enter the start time (in HH:MM format){forktime_placeholder_start}: ")
if start_time_str == "":
    start_time_str = previous_forktime[0].strftime('%H:%M')
end_time_str = input(f"Please enter the end time (in HH:MM format){forktime_placeholder_end}: ")
if end_time_str == "":
    end_time_str = previous_forktime[1].strftime('%H:%M')
# Convert the input strings to time objects
try:
    forktime = (datetime.datetime.strptime(start_time_str, "%H:%M").time(),
         datetime.datetime.strptime(end_time_str, "%H:%M").time())
except ValueError:
    print("Incorrect time format. Please make sure to use the HH:MM format.")
    # Handle the error or exit the program according to your needs
    forktime = (datetime.time(0,0), datetime.time(23,59)) 
save_params(project_url, team_id, token, api, forktime)

notify("Running", "You'll be notified when an open slot is found.")
if api:
    call_api("Starting 42 search slot correction for [" + project_url + "]")
while True:
    print("Checking...")
    slots = get_slots(project_url, team_id, days_to_begin, days_to_watch)
    if (len(slots) > 0):
        # forktime = (datetime.time(12,30), datetime.time(16,0)) 
        start_time = get_time(slots)
        print(f"Slot found at {start_time}")
        in_forktime = forktime[0] <= start_time <= forktime[1]
        if in_forktime:
            notify(f"Correction found!", "An open slot has been found for {project_url} at {start_time}")
            if api:
                call_api(f"42: Correction Found for {project_url} at {start_time}")
        else:
            print(f" is not between {forktime[0]} and {forktime[1]}")
    time.sleep(WAIT_TIME)
