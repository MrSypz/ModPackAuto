import os
import requests
from zipfile import ZipFile


def download_and_extract(url, download_path, extract_to):
    response = requests.get(url)

    if response.status_code == 200:
        # Save the downloaded content to a file
        zip_file_path = os.path.join(download_path, "downloaded_file.zip")
        with open(zip_file_path, 'wb') as zip_file:
            zip_file.write(response.content)

        # Extract the contents of the ZIP file
        with ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        # Remove the downloaded ZIP file
        os.remove(zip_file_path)

        print(f"Download and extraction successful.")
    else:
        print(f"Failed to download content from {url}. Status code: {response.status_code}")


def check_and_download_folder(folder_path, download_url, extract_to):
    if not os.path.exists(folder_path):
        print(f"Folder does not exist. Downloading and extracting contents...")

        # Create the folder if it doesn't exist
        os.makedirs(folder_path)

        # Download and extract the contents
        download_and_extract(download_url, folder_path, extract_to)
    else:
        print(f"Folder version. ->{folder_path}. already exists.")
