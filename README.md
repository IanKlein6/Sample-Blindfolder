# Sample Blindfolder Application

## Overview

The Sample Blindfolder application is a specialized tool created to assist a doctoral student and their research team in automating the blinding of research samples. This process is vital for ensuring the impartiality of scientific analyses and interpretations. Previously, the team manually blinded each sample, a labor-intensive process that detracted from their primary research activities. The introduction of this application streamlines the process, significantly saving time and enhancing productivity.

## Purpose

Blinding is a critical procedure in experimental research to minimize bias and uphold result integrity. The application conceals the identities of samples, preventing any potential biases from affecting the study's outcomes. By assigning randomized new identifiers to the samples, the application ensures the necessary anonymity for unbiased research.

## Features

- **Folder Selection**: Allows the selection of multiple folders containing the samples for blinding, with a user-friendly interface for folder navigation.
- **Blinding Process**: Randomly renames files in selected folders with anonymized identifiers, incorporating the current date and a unique sequence number.
- **Traceability**: Generates an Excel sheet mapping original file names to their new blinded counterparts, sorted in two tabs for easy reference and future unblinding.
- **User Interface**: Utilizes Tkinter, enabling a simple and intuitive graphical interface that streamlines the entire process for users.

## Technical Details

Developed in Python, the application leverages the language's simplicity and the powerful data manipulation features of libraries like Pandas and the GUI capabilities of Tkinter.

- **Python**: Selected for its ease of use and the robust data manipulation provided by Pandas.
- **Tkinter**: Employs this library for developing the application's graphical user interface.
- **Pandas**: Utilized for creating and managing the Excel log, facilitating accurate tracking of original and blinded sample names.

## Usage

### Step 1: Download and Launch
- Navigate to the 'Applications' section, select the appropriate version for your operating system, download, and execute the Sample Blindfolder application.

### Step 2: Add Folders
- Use the 'Add Folder' button to choose and add folders containing the samples you intend to blind.

### Step 3: Start Blinding
- Press the 'Destination - Blindfold' button, select an output directory, and initiate the blinding process.

### Step 4: Review Excel Sheet
- Upon completion, examine the 'Blindfold_log.xlsx' file in the output directory to view the mapping of original to blinded sample names.

## Conclusion

The Sample Blindfolder application illustrates how targeted software development can significantly benefit scientific research, enhancing efficiency by automating essential but time-consuming tasks, thus maintaining the integrity and objectivity of the research process.
