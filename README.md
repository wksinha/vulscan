# vulscan

- Ensure nodejs, npm, python and pip are installed
- Install requisite packages from npm (run the following command from the vulscan directory).
```
npm i
```
- Install requisite packages from pip (run the following command from the vulscan/src/apis directory).
```
pip install -r requirements.txt
```

- Configure the location for firefox (vulscan/src/apis/config.json) and ensure it is part of the PATH variable.
- Run patch.py (To crawl Firefox patch information)
- Run patchserver (cd into src/apis and run the following)
```
gunicorn -w 4 -b 0.0.0.0:8000 patchserver:app
```

- Run vuln-server (cd into src/apis and run the following)
```
gunicorn -w 4 -b 0.0.0.0:5000 vuln:app
```

- Start the application (cd into vulnscan and run the following)
```
npm run react-start
```