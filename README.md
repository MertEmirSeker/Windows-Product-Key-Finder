
# ![Seker Logo](https://github.com/MertEmirSeker/Pictures-and-Videos/blob/main/seker_logo.png) Windows Product Key Finder

A simple Python script to find and display your Windows Product Key with an option to save it as a text file.

## How to Run the Script

### 1. Install Python
Ensure that you have Python installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

### 2. Install Required Libraries
Install the necessary Python libraries using pip:

```bash
pip install Pillow
```

### 3. Run the Script
Navigate to the directory containing the script and run it using Python:

```bash
python key.py
```

### 4. Using the Script
The script will open a graphical interface where you can view your Windows Product Key. You will also have the option to save the key as a text file.

## Converting the Script to an Executable

You can convert this Python script into a standalone executable using PyInstaller. To do so, use the following command:

```bash
pyinstaller --onefile --windowed --icon=../icon/logo.ico --add-data "../icon/logo.ico;icon" --add-data "../icon/background.png;icon" --distpath "app" --workpath "app/build" --specpath "app" source/key.py
```

This command will create a single executable file with the specified icon and additional data files. The executable will be placed in the `app` directory.
