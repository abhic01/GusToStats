from pytube import YouTube
from pydub import AudioSegment
from scipy.io import wavfile
import speech_recognition as sr, re, requests, os.path, urllib.parse, urllib.request, moviepy.editor as mp, noisereduce as nr
from bs4 import BeautifulSoup

# Function to check if a particular game took place 
def checkGame(year : str, home_team : str, away_team : str) -> bool : 
    url = f"https://en.wikipedia.org/wiki/{year}_{teams[home_team]}_{home_team.lower().capitalize()}_season#Game_summaries" # Wiki contains a list of all games played by each team based on the year
    response = requests.get(url)
    return f"vs. {teams[away_team]} {away_team.lower().capitalize()}" in response.text

# Function to split large audio file into smaller 1 minute chunks
def getChunks(audio, duration):
    t1 = 0
    t2 = 60000
    i = 0
    while t2 <= duration: 
        print(f"Saving chunk #{i + 1}.....")
        audio[t1:t2].export(f'C:/Users/abhi2/Desktop/Personal Projects/GusToStats/audio/chunk{i}.wav', format="wav")
        i += 1
        t1 = t2
        if t2 == duration:
            break
        elif t2 + 60000 > duration:
            t2 = duration
        else:
            t2 += 60000

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
if not os.path.exists(f"C:/Users/abhi2/Desktop/Personal Projects/GusToStats/audio/{game}"):
    print(f"Importing game commentary for: {game}.....")
    query = urllib.parse.urlencode({"search_query": game})
    url = urllib.request.urlopen("https://www.youtube.com/results?" + query) # URL of the most relevant video on YT search
    search_results = re.findall(r"watch\?v=(\S{11})", url.read().decode())
    video_url = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    print(f"Link to the most relevant YT video is: {video_url}.....")

    # Downloading the audio of the YT video as an mp4 file
    try:
        video = YouTube(video_url)
        video_audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
        video_audio.download(output_path = "C:/Users/abhi2/Desktop/Personal Projects/GusToStats/audio", filename = game)
        print("Audio download completed.....")
    except Exception as e:
        print(e)
else:
    print("We already have a copy of this game commentary. Moving on.....")

# Using Speech Recognition on commentary
if not os.path.exists(f"C:/Users/abhi2/Desktop/Personal Projects/GusToStats/commentary/{game}.wav"):
    print("Starting speech recognition.....")
    r = sr.Recognizer()
    mp.AudioFileClip(f"C:/Users/abhi2/Desktop/Personal Projects/GusToStats/audio/{game}").write_audiofile(f"C:/Users/abhi2/Desktop/Personal Projects/GusToStats/audio/{game}.wav")

    # Dividing audio into smaller chunks for Google Speech Recognition to work on
    print("Spliting audio into consumable chunks......")
    audio = AudioSegment.from_wav(f"C:/Users/abhi2/Desktop/Personal Projects/GusToStats/audio/{game}.wav")
    duration = audio.duration_seconds * 1000 # Duration of audio file in milliseconds
    getChunks(audio, duration)

    # Getting a second of background noise which is to be used as a filter to eliminate noise from audio clips
    rate, noise = wavfile.read(f"C:/Users/abhi2/Desktop/Personal Projects/GusToStats/audio/noise.wav")

    print("Chunks have been created.....")

    # Converting chunks into text
    print("Converting the audio chunks into text.....")
    for i in range(int(duration / 1000) - 1):
        print(f"Converting chunk #{i + 1} to text.....")
        ogAudio = sr.AudioFile(f"C:/Users/abhi2/Desktop/Personal Projects/GusToStats/audio/chunk{i}.wav")
        audio = nr.reduce_noise(y = ogAudio, sr = rate, y_noise = noise)
        with audio as source:
            audio_file = r.record(source)
        result = r.recognize_google(audio_file, language = 'en-US')
        # Exporting the result of Speech Recognition
        open(f"C:/Users/abhi2/Desktop/Personal Projects/GusToStats/commentary/{game}.txt", mode ="a").write(str(result))
        print(f"Chunk #{i + 1} converted to text and added to './commentary/{game}.txt'.....")
        i += 1
    print("Successfully converted audio to text.....")
else:
    print("We have already generate a transcript of this game commentary. Moving on.....")