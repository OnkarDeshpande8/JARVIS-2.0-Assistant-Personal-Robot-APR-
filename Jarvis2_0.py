# JARVIS 2.0
# Author : Onkar Anil Deshpande
# Date : 12/02/2021
#-----------------------------------------------------------------------------------------

import pyttsx3                                  #pip3 install pyttsx3
import speech_recognition as sr                 #pip3 install speechRecognition  
import datetime
import wikipedia                                #pip3 install wikipedia
import  webbrowser
import os
import smtplib
import time
import logging
import vlc
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setwarnings(False)

Debug_log = "Debug.log"
PROJECT_TITLE = "JARVIS 2.0"

Pyttsx3_init = 'espeak'
VOICE_GetProp = 'voices'
VOICE_SetProp = 'voice1'
G_M = "Good Morning!"
G_A = "Good Afternoon!"
G_E = "Good Evening!"
Jarvis_Intro = "I am Jarvis. Please tell me how may I help you"

SMTP_EMAIL = 'smtp.gmail.com'
MY_EMAIL = 'onkard543@gmail.com'
Email_Password = 'Onkar@708854'

STATUS_ERROR1 = "ERROR : "

engine = pyttsx3.init(Pyttsx3_init)
voices = engine.getProperty(VOICE_GetProp)
engine.setProperty(VOICE_SetProp, voices[17].id)
engine.setProperty('rate', 190)
engine.setProperty('volume', 0.5)

CW1 = 17  #11
ACW1 = 27 #13
CW2 = 22  #15
ACW2 = 23 #16
GPIO.setup(CW1, GPIO.OUT) # GPIO Assign mode
GPIO.setup(ACW1, GPIO.OUT) # GPIO Assign mode
GPIO.setup(CW2, GPIO.OUT) # GPIO Assign mode
GPIO.setup(ACW2, GPIO.OUT) # GPIO Assign mode

def forward1():
    GPIO.output(CW1, GPIO.HIGH)
    GPIO.output(ACW1, GPIO.LOW)
    GPIO.output(CW2, GPIO.HIGH)
    GPIO.output(ACW2, GPIO.LOW)
    print('forward1')
    time.sleep(9)
    GPIO.output(CW1, GPIO.LOW)
    GPIO.output(ACW1, GPIO.LOW)
    GPIO.output(CW2, GPIO.LOW)
    GPIO.output(ACW2, GPIO.LOW)
    
def right1():
    GPIO.output(CW1, GPIO.HIGH)
    GPIO.output(ACW1, GPIO.LOW)
    GPIO.output(CW2, GPIO.LOW)
    GPIO.output(ACW2, GPIO.HIGH)
    print('right')
    time.sleep(3)
    GPIO.output(CW1, GPIO.HIGH)
    GPIO.output(ACW1, GPIO.LOW)
    GPIO.output(CW2, GPIO.HIGH)
    GPIO.output(ACW2, GPIO.LOW)
    time.sleep(3)
    GPIO.output(CW1, GPIO.LOW)
    GPIO.output(ACW1, GPIO.LOW)
    GPIO.output(CW2, GPIO.LOW)
    GPIO.output(ACW2, GPIO.LOW)
    
def left1():
    GPIO.output(CW1, GPIO.LOW)
    GPIO.output(ACW1, GPIO.HIGH)
    GPIO.output(CW2, GPIO.HIGH)
    GPIO.output(ACW2, GPIO.LOW)
    print('left')
    time.sleep(3)
    GPIO.output(CW1, GPIO.HIGH)
    GPIO.output(ACW1, GPIO.LOW)
    GPIO.output(CW2, GPIO.HIGH)
    GPIO.output(ACW2, GPIO.LOW)
    time.sleep(3)
    GPIO.output(CW1, GPIO.LOW)
    GPIO.output(ACW1, GPIO.LOW)
    GPIO.output(CW2, GPIO.LOW)
    GPIO.output(ACW2, GPIO.LOW)
    
