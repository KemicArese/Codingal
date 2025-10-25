from transformers import pipeline
import torch
import pyttsx3
import speech_recognition as sr
sentiment_pipeline = pipeline("sentiment-analysis")

def classify_text(text):
    result = sentiment_pipeline(text)
    return result

def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        print("Listening... Please speak into the microphone.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        user_input = input("Type '1' for text input, '2' for voice input, or 'exit' or 'q' to quit: ").strip()
        if user_input.lower() == 'exit' or user_input.lower() == 'q':
            print("Goodbye!")
            break
        elif user_input == '1':
            text = input("Enter text to classify sentiment: ").strip()
        elif user_input == '2':
            text = listen()
            if text is None:
                continue
        else:
            print("Invalid option. Please try again.")
            continue

    result = classify_text(text)
    sentiment = result[0]['label']
    confidence = result[0]['score']
    output = f"Sentiment: {sentiment} (Confidence: {confidence:.2f})"
    print(output)
    speak(output)
