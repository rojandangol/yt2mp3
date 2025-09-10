# YouTube to MP3 Converter

- Note: This project was built with AI assistance in about an hour for educational purposes.
- A simple web application that converts YouTube videos to MP3 files using Flask, yt-dlp, and JavaScript. Host your own converter and avoid relying on online services!

# What It Does

- Takes a YouTube URL via a web interface and converts the video to an MP3 file.
- Uses yt-dlp to download and convert the audio, served via a Flask backend.
- Triggers a browser download using JavaScript, providing a seamless experience.

# Dependencies

- Python 3.6 or higher
- Python packages (installed via pip):
- flask==2.3.2: Web framework for the backend.
- yt-dlp==2023.7.6: Downloads and converts YouTube videos.
- flask-cors==4.0.0: Handles cross-origin requests.
- ffmpeg-python==0.2.0: Python bindings for FFmpeg (optional, for future use).

- FFmpeg: A system-level dependency for audio conversion (not a Python package).

# Setup Instructions

- Clone the Repository.


- Start the Flask Server: python app.py. (The server runs on http://127.0.0.1:5000.)

- Run the Frontend:

- Open index.html in a browser, or use a live server (e.g., VS Code Live Server) on http://127.0.0.1:5500.
- Enter a YouTube URL and click "Convert" to download the MP3.

- Manual FFmpeg Installation (if needed)
- Mac: brew install ffmpeg

- Ubuntu/Debian:sudo apt update : sudo apt install -y ffmpeg

- Windows:
- Download FFmpeg from ffmpeg.org.
- Extract the archive and add the bin folder to your system PATH.
- Or, with Chocolatey: choco install ffmpeg

- Verify: Run ffmpeg -version to confirm installation.

# Files

- app.py: Flask backend for converting YouTube videos to MP3.
- script.js: JavaScript frontend for sending URLs and triggering downloads.
- index.html: HTML frontend for user input.
- requirements.txt: Python dependencies.

# Lessons Learned

- Flask after_request Issue: Flask does not allow registering after_request hooks dynamically after the app starts, causing a 500 Internal Server Error and "Failed to fetch" in JavaScript. Fixed by using a top-level @app.after_request with Flask’s g object for file cleanup.

- Server-Side Errors: The original /convert route combined conversion and file serving, leading to "Failed to fetch" if yt-dlp or FFmpeg failed (e.g., missing FFmpeg, invalid URL). Splitting into /convert (JSON response) and /download (file serving) made debugging easier.

- CORS Handling: Proper CORS configuration with flask-cors was essential to allow the frontend (http://127.0.0.1:5500) to communicate with the backend (http://127.0.0.1:5000).

# Helpful Resources

- Flask Documentation: Learn about Flask routes, send_file, and request handling.
- yt-dlp GitHub: Guide for using yt-dlp to download and convert YouTube videos.
- FFmpeg Installation Guide: Official instructions for installing FFmpeg on various systems.
- Understanding CORS: Explains CORS for cross-origin requests between frontend and backend.
- How to Download Files with JavaScript: Covers triggering browser downloads with anchor tags.
- Debugging Flask Applications: Tips for debugging Flask server errors.
- Adding FFmpeg to PATH on Windows: Step-by-step guide for Windows users.

# Notes

- Legal: This is for educational use only. Respect YouTube’s Terms of Service and copyright laws.
- Temporary Files: MP3 files are stored in the system temp directory and deleted after download.
- FFmpeg Clarification: pip install ffmpeg installs Python bindings (ffmpeg-python), but the FFmpeg binary is still - required for yt-dlp.

# Troubleshooting

- "Failed to fetch" error: Check Flask logs (python app.py) and browser DevTools (Network/Console tabs) for errors like yt-dlp failures or CORS issues.

- FFmpeg not found: Verify FFmpeg is in your PATH (ffmpeg -version). Install it manually if setup.py fails.

- CORS issues: Ensure the frontend runs on http://127.0.0.1:5500 and CORS is configured correctly in app.py.

