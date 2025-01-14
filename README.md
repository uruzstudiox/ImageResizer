# Image Resizer User Guide

This guide explains the usage, functions, and error management of the Image Resizer program. The program is a CLI tool designed to simplify operations such as resizing BMP images and adding grids.

## Table of Contents
1. [Program Objectives](#program-objectives)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
   - [4.1 Project Folders](#project-folders)
   - [4.2 Main Menu](#main-menu)
   - [4.3 Main Menu Options](#main-menu-options)
   - [4.4 Experimental](#experimental)
5. [Error Messages and Causes](#error-messages-and-causes)
6. [Developer Notes](#developer-notes)
7. [Version History Table](#version-history-table)

**Note:** For more detailed usage guides and project structure documentation, please refer to the `docs` folder.

### Program Objectives
- Resizing images.
- Adding grids to images.
- Performing operations using a user-friendly command-line interface (CLI).

### Requirements
- **Python Version:** 3.13 or higher.
- **Libraries:** The project only uses Python's standard libraries. No additional dependencies are required.

### Installation
This program does not require additional installation. To use the program:
- **For Windows users:** You can directly run the `resizer.exe` file located in the main folder.
- **For other operating systems or those who wish to use the raw Python code:** Run the `resizer.py` file located in the `raw` folder using a Python editor or IDE. You can also package the `resizer.py` file according to your operating system.

### Usage
This program allows you to perform image editing operations using a user-friendly command-line interface. Below are the basic steps and explanations for using the program:

#### Project Folders
- **data:** Folder containing the record file (`imagepath.txt`) that holds the path to the image to be processed.
- **images:** Folder containing the raw image to be processed. The `resizer.exe` or `resizer.py` targets the files in this folder for processing.
- **edited_images:** Folder where the processed images are automatically saved.
- **raw:** Folder containing the raw Python file (`resizer.py`) and the icon file (`resizer.ico`). Use the files in this folder if you want to view or modify the source code.

#### Main Menu
When you start the program, you will encounter the following menu:

#### Main Menu Options
1. **(0) Reset File Path:**
   Resets the saved file path. This operation clears the current file path.
   - **e:** Confirms the reset operation.
   - **h:** Cancels the operation and returns to the main menu.

2. **(1) Select File:**
   Allows you to select a file to process. Make sure to enter the file name during the selection process.
   - **e:** Confirms the reset operation.
   - **h:** Cancels the operation and returns to the main menu.

3. **(2) Image Gridding:**
   Adds grid lines to the selected file. You can specify the color and cell size for the grid lines.
   - **e:** Confirms the reset operation.
   - **h:** Cancels the operation and returns to the main menu.

4. **(3) Image Resizing:**
   Resizes the selected file. You need to specify parameters such as width, height, and starting point.
   - **e:** Confirms the reset operation.
   - **h:** Cancels the operation and returns to the main menu.

5. **(exit):**
   Exits the program.

#### Experimental
- The processed image must be in .bmp format. However, edited images can also be saved in other formats such as .png, .jpg, or .ico. (Tested on: Windows 11)

### Error Messages and Causes
Error messages and causes are prepared as a separate document to handle issues that may arise during interaction with the program in a modular and user-friendly manner. This information can be accessed in the `docs` folder under the file named `error_messages_and_causes`.

### Developer Notes
- This program is an open-source example project created to understand the structure of images and how they are read and processed. It aims to serve as a foundation for more comprehensive projects.
- The grid addition and resizing operations are intentionally designed in a less optimized way to facilitate understanding of the basic structure.
- The program is written as a single script file to simplify the packaging process. If desired, you can distribute the components into multiple script files for a more modular approach.
- You can share documentation gaps, bugs identified in the project, or development suggestions in the project comments.

***Translation***
\
*You can find the sources used for the translation below.*
* [Google Translate](https://translate.google.com/?hl=tr&sl=tr&tl=la&op=translate)
* [ChatGPT](https://chatgpt.com/)

### Version History Table
| Version   | Date          | Contributor   | Description       |
|-----------|---------------|---------------|-------------------|
| V0.0.0    | 14.01.2025    | Uruz          | Raw version of the document. |
| V0.0.1    | 14.01.2025    | Uruz          | First version of the document. |