def reverse1():
    GPIO.output(CW1, GPIO.LOW)
    GPIO.output(ACW1, GPIO.HIGH)
    GPIO.output(CW2, GPIO.LOW)
    GPIO.output(ACW2, GPIO.HIGH)
    print('reverse')
    time.sleep(9)
    GPIO.output(CW1, GPIO.LOW)
    GPIO.output(ACW1, GPIO.LOW)
    GPIO.output(CW2, GPIO.LOW)
    GPIO.output(ACW2, GPIO.LOW)

def stop1():
    GPIO.output(CW1, GPIO.LOW)
    GPIO.output(ACW1, GPIO.LOW)
    GPIO.output(CW2, GPIO.LOW)
    GPIO.output(ACW2, GPIO.LOW)
    print('stop')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak(G_M)
        print(G_M)

    elif hour>=12 and hour<18:
        speak(G_A)
        print(G_A)

    else:
        speak(G_E)
        print(G_E)

    speak(Jarvis_Intro)
    print(Jarvis_Intro)
    time. sleep(3)

def takeCommand():
    #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source,duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print("User said: {}".format(query))
    except:
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP(SMTP_EMAIL, 587)
    server.ehlo()
    server.starttls()
    server.login(MY_EMAIL, Email_Password)
    server.sendmail(MY_EMAIL, to, content)
    server.close()

try:
    #create a logger
    logger = logging.getLogger(PROJECT_TITLE)
    #set logging level
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(Debug_log)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    if __name__ == "__main__":
        wishMe()
        while True:
            query = takeCommand().lower()
            # Logic for executing tasks based on query
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')    
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in query:
                webbrowser.open("youtube.com")

            elif 'open google' in query:
                webbrowser.open("google.com")

            elif 'play music' in query:
                music_dir = '/home/pi/Music'
                songs = os.listdir(music_dir)
                print(songs)
                p = vlc.MediaPlayer("file:///home/pi/Music/Maay Bhavani - Tanhaji.mp3")
                p.play()
                
                try:
                    if '1' in query:
                        p = vlc.MediaPlayer("file:///home/pi/Music/Ghamand Kar - Tanhaji.mp3")
                        p.play()
                    if '2' in query:
                        p = vlc.MediaPlayer("file:///home/pi/Music/Maay Bhavani - Tanhaji.mp3")
                        p.play()
                    if '3' in query:
                        p = vlc.MediaPlayer("file:///home/pi/Music/Shankara Re Shankara - Tanhaji.mp3")
                        p.play()
                    if '4' in query:
                        p = vlc.MediaPlayer("file:///home/pi/Music/Tinak Tinak - Tanhaji.mp3")
                        p.play()
                except:
                    print("can't find songs")
                        

            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                speak(f"Sir, the time is {strTime}")

            elif 'thank you' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                speak(f"Your Welcome")

            elif 'institute vision' in query:
                print('To be a center of excellence in technical education by using cutting edge technology that produces competent engineers of today and tomorrow to serve the society')    
                speak(f"To be a center of excellence in technical education by using cutting edge technology that produces competent engineers of today and tomorrow to serve the society")

            elif 'introduce' in query:
                print()
                speak('Hi, I  am  JARVIS.  Personal Assistant Robot. Speed 4 Gigabyte. Memory 32 Gigabyte. Hardware is Raspberry pi 4')
                
            elif 'email to aakash' in query:
                try:
                    speak("What should I say?")
                    content = takeCommand()
                    to = "onkard654@gmail.com"    
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry my friend onkar. I am not able to send this email")             

            elif 'forward' in query:
                forward1()
                time.sleep(5)

            elif 'right' in query:
                right1()
                time.sleep(5)
                

            elif 'left' in query:
                left1()
                time.sleep(5)
                
            elif 'reverse' in query:
                reverse1()
                time.sleep(5)
                
            elif 'backward' in query:
                reverse1()
                time.sleep(5)

            elif 'stop' in query:
                stop1()
                time.sleep(5)
                
            elif 'hold' in query:
                stop1()
                time.sleep(5)

except Exception as e:
    print(e)
    logger.debug(STATUS_ERROR1 + str(e))
