"""
Test audio input/output with sounddevice
"""
import sounddevice as sd
import numpy as np
import time

def test_audio():
    print("=" * 50)
    print("Audio Test Utility")
    print("=" * 50)
    
    try:
        print("\n📋 Available Audio Devices:")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            print(f"  Device {i}: {device['name']} (Input: {device['max_input_channels']}, Output: {device['max_output_channels']})")
        
        print("\n🎤 Testing recording and playback...")
        print("Recording 3 seconds of audio...")
        
        sample_rate = 16000
        channels = 1
        duration = 3
        
        recording = sd.rec(int(duration * sample_rate), 
                          samplerate=sample_rate, 
                          channels=channels, 
                          dtype='int16')
        sd.wait()
        
        print("✅ Recording complete!")
        print("🔊 Playing back recorded audio...")
        
        sd.play(recording, samplerate=sample_rate)
        sd.wait()
        
        print("✅ Playback complete!")
        print("\n🎉 Audio test successful!")
        print("Your microphone and speakers are working correctly.")
        
    except Exception as e:
        print(f"\n❌ Error during audio test: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your microphone is connected")
        print("2. Check that your speakers/headphones are connected")
        print("3. Check Windows sound settings")
        print("4. Make sure no other app is using the microphone")

if __name__ == "__main__":
    test_audio()
