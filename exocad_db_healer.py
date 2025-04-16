import sys
import os
import webbrowser
import xml.etree.ElementTree as ET
from datetime import datetime
import re
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox, QStatusBar, QSizePolicy,
    QSpacerItem, QStyle, QFrame, QMenuBar, QMenu
)
from PyQt6.QtGui import QPalette, QColor, QIcon, QPixmap, QDesktopServices, QFont, QAction, QActionGroup
from PyQt6.QtCore import Qt, QSize, QUrl

PROFESSIONAL_DARK_STYLE = """
QMainWindow { background-color: #20232a; }
QWidget#CentralWidget { background-color: #20232a; color: #c8cdd4; font-size: 10pt; }
QLabel { color: #c8cdd4; padding-bottom: 3px; }
QLabel#StepLabel { font-weight: bold; color: #9cb0c9; margin-top: 5px; }
QLabel#CopyrightLabel { color: #636d83; font-size: 8pt; margin-top: 10px; }
QLabel#CopyrightLabel a { color: #569cd6; text-decoration: none; }
QLabel#CopyrightLabel a:hover { text-decoration: underline; }
QLineEdit { background-color: #2c313a; border: 1px solid #4a5263; padding: 7px; border-radius: 3px; color: #dde1e8; min-height: 20px; }
QLineEdit:read-only { background-color: #262a33; color: #7f8a9f; }
QPushButton.BrowseButton { background-color: #3a404d; color: #c8cdd4; border: 1px solid #4a5263; padding: 7px 12px; border-radius: 3px; min-height: 20px; }
QPushButton.BrowseButton:hover { background-color: #4a5263; border-color: #569cd6; }
QPushButton.BrowseButton:pressed { background-color: #333842; }
QPushButton.BrowseButton:disabled { background-color: #333842; color: #636d83; border-color: #3a404d; }
QPushButton#ActionButton { background-color: #569cd6; color: #ffffff; font-size: 12pt; font-weight: bold; padding: 10px 30px; border-radius: 4px; border: 1px solid #4a8bc5; min-height: 28px; }
QPushButton#ActionButton:hover { background-color: #4a8bc5; border-color: #569cd6; }
QPushButton#ActionButton:pressed { background-color: #3a7ab0; }
QPushButton#ActionButton:disabled { background-color: #3a4f6a; color: #7f8a9f; border-color: #3a4f6a; }
QStatusBar { color: #7f8a9f; font-size: 9pt; background-color: #20232a; border-top: 1px solid #3a404d;}
QStatusBar::item { border: none; }
QFrame.hline { border: none; border-top: 1px solid #3a404d; height: 1px; margin: 12px 0px; }
QLabel.StatusIndicator { min-width: 20px; max-width: 20px; min-height: 20px; max-height: 20px; margin-left: 5px; }
QMenuBar { background-color: #2c313a; color: #c8cdd4; border-bottom: 1px solid #4a5263;}
QMenuBar::item { background-color: transparent; padding: 4px 10px; }
QMenuBar::item:selected { background-color: #4a5263; }
QMenuBar::item:pressed { background-color: #3a404d; }
QMenu { background-color: #2c313a; color: #c8cdd4; border: 1px solid #4a5263; }
QMenu::item { padding: 5px 20px; }
QMenu::item:selected { background-color: #4a5263; }
QMenu::separator { height: 1px; background-color: #4a5263; margin: 4px 0px; }
QMessageBox { background-color: #2c313a; }
QMessageBox QLabel { color: #c8cdd4; }
QMessageBox QPushButton { background-color: #3a404d; color: #c8cdd4; border: 1px solid #4a5263; min-width: 80px; padding: 7px 12px; border-radius: 3px; min-height: 20px; }
QMessageBox QPushButton:hover { background-color: #4a5263; border-color: #569cd6; }
QMessageBox QPushButton:pressed { background-color: #333842; }
"""

