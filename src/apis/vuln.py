import sqlite3
from flask import Flask, jsonify, request, abort
import requests
import subprocess
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)
FIREFOX_CPE = 'cpe:2.3:a:mozilla:firefox'
MAX_ATTEMPTS = 3
SLEEP_TIME = 30

glob_id = 0
task_status = {}

patch_id = 0
patch_status = {}

scan_data = None

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    global task_status
    task_id = int(task_id)
    print(f"DEBUG: Requested Task ID: {task_id}")
    print(f"DEBUG: Current Task Status: {task_status}")
    
    status = task_status.get(task_id, "FAILED")
    
    print(f"DEBUG: Status for {task_id}: {status}")
    return jsonify({"status": status})

@app.route('/install', methods=['GET'])
def install_patch():

    try:
        downloadUrl = request.args.get('downloadUrl', default='', type=str)
        firefox_download_url = downloadUrl
        installer_name = downloadUrl.split('/')[-1]
        print(firefox_download_url, installer_name, sep='\n')
    except Exception as e:
        print("Failed to capture downloadUrl", e)
        abort(500, description="Failed to capture DownloadUrl.")

    attempts = 0
    # installer_name = "firefox.tar.bz2"
    # firefox_download_url = "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"


    import os
    import shutil
    try:
        import json
        with open('config.json', 'r') as file:
            config = json.load(file)
        folder_path = config["firefoxPath"]
        installPath = config["installPath"]

        print(f"Firefox Path: {folder_path}")
        print(f"Install Path: {installPath}")
    except:
        print("Could not fetch Firefox Path")
        abort(500, description="Invalid Configuration")

    try:
        print("TRYING PATH")
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        print("TRYING PATH FAILED")
        print("Failed to establish download path.")
        print(e)
        abort(500, description="Invalid Download Path")

    while True:
        print("Downloading Firefox...")
        response = requests.get(firefox_download_url, stream=True)
        try:
            if response.status_code == 200:
                with open(installer_name, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded {installer_name}")
                break
            else:
                attempts += 1
                print("Failed to download Firefox.")
                if attempts >= MAX_ATTEMPTS:
                    abort(500, description="Failed to download Firefox.")
                time.sleep(SLEEP_TIME)
        except Exception as e:
            attempts += 1
            print("Failed to download firefox: ", e)
            if attempts >= MAX_ATTEMPTS:
                abort(500, description="Failed to download Firefox.")
            time.sleep(SLEEP_TIME)

    try:
        extract_command = ["tar", "-xjf", installer_name, "-C", installPath]
        subprocess.run(extract_command)
        return jsonify("")
    except:
        print("Failed to extract files.")
        abort(500, description="Failed to extract files.")


@app.route('/start', methods=['GET'])
def start_scan():
    attempts = 0

    command = ["firefox", "--version"]
    version = None
    print("Scan Started")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        version = result.stdout.split()[-1]
        print(version)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        abort(500, e)
    result = search_nvd_vulnerabilities(version)
    data = []
    for item in result:
        cve_id = item["cve"]["id"]
        vuln_status = item["cve"]["vulnStatus"]
        published = item["cve"]['published']
        lastModified = item["cve"]['lastModified']
        cvss_data = item.get("cve", {}).get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {})
        cvss_data_v2 = item.get("cve", {}).get("metrics", {}).get("cvssMetricV2", [{}])[0].get("cvssData", {})
        cvss_metrics = item.get("cve", {}).get("metrics", {}).get("cvssMetricV2", [{}])
        base_score = cvss_data.get("baseScore", "N/A")
        if base_score == "N/A":
            base_score = cvss_data_v2.get("baseScore", "N/A")
        base_severity = cvss_data.get("baseSeverity", "N/A")
        if base_severity == "N/A":
            base_severity = cvss_metrics[0].get("baseSeverity", "N/A")

        description = item["cve"]["descriptions"][0]["value"]

        data.append((cve_id, vuln_status, base_score, base_severity, description, published,  lastModified))
    

    return jsonify(data)


def search_nvd_vulnerabilities(version, api_key=None):
    attempts = 0
    api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    headers = {}
    if api_key:
        headers["apiKey"] = api_key

    params = {
        "virtualMatchString": FIREFOX_CPE,
        "versionStart": version,
        "versionStartType": 'including',
        "versionEnd": version,
        "versionEndType": 'including'
    }

    all_records = []
    while True:
        try:
            response = requests.get(api_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "vulnerabilities" in data:
                vulnerabilities = data["vulnerabilities"]
                all_records.extend(vulnerabilities)
                print(f"Fetched {len(vulnerabilities)} records. Total so far: {len(all_records)}")
            else:
                print("No vulnerabilities found.")
            break
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}", "attempts: ", attempts)
            attempts += 1
            if attempts >= MAX_ATTEMPTS:
                abort(500, description="Failed to connect to NVD database.")
            time.sleep(SLEEP_TIME)

    return all_records


if __name__ == '__main__':
    app.run(port=5000, debug=False)