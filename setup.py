import webbrowser
import os

def setupfunction():
    username = input("What is your twitch username: ")
    webbrowser.open("twitchtokengenerator.com")
    oauth = input("What is your oauth key: ")
    clienttoken = input("What is your client-token: ")
    webbrowser.open(f"twitch.tv/{username}")
    description = input("What is your channel desription: ")
    webbrowser.open("https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/")
    channelID = input("What is your channel ID: ")



    os.system('cls')
    webbrowser.open("twitch.tv/activate")
    GQLBYPASS = input("Message @fasshn on discord for your code: ")

    with open(".env", "w") as f:
        f.write(f"BOT_NICK={username} \n")
        f.write(f"TOKEN={oauth} \n")
        f.write(f"CLIENT_ID={clienttoken} \n")
        f.write(f"DESC={description} \n")
        f.write(f"CHANNELID={channelID} \n")
        f.write(f"GQL_BYPASS={GQLBYPASS} \n")
        f.write(f"GQL_CLIENT=ue6666qo983tsx6so1t0vnawi233wa \n")
        f.write(f"BOT_PREFIX=-")
        


if __name__ == "__main__":
    setupfunction()
