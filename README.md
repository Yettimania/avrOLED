# avrOLED

## Description

This python script will generate a header file that can be used with 8 bit AVR microcontrollers. 

## Usage

Prerequisites are the 'struc' and 'sys' python libraries.

The BMP should be stored as 2 colors and 1 byte per pixel. For example, a 48x84 pixel screen should have 4,032 bytes for the python script to read.

This script assumes common OLED vertical addressing with the (0,0) origin of the LED screen at the top left. It reads the BMP image and stores 8 pixels in a single byte that can be used with AVR microcontrollers which commonly communicate of I2C, SPI. This can be stored in PROGMEM to save CPU.

Clone the repository or download the python script to the folder with the image.

Run 

```bash
python bmp2image.py Image.bmp
```
Copy or rename the .h file generate from the script.

