import json
from datetime import datetime
import os


def add_custom_profile(json_file_path, profile_id, profile_name, profile_version_id, profile_type,
                       profile_icon="Grass"):
    try:
        # Read existing JSON content
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Generate timestamp for "created" and "lastUsed" fields
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        # Add the new profile entry
        data["profiles"][profile_id] = {
            "created": timestamp,
            "gameDir": os.path.join(os.environ['APPDATA'], '.minecraft'),
            "icon": profile_icon,
            "lastUsed": "1970-01-01T00:00:00.000Z",
            "lastVersionId": profile_version_id,
            "name": profile_name,
            "type": profile_type
        }

        # Write the modified data back to the JSON file
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=2)

        # print(f"Custom profile! '{profile_name}' added to '{json_file_path}'.")
        print(f'Create profile! name\'s {profile_name}')
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {json_file_path}")
