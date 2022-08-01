#!/usr/bin/env python3

from selenium import webdriver
import os
import sys
import time
import argparse
import moviepy.editor as mpy

target_url = argparse.add_argument("--url", help="Target URL", type=str)
framerate = argparse.add_argument(
    "--framerate", help="Framerate of the output video", type=int, default=24)
count_of_frames = argparse.add_argument(
    "--count", help="Count of frames to capture", type=int, default=48)
screenshot_pause = argparse.add_argument(
    "--pause", help="Frequency of screenshots", type=float, default=0.1)

firefox_driver_source = "https://github.com/mozilla/geckodriver/releases/latest"

# Found GeckoDriver.exe in working directory. If not found, download it from firefox_driver_source
if not os.path.isfile("geckodriver.exe"):
    print("You need to download geckodriver.exe from " + firefox_driver_source)
    sys.exit()

# Create a new instance of the Firefox driver
gecko_options = webdriver.FirefoxOptions()
gecko_options.add_argument("--headless")

# New session
browser = webdriver.Firefox(options=gecko_options)
browser.get(target_url)

# Create a folder for temporary files
if not os.path.exists("TEMP"):
    os.makedirs("TEMP")

# Loop for the number of frames
for i in range(0, count_of_frames):
    time.sleep(screenshot_pause)
    browser.save_screenshot("TEMP/image" + str(i) + ".png")

# Open a files and combine them into a video
images_list = []
for frame in range(0, count_of_frames):
    images_list.append("TEMP/image" + str(frame) + ".png")
clip = mpy.ImageSequenceClip(images_list, fps=framerate)
clip.write_videofile("video.mp4")

# Clear temporary files
for file in os.listdir("TEMP"):
    os.remove("TEMP/" + file)
