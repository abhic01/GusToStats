from pytube import YouTube
import speech_recognition as sr

# Function to check if a game took place 
def checkGame(year : str, home_team : str, away_team : str) -> bool : 
    url = f"https://en.wikipedia.org/wiki/{year}_{teams[home_team]}_{home_team.lower().capitalize()}_season" # Wiki has a great list of all 
    return False

# Variable setup
teams = {"CARDINALS" : "ARIZONA", "FALCONS" : "ATLANTA", "PANTHERS" : "CAROLINA", "BEARS" : "CHICAGO", "COWBOYS" : "DALLAS", "LIONS" : "DETRIOT", 
        "PACKERS" : "GREEN BAY", "RAMS" : "LOS ANGELES", "VIKINGS" : "MINNESOTA", "SAINTS" : "NEW ORLEANS", "GIANTS" : "NEW YORK", "EAGLES" : "PHILADELPHIA",
        "49ERS" : "SAN FRANCISCO", "SEAHAWKS" : "SEATTLE", "BUCCANEERS" : "TAMPA BAY", "COMMANDERS" : "WASHINGTON", "REDSKINS" : "WASHINGTON", 
        "RAVENS" : "BALTIMORE", "BILLS" : "BUFFALO", "BENGALS" : "CINCINNATI", "BROWNS" : "CLEVELAND", "BRONCOS" : "DENVER", "TEXANS" : "HOUSTON",
        "COLTS" : "INDIANAPOLIS", "JAGUARS" : "JACKSONVILLE", "CHIEFS" : "KANSAS CITY", "RAIDERS" : "OAKLAND", "DOLPHINS" : "MIAMI", "CHARGERS" : "LOS ANGELES", 
        "PATRIOTS" : "NEW ENGLAND", "STEELERS" : "PITTSBURGH", "TITANS" : "TENNESSEE"}

# Setting up the game and teams that played
game = input("Please enter the NFL game you would like to analyze in the format {Away Team} @ {Home Team} {Year}\n").upper() # Getting game and teams
game_list = game.split()
year = game_list[3]
home_team = game_list[0]
away_team = game_list[2]
if not checkGame(year, home_team, away_team):
    print("The game you entered does not exist. Please try again.")
    exit(0)

# Importing audio from a YouTube video of a game that we want to make stats for
print(f"Importing game commentary for: {game}.....")
url = "" # Selecting the url of the particular game using BS4
try:
    video = YouTube(url)
    video_audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
    video_audio.download()
    print("Audio download completed.....")
except Exception as e:
    print(e)


# Using microphone to listen into commentary
recording = sr.Recognizer()
with sr.Microphone() as source:
    recording.adjust_for_ambient_noise(source) # Removing ambient noise that goes into mic
    print("Started listening to the commentary.....")
    audio = recording.listen(source)
    try:
        print(f"You said: {recording.recognize_google(audio)}")
    except Exception as e:
        print(e)