TRANSLATIONS = {
    "ru": {
        "window_title": "ExoCAD db healer", "menu_language": "Язык", "lang_ru": "Русский", "lang_en": "English",
        "lang_es": "Español",
        "step1_label": "1. Файл настроек формата:", "settings_placeholder": "Выберите XML файл настроек...",
        "settings_tooltip": "XML файл с тегами <FilenameTemplate> или <PathTemplate>",
        "browse_button": "Обзор...", "settings_browse_tooltip": "Выбрать файл настроек",
        "format_label": "Обнаруженный формат имени:", "format_placeholder": "...",
        "format_tooltip": "Формат имени папки из файла настроек",
        "step2_label": "2. Папка с проектами Exocad:", "projects_placeholder": "Выберите папку с проектами...",
        "projects_tooltip": "Папка, содержащая подпапки с файлами .dentalProject",
        "projects_browse_tooltip": "Выбрать папку с проектами",
        "step3_label": "3. Выполнение:", "action_button": "Выполнить Переименование",
        "action_button_tooltip": "Запустить переименование папок в выбранной директории",
        "status_ready": "Готов.", "status_select_settings": "Выберите файл настроек формата.",
        "status_format_not_found": "Не найден формат в файле настроек.",
        "status_select_projects": "Выберите папку с проектами.", "status_ready_to_run": "Готов к переименованию.",
        "status_running": "Идет процесс... Сканирование папок...",
        "status_scan_error": "Ошибка сканирования: {error}", "status_no_folders": "Папки проектов не найдены.",
        "status_found_folders": "Найдено {count} папок. Переименование...",
        "status_renaming": "Переименовано {done}/{total}...",
        "status_finished": "Готово. Переименовано: {renamed}, Пропущено: {skipped}, Ошибки: {errors}",
        "msg_box_error_title": "Ошибка", "msg_box_warning_title": "Предупреждение", "msg_box_info_title": "Информация",
        "msg_box_question_title": "Подтверждение",
        "msg_missing_input": "Выберите файл настроек, папку проектов и убедитесь, что формат загружен.",
        "msg_confirm_rename": "Переименовать папки в:\n{folder}\n\nИспользуя формат:\n{format}\n\nПродолжить?",
        "msg_scan_error": "Ошибка при сканировании папки проектов:\n{error}",
        "msg_no_folders_found": "Подходящие папки проектов не найдены в:\n{folder}",
        "msg_rename_complete": "Операция завершена.\n\nПереименовано: {renamed}\nПропущено: {skipped}\nОшибки: {errors}\n--------------------\nВсего найдено: {total}",
        "msg_check_console": "\n\nСм. консоль для деталей ошибок.",
        "tooltip_indicator_ok": "OK", "tooltip_indicator_error_format": "Ошибка: формат не найден",
        "tooltip_indicator_no_settings": "Файл не выбран", "tooltip_indicator_no_projects": "Папка не выбрана",
        "copyright_text": '<html><body><p align="center">Created by David Kamarauli (<a href="http://smiledesigner.us/">smiledesigner.us</a> | Inst: <a href="https://www.instagram.com/davidkamaraulli/">@davidkamaraulli</a>)</p></body></html>',
    },
    "en": {
        "window_title": "ExoCAD db healer", "menu_language": "Language", "lang_ru": "Русский", "lang_en": "English",
        "lang_es": "Español",
        "step1_label": "1. Format Settings File:", "settings_placeholder": "Select settings XML file...",
        "settings_tooltip": "XML file with <FilenameTemplate> or <PathTemplate> tags",
        "browse_button": "Browse...", "settings_browse_tooltip": "Select settings file",
        "format_label": "Detected Name Format:", "format_placeholder": "...",
        "format_tooltip": "Folder name format from the settings file",
        "step2_label": "2. Exocad Projects Folder:", "projects_placeholder": "Select projects folder...",
        "projects_tooltip": "Folder containing subfolders with .dentalProject files",
        "projects_browse_tooltip": "Select Exocad projects folder",
        "step3_label": "3. Execution:", "action_button": "Perform Rename",
        "action_button_tooltip": "Start renaming folders in the selected directory",
        "status_ready": "Ready.", "status_select_settings": "Select the format settings file.",
        "status_format_not_found": "Format not found in the settings file.",
        "status_select_projects": "Select the projects folder.", "status_ready_to_run": "Ready to rename.",
        "status_running": "Running... Scanning folders...",
        "status_scan_error": "Scan error: {error}", "status_no_folders": "Project folders not found.",
        "status_found_folders": "Found {count} folders. Renaming...",
        "status_renaming": "Renamed {done}/{total}...",
        "status_finished": "Finished. Renamed: {renamed}, Skipped: {skipped}, Errors: {errors}",
        "msg_box_error_title": "Error", "msg_box_warning_title": "Warning", "msg_box_info_title": "Information",
        "msg_box_question_title": "Confirmation",
        "msg_missing_input": "Select settings file, projects folder, and ensure the format is loaded.",
        "msg_confirm_rename": "Rename folders in:\n{folder}\n\nUsing format:\n{format}\n\nProceed?",
        "msg_scan_error": "Error scanning projects folder:\n{error}",
        "msg_no_folders_found": "Suitable project folders not found in:\n{folder}",
        "msg_rename_complete": "Operation complete.\n\nRenamed: {renamed}\nSkipped: {skipped}\nErrors: {errors}\n--------------------\nTotal found: {total}",
        "msg_check_console": "\n\nCheck console for error details.",
        "tooltip_indicator_ok": "OK", "tooltip_indicator_error_format": "Error: Format not found",
        "tooltip_indicator_no_settings": "File not selected", "tooltip_indicator_no_projects": "Folder not selected",
        "copyright_text": '<html><body><p align="center">Created by David Kamarauli (<a href="http://smiledesigner.us/">smiledesigner.us</a> | Inst: <a href="https://www.instagram.com/davidkamaraulli/">@davidkamaraulli</a>)</p></body></html>',
    },
    "es": {
        "window_title": "ExoCAD db healer", "menu_language": "Idioma", "lang_ru": "Русский", "lang_en": "English",
        "lang_es": "Español",
        "step1_label": "1. Archivo de Configuración de Formato:",
        "settings_placeholder": "Seleccione el archivo XML de configuración...",
        "settings_tooltip": "Archivo XML con etiquetas <FilenameTemplate> o <PathTemplate>",
        "browse_button": "Explorar...", "settings_browse_tooltip": "Seleccionar archivo de configuración",
        "format_label": "Formato de Nombre Detectado:", "format_placeholder": "...",
        "format_tooltip": "Formato de nombre de carpeta del archivo de configuración",
        "step2_label": "2. Carpeta de Proyectos Exocad:",
        "projects_placeholder": "Seleccione la carpeta de proyectos...",
        "projects_tooltip": "Carpeta que contiene subcarpetas con archivos .dentalProject",
        "projects_browse_tooltip": "Seleccionar carpeta de proyectos Exocad",
        "step3_label": "3. Ejecución:", "action_button": "Realizar Renombrado",
        "action_button_tooltip": "Iniciar el renombrado de carpetas en el directorio seleccionado",
        "status_ready": "Listo.", "status_select_settings": "Seleccione el archivo de configuración de formato.",
        "status_format_not_found": "Formato no encontrado en el archivo de configuración.",
        "status_select_projects": "Seleccione la carpeta de proyectos.", "status_ready_to_run": "Listo para renombrar.",
        "status_running": "Ejecutando... Escaneando carpetas...",
        "status_scan_error": "Error de escaneo: {error}", "status_no_folders": "Carpetas de proyecto no encontradas.",
        "status_found_folders": "Se encontraron {count} carpetas. Renombrando...",
        "status_renaming": "Renombradas {done}/{total}...",
        "status_finished": "Finalizado. Renombradas: {renamed}, omitidas: {skipped}, Errores: {errors}",
        "msg_box_error_title": "Error", "msg_box_warning_title": "Advertencia", "msg_box_info_title": "Información",
        "msg_box_question_title": "Confirmación",
        "msg_missing_input": "Seleccione el archivo de configuración, la carpeta de proyectos y asegúrese de que el formato esté cargado.",
        "msg_confirm_rename": "Renombrar carpetas en:\n{folder}\n\nUsando el formato:\n{format}\n\n¿Continuar?",
        "msg_scan_error": "Error al escanear la carpeta de proyectos:\n{error}",
        "msg_no_folders_found": "No se encontraron carpetas de proyecto adecuadas en:\n{folder}",
        "msg_rename_complete": "Operación completada.\n\nRenombradas: {renamed}\nOmitidas: {skipped}\nErrores: {errors}\n--------------------\nTotal encontradas: {total}",
        "msg_check_console": "\n\nRevise la consola para detalles de errores.",
        "tooltip_indicator_ok": "OK", "tooltip_indicator_error_format": "Error: Formato no encontrado",
        "tooltip_indicator_no_settings": "Archivo no seleccionado",
        "tooltip_indicator_no_projects": "Carpeta no seleccionada",
        "copyright_text": '<html><body><p align="center">Creado por David Kamarauli (<a href="http://smiledesigner.us/">smiledesigner.us</a> | Inst: <a href="https://www.instagram.com/davidkamaraulli/">@davidkamaraulli</a>)</p></body></html>',
    }
}


