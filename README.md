# tigerhack-checkin
script to simplify registering tigerhacks participants

https://erikrood.com/Posts/py_gsheets.html follow this guide to get creds.json file and permissions added to the service account for the sheets

## Security Warning


**Never commit your Google service account JSON, .env, or other secrets to GitHub!**

- Always add credential files (e.g., `*.json`) and `.env` to `.gitignore`.
- If secrets were pushed, revoke and rotate them immediately.
- Each user should download their own credentials and place them locally.

## Using Environment Variables

Sensitive information (service account file name, Google Sheet URLs) is now stored in a `.env` file. Example:

```
SERVICE_ACCOUNT_FILE=tigerhacks-2025-a9939a7a77ae.json
REG_SHEET_URL=https://docs.google.com/spreadsheets/d/1lMcM0t5C3rs0drZ9IJ9A4cNIhgo1ATXnwFJYj8IxBNQ/
CHECKIN_SHEET_URL=https://docs.google.com/spreadsheets/d/1L6DsVAME2TIyFEGtQjTmRWZmMPhRx4xP_Brz-ylxaUc/
```

Do not commit your `.env` file. Each user should create their own locally.

## Setup & Troubleshooting

### Step-by-step directions

1. Clone the repository.
2. Ensure you have Python 3.8+ installed.
3. Install dependencies:
    ```
    pip install -r requirements.txt
    pip install python-dotenv
    ```
    **Note:** If you get `ModuleNotFoundError: No module named 'pygsheets'`, install pygsheets directly:
    ```
    pip install pygsheets
    ```
4. Download your Google service account JSON file from the Google Cloud Console and place it in the project directory. Make sure it has access to the Google Sheets you want to use. Update the filename in your `.env` file if needed.
    - Share your Google Sheets with the service account email found in the JSON file.
    - The JSON file should match the filename used in your `.env` file (default: `tigerhacks-2025-a9939a7a77ae.json`).
5. Create a `.env` file in the project directory and add your credentials and sheet URLs (see example above).
6. Run the application:
    ```
    python main.py
    ```
7. Enter a phone number (with or without spaces/dashes) and press "Search" or hit "Enter".

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