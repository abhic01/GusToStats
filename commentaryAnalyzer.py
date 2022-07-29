from pytube import YouTube
import speech_recognition as sr, re, requests, os.path, urllib.parse, urllib.request
from bs4 import BeautifulSoup

# Function to check if a particular game took place 
def checkGame(year : str, home_team : str, away_team : str) -> bool : 
    url = f"https://en.wikipedia.org/wiki/{year}_{teams[home_team]}_{home_team.lower().capitalize()}_season#Game_summaries" # Wiki contains a list of all games played by each team based on the year
    response = requests.get(url)
    return f"vs. {teams[away_team]} {away_team.lower().capitalize()}" in response.text

# Variable setup
teams = {"CARDINALS" : "Arizona", "FALCONS" : "Atlanta", "PANTHERS" : "Carolina", "BEARS" : "Chicago", "COWBOYS" : "Dallas", "LIONS" : "Detriot", 
        "PACKERS" : "Green Bay", "RAMS" : "Los Angeles", "VIKINGS" : "Minnesota", "SAINTS" : "New Orleans", "GIANTS" : "New York", "EAGLES" : "Philadelphia",
        "49ERS" : "San Francisco", "SEAHAWKS" : "Seattle", "BUCCANEERS" : "Tampa Bay", "COMMANDERS" : "Washington", "REDSKINS" : "Washington", 
        "RAVENS" : "Baltimore", "BILLS" : "Buffalo", "BENGALS" : "Cincinnati", "BROWNS" : "Cleveland", "BRONCOS" : "Denver", "TEXANS" : "Houston",
        "COLTS" : "Indianapolis", "JAGUARS" : "Jacksonville", "CHIEFS" : "Kansas City", "RAIDERS" : "Oakland", "DOLPHINS" : "Miami", "CHARGERS" : "Los Angeles", 
        "PATRIOTS" : "New England", "STEELERS" : "Pittsburgh", "TITANS" : "Tennessee"}

# Setting up the game and teams that played
game = input("Please enter the NFL game (post 2017) you would like to analyze in the format {Away Team} vs. {Home Team} {Year}\n").upper() # Getting game and teams
game_list = game.split()
year = game_list[3]
away_team = game_list[0]
home_team = game_list[2]
if not checkGame(year, home_team, away_team):
    print("The game you entered does not exist. Please try again.")
    exit(0)
print("The game was found. Moving on.....")

# Importing audio from a YouTube video of a game that we want to make stats for
if not os.path.exists(f"./audio/{game}"):
    print(f"Importing game commentary for: {game}.....")
    query = urllib.parse.urlencode({"search_query": game})
    url = urllib.request.urlopen("https://www.youtube.com/results?" + query) # URL of the most relevant video on YT search
    search_results = re.findall(r"watch\?v=(\S{11})", url.read().decode())
    video_url = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    print(f"Link to the most relevant YT video is: {video_url} .....")

    # Downloading the audio of the YT video as an mp4 file
    try:
        video = YouTube(url)
        video_audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
        video_audio.download(f"./audio/{game}")
        print("Audio download completed.....")
    except Exception as e:
        print(e)
else:
    print("We already have a copy of this game commentary. Moving on.....")

# Using Speech Recognition on commentary
if not os.path.exists(f"./commentary/{game}"):
    print("Starting speech recognition.....")
    r = sr.Recognizer()
    audio = sr.AudioFile(f"./audio/{game}")
    with audio as source:
        audio_file = r.record(source)
    result = r.recognize_google(audio_file)

    # Exporting the result of Speech Recognition
    open(f'./commentary/{game}.txt', mode ='w').write(result)
    print(f"Speech recognition finished and saved as './commentary/{game}.txt'.....")
else:
    print("We have already generate a transcript of this game commentary. Moving on.....")