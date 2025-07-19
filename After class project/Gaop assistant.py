import pyttsx3

pyttsx3= pyttsx3.init()

def speak(text):
    print(f'Gaop: {text}')
    pyttsx3.say(text)
    pyttsx3.runAndWait()

good = {'happy', 'excited', 'great', 'fantastic', 'awesome', 'wonderful'}
hobbies = {'reading', 'coding', 'gaming', 'volleyball', 'programming'}

speak("Hello There, I am happy to see you here!\nMy name is Gaop (Greater Arc Of Python). I am a computer program to whom you can talk to feel better!")

speak("What is your name?")
name = input(":")
speak(f"Hello {name}, I hope you are having a great day!")

speak("How are you feeling today?")
feeling = input(":")

if feeling.lower() in good:
    speak("Happy to hear that!")
else:
    speak("I hope your day gets better!")

speak("What is your favorite hobby?")
hobby = input(":")

if hobby.lower() in hobbies:
    speak(f"That's great! I also enjoy {hobby}.")
else:
    speak("That's interesting! ")

speak("Would you like to restart our conversation? (yes/no)")

restart = input(":")
if restart.lower() not in ["yes", "no"]:
    speak("Please answer with 'yes' or 'no'.")
    restart = input(":")
if restart == "yes":
    speak("Let's start over then!")
elif restart == "no":
    speak("Thank you for sharing! Have a wonderful day ahead!")