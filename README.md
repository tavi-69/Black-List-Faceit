# BLK - Faceit Blacklist

BLK (Faceit Blacklist) is a Python application that uses the Faceit API to analyze players in a match. You enter a match link, and the app displays each player, allowing you to add comments about them. This helps you remember how they played in past matches, whether as an opponent or a teammate. Players are identified by their ID, so you can track them even if they change their nickname.

## Installation

1. Download the `BLK.7z` archive.
2. Extract the files.
3. Run `BLK.exe`.

## Running from Source

If you don't trust the `.7z` archive, you can run the application from source by following these steps:

1. Ensure you have Python installed. You can download it from [python.org](https://www.python.org/).
2. Install the required dependencies:
   ```sh
   pip install requests pillow python-dotenv
   ```
3. Run the script:
   ```sh
   python BLK.py
   ```
4. If you want to convert the script into an executable, install `pyinstaller` and create the `.exe` file:
   ```sh
   pip install pyinstaller
   pyinstaller --onefile BLK.py
   ```

## Usage

1. Enter the Faceit match link.
2. The app will display the list of players.
3. Add comments for each player.
4. Comments are saved and can be used for future reference.

## Requirements

- Python (if running from source)
- Internet connection
- Faceit account

## Contact
For any questions or suggestions, open an issue on GitHub.