# Helper functions for filename cleaning and XML data extraction
def clean_filename(filename):
    # Replace problematic characters for file naming
    filename = filename.replace('"', "'").replace('>', ')').replace('<', '(')
    invalid_chars = r'[:|?*/\\]'
    cleaned = re.sub(invalid_chars, '_', filename)
    # Remove control characters and trim dots/spaces
    cleaned = "".join(c for c in cleaned if ord(c) >= 32).strip('. ')
    if cleaned in ('.', '..') or not cleaned:
        return '_'
    return cleaned


def extract_data_from_dentalproject(xml_path):
    # Initialize data dictionary for placeholders
    data = {'p': '', 'l': '', 'f': '', 'd': '', 'n': '', 'c': '', 's': '', 'tc': ''}
    try:
        # Try different encodings to parse xml
        encodings_to_try = ['utf-8', 'iso-8859-1', 'windows-1252']
        tree = None
        for enc in encodings_to_try:
            try:
                with open(xml_path, 'r', encoding=enc) as f:
                    content = f.read()
                # Check for declared encoding in XML
                declared_encoding_match = re.search(r'<\?xml[^>]*encoding="([^"]+)"', content, re.IGNORECASE)
                declared_encoding = declared_encoding_match.group(1).lower() if declared_encoding_match else None
                final_encoding = enc
                if declared_encoding and declared_encoding in encodings_to_try:
                    final_encoding = declared_encoding
                parser = ET.XMLParser(encoding=final_encoding)
                tree = ET.fromstring(content.encode(final_encoding), parser=parser)
                break
            except Exception:
                continue
        if tree is None:
            raise ET.ParseError(f"Failed to parse {os.path.basename(xml_path)}")

        root = tree
        # Extract practice name
        elem_p = root.find('.//Practice/PracticeName')
        data['p'] = elem_p.text.strip() if elem_p is not None and elem_p.text else ''
        # Patient full name
        elem_l = root.find('.//Patient/PatientName')
        data['l'] = elem_l.text.strip() if elem_l is not None and elem_l.text else ''
        # Patient first name
        elem_f = root.find('.//Patient/PatientFirstName')
        data['f'] = elem_f.text.strip() if elem_f is not None and elem_f.text else ''
        # Date handling
        elem_d = root.find('.//DateTime')
        if elem_d is not None and elem_d.text:
            try:
                data['d'] = datetime.strptime(elem_d.text.split('T')[0], '%Y-%m-%d').strftime('%Y-%m-%d')
            except:
                match = re.search(r"(\d{4}-\d{2}-\d{2})", elem_d.text)
                data['d'] = match.group(1) if match else ''
        # Practice ID
        elem_n = root.find('.//Practice/PracticeId')
        data['n'] = elem_n.text.strip() if elem_n is not None and elem_n.text else ''
        # Tooth color
        elem_tc = root.find('.//ToothColor')
        data['tc'] = elem_tc.text.strip() if elem_tc is not None and elem_tc.text else ''
        # Tray number
        elem_s = root.find('.//TrayNo')
        data['s'] = elem_s.text.strip() if elem_s is not None and elem_s.text else ''
        data['c'] = ''  # Placeholder, not used currently
    except Exception as e:
        print(f"Error processing {xml_path}: {e}")
    # Ensure all values are strings and stripped
    for key in data:
        data[key] = str(data[key]).strip() if data[key] is not None else ''
    print(f"Extracted data from {xml_path}: {data}")
    return data


