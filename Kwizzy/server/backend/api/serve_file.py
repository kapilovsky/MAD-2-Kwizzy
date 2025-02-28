from flask import send_from_directory, abort, current_app
from werkzeug.utils import safe_join
from flask_restful import Resource
import os


class FileApi(Resource):
    def get(self, filename):
        try:
            # Get the application root directory (where your app is located)
            app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            # Construct the upload folder path relative to app root
            # Remove the leading './' if present in UPLOAD_FOLDER
            relative_path = current_app.config["UPLOAD_FOLDER"].lstrip("./")
            upload_folder = os.path.join(app_root, relative_path)

            # Ensure the directory exists
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder, exist_ok=True)

            # Safely join the path and filename
            file_path = safe_join(upload_folder, filename)
            if not os.path.exists(file_path):
                print(f"File not found at: {file_path}")
                abort(404, description="File not found")

            # Get the directory containing the file
            directory = os.path.dirname(file_path)
            # Get just the filename
            basename = os.path.basename(file_path)

            return send_from_directory(directory, basename)

        except Exception as e:
            print(f"Error: {str(e)}")
            abort(404, description="File not found")
