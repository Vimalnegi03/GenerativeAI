import speech_recognition as sr
import time

# Initialize recognizer
recognizer = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("🔧 Calibrating microphone for background noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source, duration=2)
    
    print("✅ Calibration complete.")
    print("🎤 You will be able to speak in 3 seconds...")
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

    print("🎙️ Listening now... Speak clearly!")
    audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)

    try:
        print("🔍 Recognizing...")
        text = recognizer.recognize_google(audio)
        print("✅ You said:", text)
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError as e:
        print(f"❌ Could not request results from Google Speech Recognition service; {e}")
