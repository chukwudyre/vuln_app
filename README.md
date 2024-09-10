# Vulnerability Management App

This Streamlit application allows you to view and manage vulnerabilities across different categories.

## Setup Instructions

Follow these steps to set up and run the Vulnerability Management App:

1. Clone the repository or download the project folder.

2. Ensure you have Python installed (preferably Python 3.7 or later).

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

7. The app should now be running. Open a web browser and go to the URL displayed in the terminal (usually http://localhost:8501).

## Project Structure

- `app.py`: The main Streamlit application file
- `style.css`: Custom CSS styles for the app
- `requirements.txt`: List of Python dependencies
- `app_activity.log`: Log file for app activities

## Troubleshooting

If you encounter any issues, please ensure you're using the latest version of Streamlit and that all dependencies are correctly installed.

For the error "AttributeError: module 'streamlit' has no attribute 'experimental_rerun'", replace `st.experimental_rerun()` with `st.rerun()` in the `app.py` file.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

[Specify your license here, e.g., MIT License]