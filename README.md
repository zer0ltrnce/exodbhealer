ExoCAD db healer
![alt text](https://img.shields.io/badge/Python-3.6+-blue.svg)

![alt text](https://img.shields.io/badge/License-GPLv3-blue.svg)
ExoCAD db healer is a graphical user interface (GUI) tool developed to simplify the organization and management of ExoCAD project folders. The application allows you to automatically rename project folders based on information contained within ExoCAD settings files (XML) and .dentalProject files.
Features
Customizable Renaming: Utilize ExoCAD settings files to define the folder name format. Supports <FilenameTemplate> and <PathTemplate> tags.
Automatic Data Extraction: The application automatically extracts necessary information (patient name, date, etc.) from .dentalProject files.
Multiple Language Support: The user interface is available in English, Russian, and Spanish.
Easy-to-Use GUI: Intuitive graphical interface built with PyQt6.
Error Handling: Provides warnings and error messages to keep the user informed about the process.
Screenshot (optional)
You can add a screenshot of the running application for better visual representation. Replace path/to/screenshot.png with the actual path to your image.
<p align="center">
<img src="path/to/screenshot.png" alt="ExoCAD db healer Screenshot" width="600">
</p>
Installation
Install Python 3.6 or later: https://www.python.org/downloads/
Install the PyQt6 library:
Open your terminal or command prompt and run:
pip install PyQt6
Use code with caution.
Bash
Download the project files (exocad_db_healer.py and any other files) from the GitHub repository.
Usage
Run the application by executing the following command in your terminal:
python exocad_db_healer.py
Use code with caution.
Bash
Step 1: Format Settings File. Click the "Browse..." button and select your ExoCAD XML settings file containing either <FilenameTemplate> or <PathTemplate> tags. The application will attempt to detect the folder name format and display it.
Step 2: Exocad Projects Folder. Click the "Browse..." button and select the folder containing subfolders with .dentalProject files.
Step 3: Execution. Click the "Perform Rename" button. The application will ask for confirmation and then begin the renaming process.
The status of the process and the results will be displayed in the status bar and in a dialog box upon completion.
Language Support
To change the interface language, use the "Language" menu in the application's main menu.
License
This project is distributed under the GNU General Public License v3.0.
Contact
Created by David Kamarauli (smiledesigner.us) | Instagram: @davidkamaraulli
