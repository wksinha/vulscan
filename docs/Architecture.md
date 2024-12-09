# Architecture

## UI
- Allows user to interact and control actions
    - Initiate Scan
    - Request Patch

## Vulnerability Scanner and Patcher
- Asset Detection Module scans the system for assets/products (firefox) and their versions.
- Vulnerability Scanning Module scans the NVD api for the product/version.

## Patching Server
- Downloader/Parser that crawls the product (firefox) website for changes.
- Scheduler (cronjob) running the above periodically.
- Database (SQLite) that holds the crawled information (package CVID fixes, download links)
- REST API endpoints for service exposure.