# Function to generate new folder name based on format and data
def generate_new_name(format_string, data):
    # Start with the provided format string
    new_name = format_string
    placeholders = re.findall(r"%\w+", format_string)

    print(f"Generating name using format: '{format_string}'")
    # Replace all placeholders with corresponding data
    for key, value in data.items():
        placeholder = f"%{key}"
        if placeholder in placeholders:
            print(f"Replacing '{placeholder}' with '{value}'")
            new_name = new_name.replace(placeholder, str(value))

    # Remove unfilled placeholders, leaving separators intact
    temp_name = new_name
    for ph in placeholders:
        key = ph[1:]
        if key not in data or not data[key]:
            temp_name = temp_name.replace(ph, '')
            print(f"Removed empty placeholder '{ph}', result: '{temp_name}'")

    new_name = temp_name

    # Custom cleaning to handle placeholders and special characters
    # Reduce 3+ consecutive hyphens/underscores to a single hyphen
    new_name = re.sub(r'[-_]{3,}', '-', new_name)
    # Trim leading/trailing hyphens or underscores
    new_name = new_name.strip('-_')

    print(f"Before final cleanup: '{new_name}'")
    # Final cleanup for filesystem compatibility
    cleaned_name = clean_filename(new_name)
    print(f"After final cleanup: '{cleaned_name}'")
    return cleaned_name


