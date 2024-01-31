import os
import shutil
import requests
import tkinter as tk
from tkinter import filedialog

import customprofile
import versioncheck

mc_path = os.path.join(os.environ['APPDATA'], '.minecraft')
verions = os.path.join(mc_path, 'versions' + '\\fabric-loader-0.15.3-1.20.1')
verions_path = os.path.join(mc_path, 'versions')
mods_path = os.path.join(mc_path, 'mods')


def choose_minecraft_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    initial_dir = os.path.join(os.environ['APPDATA'])
    mcchecker_path = filedialog.askdirectory(title="Select Minecraft Path", initialdir=initial_dir)
    return mcchecker_path


def check_mc(mc_path):
    if os.path.exists(mc_path):
        mods_path = os.path.join(mc_path, 'mods')
        if os.path.exists(mods_path):
            print('Warning: It needs to clear the folder. Do you want to backup your old mods? Y/N')
            do_backup = input().lower()
            if do_backup == 'n':
                shutil.rmtree(mods_path)
                os.makedirs(mods_path)
                print("Cleared the 'mods' folder.")
            elif do_backup == 'y':
                backup_path = os.path.join(mc_path, 'old_mods')
                shutil.copytree(mods_path, backup_path)
                print(f"Backup created at: {backup_path}")
                shutil.rmtree(mods_path)
                os.makedirs(mods_path)
                print("Cleared the 'mods' folder and created a backup.")
        else:
            os.makedirs(mods_path)
        return mods_path
    else:
        print("Could not find the specified Minecraft path.")
        return False


def version_modpack(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        text_content = response.text

        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error reading the text file from the URL: {e}")
        return None


def version_checker(latest, present):
    try:
        present_float = float(present)
        latest_float = float(latest)

        if present_float == latest_float:
            print(f'Your version is the latest: {latest}')
        elif present_float < latest_float:
            print(f'Your version is not up to date. Latest version is: {latest} pls update your modpack.')

        else:
            print(f'Your version is ahead of the latest: {present} that mean this one is impossible!!')
    except ValueError:
        print("Invalid version format. Please provide valid version numbers.")


if __name__ == "__main__":
    mcchecker_path = choose_minecraft_path()
    if not mc_path:
        print("No Minecraft path selected. Exiting.")
    else:
        mods_path = check_mc(mcchecker_path)

        versionmodpack_url = 'https://raw.githubusercontent.com/MrSypz/ModPackAuto/main/container/modpackversion'  # Replace with the actual URL of the text file
        latest_version = version_modpack(versionmodpack_url)
        present_version = '1.0'
        version_checker(latest_version, present_version)

        versionloader_url = 'https://raw.githubusercontent.com/MrSypz/ModPackAuto/main/container/modversion.zip'  # Version of game exam fabric version 1.20.1
        versioncheck.check_and_download_folder(verions, versionloader_url, verions_path)

        print('Half Way Done!!')
        print('Do you want to create new profile(First time use request to create) Y/N')
        check = input().lower()  # Convert input to lowercase for case-insensitive comparison

        if check == 'y':
            print('Create a Profile Part')
            print('Enter Your Profile Name')
            json_file_path = os.path.join(os.environ['APPDATA'], '.minecraft', 'launcher_profiles.json')
            profile_id = 'bfc89f1e92619f7ecca11732017a4e33'
            profile_name = input()
            profile_version_id = 'fabric-loader-0.15.3-1.20.1'
            profile_type = 'custom'

            customprofile.add_custom_profile(json_file_path, profile_id, profile_name, profile_version_id, profile_type)
        elif check == 'n':
            print('Skip creating a profile part.')
        else:
            print('Invalid input. Please enter Y or N.')

        mod_url = 'https://raw.githubusercontent.com/MrSypz/ModPackAuto/main/container/modfile.zip'
        downloadcheck = input().lower()
        if downloadcheck == 'y':
            print('Downloading a Mod.')
            versioncheck.download_and_extract(mod_url, mc_path, mods_path)
        elif downloadcheck == 'n':
            print('skip loading mod')
        else :
            print('invalid input.')
        print(f'Finish!! Enjoy Your Game.Modpack version {latest_version}')
    pass
