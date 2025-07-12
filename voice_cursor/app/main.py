import speech_recognition as sr

def main():
    r = sr.Recognizer()
    r.pause_threshold = 5  # Seconds of silence before considering the phrase complete

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something (will stop after 3 sec of silence)...")

        try:
            audio = r.listen(source, timeout=5)
            # timeout: max wait for speech to start
            # phrase_time_limit: max total time for phrase

            print("Recognizing...")
            speech_to_text = r.recognize_google(audio)
            print("You said:", speech_to_text)

        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

main()
