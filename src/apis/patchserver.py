import sqlite3
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

SQLITE_FIREFOX_DB = 'firefox_releases.db'

def get_db_connection():
    try:
        conn = sqlite3.connect(SQLITE_FIREFOX_DB)
        conn.row_factory = sqlite3.Row
        return conn
    except:
        print("Failed to establish connection with DB.")
        return None

@app.route('/process_cvid', methods=['GET'])
def get_records_and_install():
    try:
        text = request.args.get('cvid', default='', type=str)
        conn = get_db_connection()
        cursor = conn.cursor()
        print(text)
        cursor.execute("SELECT link FROM vuln WHERE vul like ? ORDER BY VERSION ASC LIMIT 1", ('%' + text + '%',))
        records = cursor.fetchall()
        records_list = [dict(record) for record in records]

        conn.close()

        try:
            url = "http://127.0.0.1:5000/install"
            params = {
                'downloadUrl': records_list[0]['link']
            }
            print("REQUESTING")
            response = requests.get(url, params=params)
            print(response.text)
            print(response.status_code)
            response.raise_for_status()
        except Exception as e:
            print("Failed to download via patchserver", e)
            abort(500, description="Failed to download.")
        return jsonify()
    except:
        print("Failed to fetch records from DB.")
        abort(500, description="Failed to fetch records from the database.")


if __name__ == '__main__':
    app.run(port=8000, debug=False)