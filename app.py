#This is where the magic happens
from flask import Flask, request, jsonify, send_file, g
import os
import yt_dlp
from flask_cors import CORS
import tempfile
import time
from pathvalidate import sanitize_filename

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"], expose_headers=["Content-Disposition"])

# Directory for temporary files
DOWNLOAD_FOLDER = tempfile.gettempdir()

# Register after_request at the app level
@app.after_request
def cleanup_file(response):
    # Check if file_path is set in the request context
    file_path = getattr(g, 'file_path_to_delete', None)
    if file_path and os.path.exists(file_path):
        try:
            time.sleep(2)  # Small delay to ensure file is sent
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file: {e}")
    return response

@app.route("/")
def index():
    return "YouTube to MP3 Converter YEAHHH"

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(id)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_id = info.get("id", None)
            video_title = info.get("title", None)

            if not video_id:
                return jsonify({"error": "Could not extract video ID"}), 500
            # filename = f"{video_id}.mp3"
            # file_path = os.path.join(DOWNLOAD_FOLDER, filename)
            # if not os.path.exists(file_path):
            #     return jsonify({"error": "Converted file not found"}), 500
            if not video_id:
                return jsonify({"error": "Could not extract video ID"}), 500
            if not video_title:
                print("No video title found.")
                video_title = video_id
        # return jsonify({"filename": filename}), 200

      # Sanitize the title to create a valid filename
            sanitized_title = sanitize_filename(video_title)
            filename = f"{sanitized_title}.mp3"
            # Rename the downloaded file to use the sanitized title
            original_file = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp3")
            new_file = os.path.join(DOWNLOAD_FOLDER, filename)
            if os.path.exists(original_file):
                os.rename(original_file, new_file)
            else:
                return jsonify({"error": "Converted file not found"}), 500

        return jsonify({"filename": filename, "title": video_title}), 200

    except yt_dlp.utils.DownloadError as e:
        print(f"yt_dlp DownloadError: {str(e)}")
        return jsonify({"error": f"Download failed: {str(e)}"}), 500
    except Exception as e:
        print(f"General error during conversion: {str(e)}")
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    try:
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return jsonify({"error": "File not found"}), 404

        # Store file path in request context for cleanup
        g.file_path_to_delete = file_path

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype="audio/mpeg"
        )
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    #running python app.py with debug=True. Helps with debugging
    app.run(port=5000, debug=True)