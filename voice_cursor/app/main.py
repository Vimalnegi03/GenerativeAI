import speech_recognition as sr
from langgraph.checkpoint.mongodb import MongoDBSaver
import pyttsx3
from graph import create_chat_graph

MONGODB_URI = ""
Ai_Message = ""
config = {"configurable": {"thread_id": "7"}}

def speak(text: str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
    engine.say(text)
    engine.runAndWait()

def main():
    global Ai_Message
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph = create_chat_graph(checkpointer=checkpointer)
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            speak("Hello! I am listening.")
            while True:
                print("Say something (say 'exit' to quit)...")
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                    print("Recognizing...")
                    speech_to_text = r.recognize_google(audio).lower()
                    print("You said:", speech_to_text)

                    if speech_to_text in ["exit", "quit", "band karo", "bye"]:
                        speak("Okay, shutting down. Goodbye!")
                        return

                    # Get the stream of messages
                    latest_message = None
                    for event in graph.stream(
                        {"messages": [{"role": "user", "content": speech_to_text}]},
                        config,
                        stream_mode="values"
                    ):
                        if "messages" in event:
                            latest_message = event["messages"][-1]

                    if latest_message:
                        Ai_Message = latest_message.content
                        print("🤖 AI Final Message:", Ai_Message)
                        speak(Ai_Message)

                except sr.WaitTimeoutError:
                    print("⏱️ Timeout: No speech detected.")
                except sr.UnknownValueError:
                    print("❓ Could not understand audio.")
                    speak("Sorry, I couldn't understand.")
                except sr.RequestError as e:
                    print(f"🔌 Google Speech error: {e}")
                    speak("I'm facing a speech recognition error.")

if __name__ == "__main__":
    main()
