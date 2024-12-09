import sqlite3
import platform
import os
import json
import subprocess

DB_FILE = 'assets.db'

def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            os TEXT,
            os_version TEXT,
            cpu TEXT,
            memory INTEGER,
            disk INTEGER,
            network TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_memory_info():
    return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')

def get_disk_info():
    statvfs = os.statvfs('/')
    return statvfs.f_frsize * statvfs.f_blocks

def get_network_info():
    result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
    return result.stdout

def get_it_info():
    os_info = platform.system()
    os_version = platform.version()
    cpu_info = platform.processor()
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    network_info = get_network_info()

    it_info = {
        "os": os_info,
        "os_version": os_version,
        "cpu": cpu_info,
        "memory": memory_info,
        "disk": disk_info,
        "network": network_info
    }

    return it_info

def update_database(it_info):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO assets (os, os_version, cpu, memory, disk, network)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (it_info["os"], it_info["os_version"], it_info["cpu"],
          it_info["memory"], it_info["disk"], it_info["network"]))
    
    conn.commit()
    conn.close()

def main():
    initialize_database()
    it_info = get_it_info()
    update_database(it_info)

    print(json.dumps(it_info, indent=4))

if __name__ == "__main__":
    main()
