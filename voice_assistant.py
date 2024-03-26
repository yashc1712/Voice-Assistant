from neuralintents import BasicAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['Go Shopping', 'Clean Room', 'Learn AI']

def create_note():
    global recognizer
    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = ''.join(c for c in filename if c.isalnum() or c.isspace())
                filename = filename.replace(' ', '_')  # Replace spaces with underscores
                filename = filename.lower()

            with open(filename + '.txt', 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created note {filename}")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you. Please try again!!!")
            speaker.runAndWait()

def add_todo():
    global recognizer
    speaker.say("What do you want to add?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f"I successfully added {item} to todo list")
                speaker.runAndWait()
        
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you. Please try again!!!")            
            speaker.runAndWait()

def show_todo():
    speaker.say("The items on your todo list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    speaker.say("Hello. What can i do for you today?")
    speaker.runAndWait()

def quit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit(0)

mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todo,
    "exit": quit
}

assistant = BasicAssistant(r'C:\Users\Yash\Desktop\Python\Voice Assistant\intents.json', mappings)
assistant.fit_model(epochs=50)
assistant.save_model()

while True:
  try:
    with speech_recognition.Microphone() as mic:
      recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
      audio = recognizer.listen(mic)
      message = recognizer.recognize_google(audio)
    assistant.process_input(message)
  except speech_recognition.UnknownValueError:
    recognizer = speech_recognition.Recognizer()
