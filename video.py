import cv2
import numpy as np

# --- CONFIGURATION ---
VIDEO_PATH = 'second_video.mp4'
OUTPUT_FILE = 'frames_data.h'
WIDTH = 128
HEIGHT = 64
FRAME_DELAY = 16

def convert_video():
    cap = cv2.VideoCapture(VIDEO_PATH)
    frames_list = []

    print("Extracting and processing frames using Otsu's Algorithm...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 1. Resize to EXACTLY 128x64
        frame_res = cv2.resize(frame, (WIDTH, HEIGHT))

        # 2. Convert to Grayscale
        gray = cv2.cvtColor(frame_res, cv2.COLOR_BGR2GRAY)

        # 3. THE MAGIC: Otsu's Thresholding
        # This automatically finds the best black/white balance per frame.
        # It keeps text legible and faces clear without random dark dots.
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # 4. Pack bits into hex format
        flat = binary.flatten()
        byte_array = []
        for i in range(0, len(flat), 8):
            byte_val = 0
            for bit in range(8):
                if flat[i + bit] > 0:
                    byte_val |= (1 << (7 - bit))
            byte_array.append(f"0x{byte_val:02x}")
        
        frames_list.append(byte_array)

    cap.release()

    # Calculate exact array sizes
    num_frames = len(frames_list)
    bytes_per_frame = (WIDTH * HEIGHT) // 8

    print(f"Formatting {num_frames} frames into flawless C++...")

    # 5. WRITE TO C++ HEADER FILE (Fixing all comma errors)
    with open(OUTPUT_FILE, 'w') as f:
        # Standard includes for ESP32 PROGMEM
        f.write("#include <Arduino.h>\n")
        f.write("#include <pgmspace.h>\n\n")
        
        f.write(f"#define FRAME_WIDTH {WIDTH}\n")
        f.write(f"#define FRAME_HEIGHT {HEIGHT}\n")
        f.write(f"#define FRAME_DELAY {FRAME_DELAY}\n")
        f.write(f"#define NUM_FRAMES {num_frames}\n\n")

        # Start the 2D array
        f.write(f"const unsigned char frames[{num_frames}][{bytes_per_frame}] PROGMEM = {{\n")

        # Safely wrap every frame inside its own { } to prevent C++ compiler errors
        for i, frame_bytes in enumerate(frames_list):
            f.write(f"  {{ // Frame {i}\n    ")
            
            # Format bytes into neat rows of 16
            lines = []
            for j in range(0, len(frame_bytes), 16):
                lines.append(", ".join(frame_bytes[j : j + 16]))
            
            f.write(",\n    ".join(lines))
            
            # Close the frame's bracket. Add a comma ONLY if it's not the last frame.
            if i < num_frames - 1:
                f.write("\n  },\n")
            else:
                f.write("\n  }\n") # NO COMMA on the last frame!

        f.write("};\n")

    print(f"Success! Saved to {OUTPUT_FILE}. Ready to compile in PlatformIO.")

if __name__ == "__main__":
    convert_video()