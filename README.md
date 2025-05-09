# Student Grades Application

This project is a Python application designed to process student grades. It provides a user-friendly interface for selecting a grades file and generating output files that include treatment and analysis of the grades data.

## Project Structure

```
student-grades-app
├── src
│   ├── main.py               # Entry point of the application
│   ├── ui.py                 # User interface code
│   ├── grades_processor.py    # Logic for processing grades data
│   └── utils
│       └── file_utils.py     # Utility functions for file operations
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd student-grades-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/main.py
   ```

2. Use the graphical interface to select your grades file (in CSV format).

3. Click the button to generate the output files:
   - `traitement.csv`: Contains the processed grades, averages, and ranks.
   - `analyse.csv`: Contains statistical analysis of the grades by subject and for the class.

## Dependencies

This project requires the following Python libraries:
- Tkinter or PyQt (for the user interface)
- CSV (for handling CSV file operations)
- Statistics (for calculating averages and other statistics)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.