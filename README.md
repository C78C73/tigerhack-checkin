# tigerhack-checkin
script to simplify registering tigerhacks participants

https://erikrood.com/Posts/py_gsheets.html follow this guide to get creds.json file and permissions added to the service account for the sheets

## Security Warning

**Never commit your Google service account JSON or other secrets to GitHub!**

- Always add credential files (e.g., `*.json`) to `.gitignore`.
- If secrets were pushed, revoke and rotate them immediately.
- Each user should download their own credentials and place them locally.

## Setup & Troubleshooting

### Step-by-step directions

1. Clone the repository.
2. Ensure you have Python 3.8+ installed.
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
    **Note:** If you get `ModuleNotFoundError: No module named 'pygsheets'`, install pygsheets directly:
    ```
    pip install pygsheets
    ```
4. Download your Google service account JSON file from the Google Cloud Console and place it in the project directory. Make sure it has access to the Google Sheets you want to use. Update the filename in `main.py` if needed.
    - Share your Google Sheets with the service account email found in the JSON file.
    - The JSON file should match the filename used in the code (default: `tigerhacks-2025-a9939a7a77ae.json`).
4. Run the application:
    ```
    python main.py
    ```
5. Enter a phone number (with or without spaces/dashes) and press "Search" or hit "Enter".

### Features & Optimizations

- Pressing "Enter" now triggers the search button for faster workflow.
- The app caches sheet data to reduce repeated Google Sheets API calls and speed up lookups.
- Only necessary columns are fetched for duplicate checks, improving performance.
- The UI remains responsive during sheet operations by using background threads.
- Duplicate check-ins are prevented by searching the check-in sheet before adding a new entry.

### Common Issues

- **pygsheets not found:** Make sure you are using the correct Python interpreter in VS Code. You may need to install pygsheets manually.
- **Google Sheets API:** Ensure your `service_account_file` is present and valid.
- **GUI not displaying:** Try running from the terminal, not the VS Code output pane.

### Suggestions for improvement

- Add error handling for Google Sheets API failures.
- Add logging for check-in events.
- Add a requirements.txt entry for pygsheets.
- Consider packaging as an executable for easier distribution.