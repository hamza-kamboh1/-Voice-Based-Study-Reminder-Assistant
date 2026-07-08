"""
Simple STT Test using sounddevice
"""
import sounddevice as sd
import speech_recognition as sr
import numpy as np

def test_stt():
    print("=" * 50)
    print("STT Test with sounddevice")
    print("=" * 50)
    
    try:
        print("\n🎤 Recording 5 seconds of audio...")
        print("Speak clearly into your microphone...")
        
        sample_rate = 16000
        duration = 5
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16'
        )
        sd.wait()
        
        print("✅ Recording complete!")
        print("🔄 Transcribing...")
        
        audio_data = recording.tobytes()
        audio = sr.AudioData(audio_data, sample_rate, 2)
        
        recognizer = sr.Recognizer()
        text = recognizer.recognize_google(audio)
        
        print(f"\n📝 You said: {text}")
        print("\n✅ STT Test successful!")
        
    except sr.UnknownValueError:
        print("\n❌ Could not understand audio. Please speak clearly and try again.")
    except sr.RequestError as e:
        print(f"\n❌ Error with Google Speech Recognition: {e}")
        print("Please check your internet connection.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your microphone is connected")
        print("2. Check internet connection")
        print("3. Try speaking clearly and loudly")

if __name__ == "__main__":
    test_stt()
