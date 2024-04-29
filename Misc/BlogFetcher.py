# !! Note: This no longer works. !!
# The blog storage has been made private, meaning a list of all images is impossible to obtain currently.
# So unless you know the exact name of the image, you aren't able to get it early.

# I know this code is probably bad, I had no idea what I was doing, and I just mixed some examples from the documentation with chat gpt.
import requests
import time
import os
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

FOLDER_PATH = "Images"
BLOG_URL = "https://bigblog-storage.s3.us-east-1.amazonaws.com"
def sanitize_image_name(name):
    sanitized_name = re.sub(r'[\\/*?"<>|:]', ' ', name)
    sanitized_name = sanitized_name.strip()
    return sanitized_name
print("BIG Blog Fetcher")
print("----------------------------")
print("")
print("This script fetches blog images from BIG Games")
print("Please provide the key to match for the last modified property.")
print("For example, 2023-12-23 will only display images from the 23rd of December 2023")
timesDone = 0
os.makedirs(FOLDER_PATH, exist_ok=True)
while True:
    timesDone = timesDone + 1
    print("")
    print("----------------------------")
    print("")
    if timesDone != 1:
        print("Please provide the key to match for the last modified property. (Or !exit to exit)")
    userKeyMatch = input()
    if userKeyMatch == "!exit":
        break
    if len(userKeyMatch) < 5:
        print("")
        print("The key match is short.")
        print("This could match a lot of images, which can take a long time.")
        print("Are you sure? (yes/no)")
        if input().lower() != "yes":
            continue
    print("")
    print("Getting blog images...")
    response = requests.get(BLOG_URL)
    if response.status_code == 200:
        print("Got a list of blog images...")
        keyFolderPath = os.path.join(FOLDER_PATH, sanitize_image_name(userKeyMatch))
        os.makedirs(keyFolderPath, exist_ok=True)
        bs_data = BeautifulSoup(response.content, 'xml')
        root = ET.fromstring(response.content)
        for tag in bs_data.find_all('Contents'):
            lastModified = tag.find("LastModified").text
            fileName = tag.find("Key").text
            if userKeyMatch in lastModified:
                print(f"Downloading {fileName}")
                imageResponse = requests.get(BLOG_URL + "/" + fileName)
                if imageResponse.status_code == 200:
                    fileNameToUse = sanitize_image_name(fileName)
                    file_name = f"{keyFolderPath}/{fileNameToUse}"
                    with open(file_name, 'wb') as file:
                        file.write(imageResponse.content)
                else:
                    print(f"Failed to download {fileName}")
        print("")
        print("All images have been downloaded.")
    else:
        print(f"Error downloading: {response.status_code}")
