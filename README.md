# ExoCAD db healer

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg) ![License](https://img.shields.io/badge/License-GPLv3-blue.svg)

ExoCAD db healer is a graphical user interface (GUI) tool developed to simplify the organization and management of ExoCAD project folders. The application allows you to automatically rename project folders based on information contained within ExoCAD settings files (XML) and `.dentalProject` files.

## Features

- **Customizable Renaming**: Utilize ExoCAD settings files to define the folder name format. Supports `<FilenameTemplate>` and `<PathTemplate>` tags.
- **Automatic Data Extraction**: The application automatically extracts necessary information (patient name, date, etc.) from `.dentalProject` files.
- **Multiple Language Support**: The user interface is available in English, Russian, and Spanish.
- **Easy-to-Use GUI**: Intuitive graphical interface built with PyQt6.
- **Error Handling**: Provides warnings and error messages to keep the user informed about the process.

## Screenshot

![ExoCAD db healer Screenshot](https://i.ibb.co/Wvq4Dwh0/Screenshot-2025-04-15-094004.png)

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

makefile
Copy
Edit
::contentReference[oaicite:0]{index=0}
 
