# ExoCAD db healer

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg) ![License](https://img.shields.io/badge/License-GPLv3-blue.svg)

ExoCAD db healer is a graphical tool designed specifically for situations where you've changed the project naming format in ExoCAD, causing old project paths to break. This application isn’t meant to simply organize or simplify — it’s built to fix the folder structure inside your CAD-Data directory. It automatically renames existing project folders to match the naming convention defined in your current defaultsettings.cfg, restoring consistency and functionality to your ExoCAD database.

## Features

- **Customizable Renaming**: Utilize ExoCAD settings files to define the folder name format. Supports `<FilenameTemplate>` and `<PathTemplate>` tags.
- **Automatic Data Extraction**: The application automatically extracts necessary information (patient name, date, etc.) from `.dentalProject` files.
- **Multiple Language Support**: The user interface is available in English, Russian, and Spanish.
- **Easy-to-Use GUI**: Intuitive graphical interface built with PyQt6.
- **Error Handling**: Provides warnings and error messages to keep the user informed about the process.

## Screenshot

![ExoCAD db healer Screenshot](https://i.ibb.co/Wvq4Dwh0/Screenshot-2025-04-15-094004.png)


## Compiled Release

A pre-built executable version of **ExoCAD db healer** is available for users who prefer not to install Python or manage dependencies.

### Features

- No installation required. Download and run directly.
- Built-in GUI with full functionality identical to the source version.
- Supports Windows systems. Versions for Linux and macOS may follow.

### Download

The compiled build can be downloaded here:  
**[Download ExoCAD db healer - Windows Build](https://github.com/zer0ltrnce/exodbhealer/releases/tag/exocaddbhealer)**

## Installation

1. Install Python 3.6 or later: [Download Python](https://www.python.org/downloads/)
2. Install the PyQt6 library:

   ```bash
   pip install PyQt6
Download the project files (exocad_db_healer.py and any other necessary files) from the GitHub repository.

Usage
Run the application by executing the following command in your terminal:

bash
Copy
Edit
python exocad_db_healer.py
Step 1: Format Settings File
Click the "Browse..." button and select your ExoCAD XML settings file containing either <FilenameTemplate> or <PathTemplate> tags. The application will attempt to detect the folder name format and display it.

Step 2: ExoCAD Projects Folder
Click the "Browse..." button and select the folder containing subfolders with .dentalProject files.

Step 3: Execution
Click the "Perform Rename" button. The application will ask for confirmation and then begin the renaming process.

The status of the process and the results will be displayed in the status bar and in a dialog box upon completion.

Language Support
To change the interface language, use the "Language" menu in the application's main menu.

License
This project is distributed under the GNU General Public License v3.0.

Contact
Created by David Kamarauli (smiledesigner.us)
Instagram: @davidkamaraulli
 
