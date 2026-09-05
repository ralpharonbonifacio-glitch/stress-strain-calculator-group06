**Stress and Strain Analysis System**

**Group Members**
Member	                  Primary Responsibility
BONIFACIO, Ralph Aron	    Task 1 – Basic Calculations
DELA CRUZ, Andrei Karl    Task 2 – Control Structures
FRANCO, Eivrard Seraphim	Task 3 – Data Structures
MEDALLON, Matthew Zachary	Task 4 – Functions
NEPOMUCENO, Josef Jaden	  Task 5 – OOP

_Task 6 – Modular Integration was completed collaboratively by all members._

**Project Description**
The Stress and Strain Analysis System is a comprehensive, object-oriented Python application designed to calculate and 
evaluate the mechanical properties of various materials under load. Developed incrementally, the project evolved from 
a basic mathematical calculator into a robust, modular system capable of handling complex data structures, validating 
safety parameters, managing session histories, and saving/exporting test data. It serves as a tool for analyzing how 
materials like metals, plastics, and composites behave under applied forces.

**Program Features**
- Core Calculations: Computes stress (σ), strain (ε), Young's Modulus, and Factor of Safety based on user inputs (force, cross-sectional area, original length, and change in length).
- Robust Error Handling & Validation: Includes strict input validation to prevent crashes from invalid data (e.g., division by zero) and ensures graceful program termination.
- Material Management: Utilizes an object-oriented class hierarchy (Material, Metal, Plastic, Composite) to manage predefined and custom material properties.
- Session Tracking & Statistics: Uses lists, dictionaries, sets, and tuples to store detailed calculation history, track unique materials tested, and generate session summaries.
- Data Persistence & Export: Supports saving and loading test session results using JSON, and exporting test data to CSV files for external review. Includes test timestamping for accurate record-keeping.
- Modular Architecture: Responsibilities are cleanly separated into distinct modules for better maintainability and code organization.

**Installation/Requirements**
This program relies entirely on the Python Standard Library. No external packages (like pip installs) are required.
Python Version: Python 3.7 or higher is required (for dataclasses and standard path management).
Standard Modules Used: json, csv, datetime, pathlib, os, and random.

**How to Run the Program**
To start the application, navigate to the root directory of the project in your terminal or command prompt and execute the main script:

Bash
python main.py

**Repository Structure**
The application follows a modular file structure to separate different system responsibilities:
main.py: The main entry point of the program. It provides the user interface/menu, handles user interactions, and coordinates the flow of data between all other modules.
material.py: Contains the core Object-Oriented Material class hierarchy, including specialized subclasses for Metal, Plastic, and Composite.
properties.py: Manages the data-oriented material properties and utilizes Python dataclasses to efficiently structure property data.
tests.py: Contains the classes that model individual stress-strain tests (e.g., StressStrainTest), as well as collections to manage multiple tests within a session.
utils.py: A library of reusable helper functions, including the core math functions (stress, strain, Young's modulus, factor of safety) and input validation routines.
database.py: Manages the system's predefined materials, handling the storage, retrieval, loading (JSON), and exporting (CSV) of test data and material profiles.
