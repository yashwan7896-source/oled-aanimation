# OLED Animation on ESP32

This project plays black and white animations on a 128x64 SSD1306 OLED display using an ESP32 microcontroller.


## What you need

- ESP32
- 128x64 SSD1306 OLED Display
- Python 3
- OpenCV (`pip install opencv-python`)
- PlatformIO (VS Code)

## Wiring

| OLED | ESP32 |
|------|-------|
| GND | GND |
| VCC | 3.3V |
| SCL | GPIO 22 |
| SDA | GPIO 21 |

## How to use

### 1. Add your video

Put your video in the project folder.

If your video has a different name, change the filename in `video.py`.

### 2. Run the Python script

```bash
python video.py
```

This will generate a file named `frames_data.h`.

### 3. Update `main.cpp`

Open `frames_data.h` and copy the generated frame array.

Replace the old frame array inside `src/main.cpp`.

Don't change anything else.

### 4. Upload to ESP32

Open the project in PlatformIO and upload it to your ESP32.

If everything is connected correctly, the animation will start playing on the OLED.

## Troubleshooting

### OLED is blank

- Check the wiring.
- Make sure your OLED uses the `0x3C` I2C address.

### Python error

Install OpenCV:

```bash
pip install opencv-python
```

### Upload failed

- Try another USB cable or USB port.
- Check if the correct board is selected in PlatformIO.

## Notes

- OLED resolution is **128×64**.
- The Python script converts each frame into black and white before generating the frame data.
- Shorter videos work better because they use less memory.

---

If you found this project useful, feel free to ⭐ the repository.
