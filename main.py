import os
import shutil
import requests
import tkinter as tk
from tkinter import filedialog

import customprofile
import filehandler


def choose_minecraft_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    initial_dir = os.path.join(os.environ['APPDATA'])
    mcchecker_path = filedialog.askdirectory(title="Select Minecraft Path", initialdir=initial_dir)
    return mcchecker_path


mc_path = choose_minecraft_path()
verions = os.path.join(mc_path, 'versions' + '\\fabric-loader-0.15.3-1.20.1')
verions_path = os.path.join(mc_path, 'versions')
mods_path = os.path.join(mc_path, 'mods')
modpack_version_path = os.path.join(mc_path, 'modpackversion')
modpack_version_file = os.path.join(modpack_version_path, 'version.txt')

_version_ = '1.1'
_version_client_ = '1.0'


def check_mc(mc_path):
    if os.path.exists(mc_path):
        if os.path.exists(modpack_version_file):
            try:
                with open(modpack_version_file, "r") as file:
                    content = file.read()
            except FileNotFoundError:
                print(f"File not found: {modpack_version_file}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            os.makedirs(modpack_version_path, exist_ok=True)
            with open(modpack_version_file, "w") as file:
                file.write(_version_client_)

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


def version_updater(version):
    if os.path.exists(modpack_version_file):
        with open(modpack_version_file, "w") as file:
            file.write(version)


def read_modpack_version():
    try:
        with open(modpack_version_file, "r") as file:
            version = file.read().strip()  # Strip to remove leading/trailing whitespaces
            return version
    except FileNotFoundError:
        print(f"File not found: {modpack_version_file}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the modpack version file: {e}")
        return None


if __name__ == "__main__":
    mod_url = 'https://raw.githubusercontent.com/MrSypz/ModPackAuto/main/container/modfile.zip'
    if not mc_path:
        print("No Minecraft path selected. Exiting.")
    else:
        mods_path = check_mc(mc_path)
        versionmodpack_url = 'https://raw.githubusercontent.com/MrSypz/ModPackAuto/main/container/modpackversion'
        latest_version = version_modpack(versionmodpack_url)

        versionloader_url = 'https://raw.githubusercontent.com/MrSypz/ModPackAuto/main/container/modversion.zip'
        filehandler.check_and_download_folder(verions, versionloader_url, verions_path)

        print('Half Way Done!!')


        # Function to validate input for creating a profile
        def validate_profile_input():
            while True:
                check = input('Do you want to create a new profile? (Y/N): ').lower()
                if check in {'y', 'n'}:
                    return check
                else:
                    print('Invalid input. Please enter Y or N.')


        check = validate_profile_input()

        if check == 'y':
            print('-Create a Profile Part-')
            print('Enter Your Profile Name')
            json_file_path = os.path.join(os.environ['APPDATA'], '.minecraft', 'launcher_profiles.json')
            profile_id = 'bfc89f1e92619f7ecca11732017a4e33'
            profile_name = input()
            profile_version_id = 'fabric-loader-0.15.3-1.20.1'
            profile_type = 'custom'

            customprofile.add_custom_profile(json_file_path, profile_id, profile_name, profile_version_id, profile_type)
        else:
            print('Skipping the profile creation part.')


        # Function to validate input for downloading the modpack
        def validate_modpack_download():
            while True:
                downloadcheck = input('Do you want to download modpack? (Y/N): ').lower()
                if downloadcheck in {'y', 'n'}:
                    return downloadcheck
                else:
                    print('Invalid input. Please enter Y or N.')


        if validate_modpack_download() == 'y':
            print('-Download Modpack Part-')
            print(f'Your modpack version is {read_modpack_version()} latest version is {latest_version}')
            print('Downloading a Mod.')
            filehandler.download_and_extract(mod_url, mc_path, mods_path)
            version_updater(latest_version)
        else:
            print('Skipping the modpack download part.')
            print('You didn\'t download anything why?')

        print(f'Your ModPack version is {read_modpack_version()}')
        print(f'Finish!! Enjoy Your Game.')
