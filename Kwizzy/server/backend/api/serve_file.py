from flask import send_from_directory, abort
from werkzeug.utils import safe_join
from flask_restful import Resource
from flask import current_app
import os
from .. import cache


class FileApi(Resource):
    def get(self, filename):
        try:
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            # Convert to absolute path if it's relative
            if not os.path.isabs(upload_folder):
                upload_folder = os.path.abspath(upload_folder)

            # Ensure the file exists
            file_path = safe_join(upload_folder, filename)
            if not os.path.exists(file_path):
                print(f"File not found at: {file_path}")
                abort(404, description="File not found")

            return send_from_directory(upload_folder, filename)
        except Exception as e:
            print(f"Error: {str(e)}")
            abort(404, description="File not found")
