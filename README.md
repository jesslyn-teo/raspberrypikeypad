## raspberrypikeypad
This project implements a home security system using a Raspberry Pi, an ultrasonic sensor, a camera, a keypad, and a Telegram bot for notifications. The system is designed to detect motion, capture images of intruders, and allow access through a keypad or a Telegram command.

## Table of Contents
1. Introduction
2. Componenets and Setup
3. Installations
4. Usage
5. Troubleshooting

# Introduction
Hi! This is one of my first ever electronic projects I have done together with my teammate for my elective in the Internet of Things.

# Components and Setup
- Hardware Components
  1. Raspberry Pi: The main controller.
  2. PiCamera: Used to capture images of intruders.
  3. Ultrasonic Sensor: Detects motion by measuring distance.
  4. Keypad: Used to input a passcode for door unlocking.
  5. LED: Indicates door unlocking status.
  6. Buzzer: Alerts the homeowner after multiple failed attempts.
  7. GPIO Pins: For connecting the above components.
- Software Components
  1. Python: The programming language used for scripting.
  2. RPi.GPIO: Library for controlling GPIO pins.
  3. PiCamera: Library for controlling the camera module.
  4. requests: Library for making HTTP requests to the Telegram API.
  5. python-telegram-bot: Library for integrating with Telegram

# Installation 
1. Setup Telegram Bot
   - Create a new bot using BotFather on Telegram in order to obtain the token
2. Connect the Hardware
   - Connect the components to the Raspberry Pi GPIO pins as per the wiring diagram

# Usage 
1. Motion Detection:
   - The ultrasonic sensor continuously monitors for motion.
   - If motion is detected within the threshold distance, the system captures an image and sends it to the homeowner via Telegram.
2. Keypad Activation:
   - The user can input a 4-digit passcode to unlock the door.
   - If the correct passcode is entered, the LED blinks 3 times indicating the door is unlocked.
   - If the incorrect passcode is entered 3 times, the buzzer alerts the homeowner and an image is sent via Telegram.
3. Remote Door Unlocking:
   - The homeowner can send the /unlock_door command to the Telegram bot to remotely unlock the door.
   - The LED blinks 3 times indicating the door is unlocked.

# Troubleshooting 
- Camera Issues: Ensure the camera is properly connected and enabled in the Raspberry Pi configuration.
- GPIO Pin Conflicts: Check for any conflicts with other connected devices or incorrect wiring.
- Telegram Bot Errors: Verify the bot token and chat ID. Check internet connectivity on the Raspberry Pi.
