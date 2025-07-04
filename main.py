import os
import requests
import random
import time
import asyncio
from twitchio.ext import commands
import datetime
import webbrowser



BadgeR = False
NameR = True
PaintR = True
with open("config.txt") as f:
    config = f.readlines()
    BadgeRotate = config[0]
    NameRotate = config[1]
    PaintRotate = config[2]
    if BadgeRotate == "on":
        BadgeR = True
    if NameRotate == "on":
        print("name on")
        NameR = True
    else:
        print("name off")
    if PaintRotate == "on":
        PaintR == True

CurrentName = 0
CurrentBadge = 0
CurrentColor = 0

ViewerList = []
ViewerFile = open("viewlist.txt", "r")
ViewFile = ViewerFile.readlines()
for line in ViewFile:
    ViewerList.append(line.strip())

    print(f'added {line}')
print(ViewerList)
bot = commands.Bot(
    token=os.environ['TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=ViewerList,
)

badges = []
badgelist = open("badgelist.txt", "r")
badgelst = badgelist.readlines()
for line in badgelst:
    badges.append(line.strip())
badgelist.close()
print(badges)


Names = []
namelist = open("namelist.txt", "r")
namelst = namelist.readlines()
for line in namelst:
    print(line)
    Names.append(line.strip())
namelist.close()
print(Names)
print(f"names: {len(Names)}")


Colors = []
colorList = open("colorlist.txt", "r")
colorListR = colorList.readlines()
for line in colorListR:
    Colors.append(line.strip())
colorList.close()
print(f"Color: {colorList}")


url = "https://gql.twitch.tv/gql"
headers = {
    "Authorization": f"OAuth {os.environ['GQL_BYPASS']}",
    "Client-Id": f"{os.environ['GQL_CLIENT']}",
    "Content-Type": "application/json",
}


color_request_template = {
    "query": """
        mutation updateChatColor($input: UpdateChatColorInput!) {
            updateChatColor(input: $input) {
                user {
                    id
                    chatColor
                    __typename
                }
                __typename
            }
        }
    """,
    "variables": {
        "input": {
            "color": f"{Colors[CurrentColor]}"  # Change this to any valid HEX color (e.g., "#00FF00")
        }
    }
}

badge_request_template = {
    "query": """
        mutation selectGlobalBadge($input: SelectGlobalBadgeInput!) {
            selectGlobalBadge(input: $input) {
                __typename
            }
        }
    """,
    "variables": {
        "input": {
            "badgeSetID": "",
            "badgeSetVersion": "1"
        }
    }
}


url = "https://gql.twitch.tv/gql"
headers = {
    "Authorization": f"OAuth {os.environ['GQL_BYPASS']}",
    "Client-Id": f"{os.environ['GQL_CLIENT']}",
    "Content-Type": "application/json",
}

request_template = [{
    "operationName": "UpdateUserProfile",
    "variables": {
        "input": {
            "displayName": "",
            "description": f"{os.environ['DESC']}",
            "userID": f"{os.environ['CHANNELID']}"
        }
    },
    "extensions": {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "991718a69ef28e681c33f7e1b26cf4a33a2a100d0c7cf26fbff4e2c0a26d15f2"
        }
    }
}]





@bot.event()
async def event_message(ctx):
    author = ctx.author.name
    if author == os.environ['BOT_NICK']:
        print("Message typed")
        if BadgeR:
            select_global_badge()
        if NameR:
            select_global_name()
        if PaintR:
            update_chat_color()

def select_global_name():
    global CurrentName
    print("name thingy")

    # Wrap request in a list []
    print(f"Current Name: {Names[CurrentName]}")
    request_payload = [{
        "operationName": "UpdateUserProfile",
        "variables": {
            "input": {
                "displayName": Names[CurrentName],
                "description": f"{os.environ['DESC']}",
                "userID": f"{os.environ['CHANNELID']}"
            }
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "991718a69ef28e681c33f7e1b26cf4a33a2a100d0c7cf26fbff4e2c0a26d15f2"
            }
        }
    }]

    try:
        CurrentName = CurrentName + 1
        if CurrentName == len(Names) - 1:
            CurrentName = 0
        
        response = requests.post(url, json=request_payload, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        print(f"Name {Names[CurrentName]} selected successfully!")
        print(response.json())  # Debugging

    except requests.exceptions.RequestException as error:
        print(f"Error selecting name: {error}")
        time.sleep(5)  # Wait before retrying

def select_global_badge():
    global CurrentBadge
    badge_request_template["variables"]["input"]["badgeSetID"] = badges[CurrentBadge]
    
    try:
        CurrentBadge = (CurrentBadge + 1)
        if CurrentBadge > len(badges) - 1:
            CurrentBadge = 0
        response = requests.post(url, json=badge_request_template, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        print(f"Badge {badge_request_template['variables']['input']['badgeSetID']} selected successfully!")
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error selecting badge: {error}")
        raise

def update_chat_color():
    global CurrentColor
    selected_color = Colors[CurrentColor]
    color_request_template["variables"]["input"]["color"] = selected_color

    try:
        # Cycle to the next color
        CurrentColor = (CurrentColor + 1) % len(Colors)

        response = requests.post(url, json=color_request_template, headers=headers)
        response.raise_for_status()

        print(f"✅ Chat color changed to: {selected_color}")
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"❌ Error setting chat color: {error}")
        raise




if __name__ == "__main__":
    bot.run()