# Main application class
class RenamerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize paths and settings
        self.settings_file_path = None
        self.projects_folder_path = None
        self.rename_format = ""
        self.current_lang = "ru"
        self.setWindowTitle(TRANSLATIONS[self.current_lang]["window_title"])
        self.setGeometry(100, 100, 600, 450)
        # Set window icon if available
        try:
            app_icon_path = 'app_icon.ico'
            if os.path.exists(app_icon_path):
                self.setWindowIcon(QIcon(app_icon_path))
            else:
                self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        except Exception as e:
            print(f"Failed to load icon: {e}")
        self.init_ui()
        self.apply_styles()
        self.retranslateUi()
        self.update_ui_states()

    def init_ui(self):
        # Set up the main widget and layout
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(10)

        self.init_menu()

        # Settings section
        self.settings_label = QLabel()
        self.settings_label.setObjectName("StepLabel")
        settings_input_layout = QHBoxLayout()
        self.settings_path_edit = QLineEdit()
        self.settings_path_edit.setReadOnly(True)
        self.settings_browse_button = QPushButton()
        self.settings_browse_button.setProperty("class", "BrowseButton")
        self.settings_browse_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        self.settings_browse_button.clicked.connect(self.select_settings_file)
        self.settings_status_indicator = QLabel()
        self.settings_status_indicator.setProperty("class", "StatusIndicator")
        settings_input_layout.addWidget(self.settings_path_edit)
        settings_input_layout.addWidget(self.settings_browse_button)
        settings_input_layout.addWidget(self.settings_status_indicator)

        self.format_label = QLabel()
        self.format_label.setStyleSheet("font-size: 9pt; color: #7f8a9f; margin-top: 5px;")
        self.format_display_edit = QLineEdit()
        self.format_display_edit.setReadOnly(True)

        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setProperty("class", "hline")

        # Projects section
        self.projects_label = QLabel()
        self.projects_label.setObjectName("StepLabel")
        projects_input_layout = QHBoxLayout()
        self.projects_path_edit = QLineEdit()
        self.projects_path_edit.setReadOnly(True)
        self.projects_browse_button = QPushButton()
        self.projects_browse_button.setProperty("class", "BrowseButton")
        self.projects_browse_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon))
        self.projects_browse_button.clicked.connect(self.select_projects_folder)
        self.projects_status_indicator = QLabel()
        self.projects_status_indicator.setProperty("class", "StatusIndicator")
        projects_input_layout.addWidget(self.projects_path_edit)
        projects_input_layout.addWidget(self.projects_browse_button)
        projects_input_layout.addWidget(self.projects_status_indicator)

        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setProperty("class", "hline")

        # Action section
        self.action_label = QLabel()
        self.action_label.setObjectName("StepLabel")
        action_layout = QHBoxLayout()
        action_layout.addStretch(1)
        self.action_button = QPushButton()
        self.action_button.setObjectName("ActionButton")
        self.action_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        self.action_button.setIconSize(QSize(18, 18))
        self.action_button.clicked.connect(self.run_blast)
        action_layout.addWidget(self.action_button)
        action_layout.addStretch(1)

        # Copyright footer
        self.copyright_label = QLabel()
        self.copyright_label.setObjectName("CopyrightLabel")
        self.copyright_label.setTextFormat(Qt.TextFormat.RichText)
        self.copyright_label.setOpenExternalLinks(True)
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Assemble the layout
        main_layout.addWidget(self.settings_label)
        main_layout.addLayout(settings_input_layout)
        main_layout.addWidget(self.format_label)
        main_layout.addWidget(self.format_display_edit)
        main_layout.addWidget(line1)
        main_layout.addWidget(self.projects_label)
        main_layout.addLayout(projects_input_layout)
        main_layout.addWidget(line2)
        main_layout.addWidget(self.action_label)
        main_layout.addSpacerItem(QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        main_layout.addLayout(action_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(self.copyright_label)

    def init_menu(self):
        # Set up the language menu
        menu_bar = self.menuBar()
        self.language_menu = menu_bar.addMenu("")
        self.language_action_group = QActionGroup(self)
        self.language_action_group.setExclusive(True)

        self.action_ru = QAction(TRANSLATIONS["ru"]["lang_ru"], self, checkable=True)
        self.action_en = QAction(TRANSLATIONS["en"]["lang_en"], self, checkable=True)
        self.action_es = QAction(TRANSLATIONS["es"]["lang_es"], self, checkable=True)

        self.action_ru.triggered.connect(lambda: self.change_language("ru"))
        self.action_en.triggered.connect(lambda: self.change_language("en"))
        self.action_es.triggered.connect(lambda: self.change_language("es"))

        self.language_action_group.addAction(self.action_ru)
        self.language_action_group.addAction(self.action_en)
        self.language_action_group.addAction(self.action_es)

        self.language_menu.addAction(self.action_ru)
        self.language_menu.addAction(self.action_en)
        self.language_menu.addAction(self.action_es)

        # Set default language
        if self.current_lang == "ru":
            self.action_ru.setChecked(True)
        elif self.current_lang == "en":
            self.action_en.setChecked(True)
        elif self.current_lang == "es":
            self.action_es.setChecked(True)

    def change_language(self, lang_code):
        # Switch UI language
        if lang_code in TRANSLATIONS and self.current_lang != lang_code:
            self.current_lang = lang_code
            print(f"Switched language to: {lang_code}")
            if lang_code == "ru":
                self.action_ru.setChecked(True)
            elif lang_code == "en":
                self.action_en.setChecked(True)
            elif lang_code == "es":
                self.action_es.setChecked(True)
            self.retranslateUi()
            self.update_ui_states()

    def retranslateUi(self):
        # Update all UI text based on current language
        tr = TRANSLATIONS[self.current_lang]
        self.setWindowTitle(tr["window_title"])
        self.language_menu.setTitle(tr["menu_language"])
        self.settings_label.setText(tr["step1_label"])
        self.settings_path_edit.setPlaceholderText(tr["settings_placeholder"])
        self.settings_path_edit.setToolTip(tr["settings_tooltip"])
        self.settings_browse_button.setText(tr["browse_button"])
        self.settings_browse_button.setToolTip(tr["settings_browse_tooltip"])
        self.format_label.setText(tr["format_label"])
        self.format_display_edit.setPlaceholderText(tr["format_placeholder"])
        self.format_display_edit.setToolTip(tr["format_tooltip"])
        self.projects_label.setText(tr["step2_label"])
        self.projects_path_edit.setPlaceholderText(tr["projects_placeholder"])
        self.projects_path_edit.setToolTip(tr["projects_tooltip"])
        self.projects_browse_button.setText(tr["browse_button"])
        self.projects_browse_button.setToolTip(tr["projects_browse_tooltip"])
        self.action_label.setText(tr["step3_label"])
        self.action_button.setText(tr["action_button"])
        self.action_button.setToolTip(tr["action_button_tooltip"])
        self.copyright_label.setText(tr["copyright_text"])
        self.action_ru.setText(tr["lang_ru"])
        self.action_en.setText(tr["lang_en"])
        self.action_es.setText(tr["lang_es"])
        self.update_ui_states()

    def apply_styles(self):
        # Apply the dark theme styles
        self.setStyleSheet(PROFESSIONAL_DARK_STYLE)
        self.success_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton).pixmap(QSize(16, 16))
        self.error_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton).pixmap(QSize(16, 16))
        self.settings_status_indicator.clear()
        self.projects_status_indicator.clear()

    def update_ui_states(self):
        # Update button states and status bar
        tr = TRANSLATIONS[self.current_lang]
        settings_ok = bool(self.settings_file_path and self.rename_format)
        projects_ok = bool(self.projects_folder_path)
        action_enabled = settings_ok and projects_ok
        self.action_button.setEnabled(action_enabled)

        if self.settings_file_path:
            self.settings_status_indicator.setPixmap(self.success_icon if self.rename_format else self.error_icon)
            self.settings_status_indicator.setToolTip(
                tr["tooltip_indicator_ok"] if self.rename_format else tr["tooltip_indicator_error_format"])
        else:
            self.settings_status_indicator.clear()
            self.settings_status_indicator.setToolTip(tr["tooltip_indicator_no_settings"])

        if self.projects_folder_path:
            self.projects_status_indicator.setPixmap(self.success_icon)
            self.projects_status_indicator.setToolTip(tr["tooltip_indicator_ok"])
        else:
            self.projects_status_indicator.clear()
            self.projects_status_indicator.setToolTip(tr["tooltip_indicator_no_projects"])

        status_key = "status_ready"
        if not action_enabled:
            if not self.settings_file_path:
                status_key = "status_select_settings"
            elif not self.rename_format:
                status_key = "status_format_not_found"
            elif not self.projects_folder_path:
                status_key = "status_select_projects"
        else:
            status_key = "status_ready_to_run"
        self.status_bar.showMessage(tr[status_key])

    def select_settings_file(self):
        # Open dialog to select XML settings file
        tr = TRANSLATIONS[self.current_lang]
        file_path, _ = QFileDialog.getOpenFileName(self, tr["settings_browse_tooltip"], "",
                                                   "XML Files (*.xml);;All Files (*)")
        if file_path:
            self.settings_file_path = file_path
            self.settings_path_edit.setText(file_path)
            self.rename_format = ""
            self.format_display_edit.clear()
            self.settings_status_indicator.clear()
            self.read_settings_format()
            self.update_ui_states()

    def read_settings_format(self):
        # Parse the XML settings file for the rename format
        tr = TRANSLATIONS[self.current_lang]
        if not self.settings_file_path:
            return
        try:
            encodings_to_try = ['utf-8', 'iso-8859-1', 'windows-1252']
            root = None
            for enc in encodings_to_try:
                try:
                    with open(self.settings_file_path, 'r', encoding=enc) as f:
                        content = f.read()
                    declared_encoding_match = re.search(r'<\?xml[^>]*encoding="([^"]+)"', content, re.IGNORECASE)
                    declared_encoding = declared_encoding_match.group(1).lower() if declared_encoding_match else None
                    final_encoding = enc
                    if declared_encoding and declared_encoding in encodings_to_try:
                        final_encoding = declared_encoding
                    parser = ET.XMLParser(encoding=final_encoding)
                    root = ET.fromstring(content.encode(final_encoding), parser=parser)
                    break
                except Exception:
                    continue
            if root is None:
                raise ET.ParseError("Could not parse settings XML")

            format_elem = root.find('.//FilenameTemplate') or root.find('.//PathTemplate')
            if format_elem is not None and format_elem.text:
                self.rename_format = format_elem.text.strip()
                self.format_display_edit.setText(self.rename_format)
                print(f"Loaded rename format: {self.rename_format}")
            else:
                self.rename_format = ""
                self.format_display_edit.clear()
                QMessageBox.warning(self, tr["msg_box_warning_title"], tr["status_format_not_found"])
                print("No format found in settings file")
        except (ET.ParseError, IOError) as e:
            self.rename_format = ""
            self.format_display_edit.clear()
            QMessageBox.critical(self, tr["msg_box_error_title"], f"{tr['status_format_not_found']}\n{e}")
            self.settings_file_path = None
            self.settings_path_edit.clear()
            print(f"Error reading settings file: {e}")

    def select_projects_folder(self):
        # Open dialog to select projects folder
        tr = TRANSLATIONS[self.current_lang]
        folder_path = QFileDialog.getExistingDirectory(self, tr["projects_browse_tooltip"], "",
                                                       QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks)
        if folder_path:
            self.projects_folder_path = folder_path
            self.projects_path_edit.setText(folder_path)
            self.update_ui_states()

    def run_blast(self):
        # Execute the renaming process
        tr = TRANSLATIONS[self.current_lang]
        if not self.settings_file_path or not self.projects_folder_path or not self.rename_format:
            QMessageBox.warning(self, tr["msg_box_warning_title"], tr["msg_missing_input"])
            return

        reply = QMessageBox.question(self, tr["msg_box_question_title"],
                                     tr["msg_confirm_rename"].format(folder=self.projects_folder_path,
                                                                     format=self.rename_format),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
                                     QMessageBox.StandardButton.Cancel)
        if reply == QMessageBox.StandardButton.Cancel:
            self.status_bar.showMessage(tr["status_ready_to_run"])
            return

        self.status_bar.showMessage(tr["status_running"])
        QApplication.processEvents()

        project_folders_to_rename = []
        project_file_map = {}
        try:
            print(f"Scanning folder: {self.projects_folder_path}")
            for item in os.listdir(self.projects_folder_path):
                item_path = os.path.join(self.projects_folder_path, item)
                if os.path.isdir(item_path):
                    found_project_file = False
                    actual_project_filename = None
                    try:
                        for sub_item in os.listdir(item_path):
                            sub_item_path = os.path.join(item_path, sub_item)
                            if sub_item.lower().endswith(".dentalproject") and os.path.isfile(sub_item_path):
                                found_project_file = True
                                actual_project_filename = sub_item
                                break
                    except Exception as e:
                        print(f"Warning: Couldn't access {item_path}: {e}")
                        continue
                    if found_project_file:
                        try:
                            if os.path.getsize(os.path.join(item_path, actual_project_filename)) > 0:
                                project_folders_to_rename.append(item_path)
                                project_file_map[item_path] = actual_project_filename
                                print(f"Found project folder: {item_path} with {actual_project_filename}")
                        except Exception as e:
                            print(f"Skipping {item_path} due to validation error: {e}")
        except Exception as e:
            QMessageBox.critical(self, tr["msg_box_error_title"], tr["msg_scan_error"].format(error=e))
            self.status_bar.showMessage(tr["status_scan_error"].format(error=e))
            print(f"Scan failed: {e}")
            return

        if not project_folders_to_rename:
            QMessageBox.information(self, tr["msg_box_info_title"],
                                    tr["msg_no_folders_found"].format(folder=self.projects_folder_path))
            self.status_bar.showMessage(tr["status_no_folders"])
            print("No project folders found")
            return

        folder_count = len(project_folders_to_rename)
        self.status_bar.showMessage(tr["status_found_folders"].format(count=folder_count))
        print(f"Total folders to process: {folder_count}")
        QApplication.processEvents()

        renamed_count, error_count, skipped_count = 0, 0, 0
        rename_details = []
        for i, old_folder_path in enumerate(project_folders_to_rename):
            folder_name = os.path.basename(old_folder_path)
            actual_project_filename = project_file_map.get(old_folder_path)
            if not actual_project_filename:
                print(f"Error: No project file mapped for {old_folder_path}")
                error_count += 1
                rename_details.append((old_folder_path, "(Error)", "Mapping issue"))
                continue

            dentalproject_file_path = os.path.join(old_folder_path, actual_project_filename)
            print(f"\nProcessing folder: {folder_name}")
            data = extract_data_from_dentalproject(dentalproject_file_path)
            new_folder_name = generate_new_name(self.rename_format, data)

            if not new_folder_name or new_folder_name == '_':
                print(f"Skipping {folder_name}: invalid new name '{new_folder_name}'")
                skipped_count += 1
                rename_details.append((old_folder_path, f"({new_folder_name})", "Skipped: Invalid name"))
                continue

            if new_folder_name == folder_name:
                print(f"Skipping {folder_name}: name already correct")
                skipped_count += 1
                rename_details.append((old_folder_path, new_folder_name, "Skipped: Already correct"))
                continue

            new_folder_path = os.path.join(self.projects_folder_path, new_folder_name)
            try:
                if os.path.exists(new_folder_path):
                    if os.path.normcase(os.path.abspath(old_folder_path)) == os.path.normcase(
                            os.path.abspath(new_folder_path)):
                        print(f"Skipping {folder_name}: only case difference")
                        skipped_count += 1
                        rename_details.append((old_folder_path, new_folder_name, "Skipped: Case difference"))
                    else:
                        print(f"Error: {new_folder_name} already exists, skipping {folder_name}")
                        error_count += 1
                        rename_details.append((old_folder_path, new_folder_name, "Error: Target exists"))
                else:
                    print(f"Renaming {old_folder_path} to {new_folder_path}")
                    os.rename(old_folder_path, new_folder_path)
                    renamed_count += 1
                    rename_details.append((old_folder_path, new_folder_name, "Success"))
                    self.status_bar.showMessage(tr["status_renaming"].format(done=i + 1, total=folder_count))
                    QApplication.processEvents()
            except Exception as e:
                print(f"Failed to rename {folder_name}: {e}")
                error_count += 1
                rename_details.append((old_folder_path, new_folder_name, f"Error: {e}"))

        final_message = tr["msg_rename_complete"].format(renamed=renamed_count, skipped=skipped_count,
                                                         errors=error_count, total=folder_count)
        self.status_bar.showMessage(
            tr["status_finished"].format(renamed=renamed_count, skipped=skipped_count, errors=error_count))
        print("\n--- Rename Results ---")
        for old, new, status in rename_details:
            print(f"'{os.path.basename(old)}' -> '{new}': {status}")
        print("--------------------\n")

        msg_box_func = QMessageBox.warning if error_count > 0 else QMessageBox.information
        msg_box_func(self, tr["msg_box_info_title"],
                     final_message + (tr["msg_check_console"] if error_count > 0 else ""))


# Application entry point
if __name__ == '__main__':
    # Enable high DPI scaling for better display
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    window = RenamerApp()
    window.show()
    sys.exit(app.exec())
