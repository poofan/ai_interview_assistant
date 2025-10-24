#!/usr/bin/env python3
"""
Test script for dual audio capture mode (System + Microphone)
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.audio_capture import AudioCapture
from loguru import logger

# Configure logging
logger.remove()
logger.add(sys.stderr, format="<level>{level: <8}</level> | {message}")
logger.add("logs/test_dual_audio.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}")

def test_dual_capture():
    """Test dual audio capture"""
    print("\n" + "="*60)
    print("[TEST] Dual Audio Capture Test")
    print("="*60)
    
    # Create audio capture with "both" mode
    audio = AudioCapture(
        sample_rate=16000,
        channels=1,
        chunk_size=1024,
        buffer_seconds=5,
        source="both",
        device_name="стерео микшер"
    )
    
    try:
        print("[TEST] Starting audio capture...")
        audio.start()
        
        print("[TEST] Audio capture started successfully!")
        print("[TEST] Recording for 5 seconds...")
        print("[TEST] Speak into your microphone and play system audio...\n")
        
        chunks_received = 0
        start_time = time.time()
        
        # Record for 5 seconds
        while time.time() - start_time < 5:
            chunk = audio.get_audio_chunk(timeout=1.0)
            if chunk is not None:
                chunks_received += 1
                print(f"  [OK] Chunk {chunks_received} received ({len(chunk)} samples)")
            else:
                print("  [WAIT] Timeout (no audio)")
            
            time.sleep(0.1)
        
        print(f"\n[TEST] Recording completed!")
        print(f"[TEST] Total chunks received: {chunks_received}")
        
        # Get buffer
        buffer = audio.get_buffer(seconds=2)
        print(f"[TEST] Last 2 seconds of buffer: {len(buffer)} samples")
        print(f"[TEST] Buffer RMS: {(buffer ** 2).mean() ** 0.5:.4f}")
        
        audio.stop()
        print("\n[TEST] [SUCCESS] Dual capture test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        logger.exception(e)
        return False
    finally:
        if audio.is_running():
            audio.stop()

if __name__ == "__main__":
    success = test_dual_capture()
    sys.exit(0 if success else 1)
