#!/bin/bash

# gunicorn -w 4 -b 0.0.0.0:5000 src/apis/vuln:app
python src/apis/vuln.py &
VULN_PID=$!
echo "vuln.py running with PID: $VULN_PID" >> running.info


# gunicorn -w 4 -b 0.0.0.0:8000 src/apis/patchserver:app
python src/apis/patchserver.py &
PATCHSERVER_PID=$!
echo "patchserver.py running with PID: $PATCHSERVER_PID" >> running.info

npm run react-start &
REACT_PID=$!
echo "react-start running with PID: $REACT_PID" >> running.info
