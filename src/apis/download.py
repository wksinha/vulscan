import requests
import subprocess
import os
import platform

firefox_download_url = "https://download.mozilla.org/?product=firefox-latest&os=win&lang=en-US"

if platform.system() == "Windows":
    installer_name = "Firefox Installer.exe"
    firefox_download_url = "https://download.mozilla.org/?product=firefox-latest&os=win&lang=en-US"
elif platform.system() == "Linux":
    installer_name = "firefox.tar.bz2"
    firefox_download_url = "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"
elif platform.system() == "Darwin":  # macOS
    installer_name = "Firefox.dmg"
    firefox_download_url = "https://download.mozilla.org/?product=firefox-latest&os=osx&lang=en-US"
else:
    raise Exception("Unsupported OS")

import os
import shutil
folder_path = '~/programs/firefox'

if os.path.isdir(folder_path):
    shutil.rmtree(folder_path)

print("Downloading Firefox...")
response = requests.get(firefox_download_url, stream=True)
if response.status_code == 200:
    with open(installer_name, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print(f"Downloaded {installer_name}")
else:
    print("Failed to download Firefox.")
    exit(1)

extract_command = ["tar", "-xjf", "firefox.tar.bz2", "-C", "/home/warks/programs"]
subprocess.run(extract_command)