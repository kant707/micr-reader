# MICR Reader

## Requirements:
- Python v3.11.4
- Node.js v18.19.0
- NPM v10.2.3
- pytesseract v0.3.10
- tesseract v5.3.1

## How to run:
1. Create a virtual environment 
    ```
    python -m venv myenv
    ```

2. Activate the virtual environment
    - Windows
        ```
        myenv\Scripts\activate
        ```
    - macOS and Linux
        ```
        source myenv/bin/activate
        ```

3. Install Dependencies
    ```
    pip install package-name
    ```
    i.e., pip install pytesseract

4. Generate the requirements.txt file
    ```
    pip freeze > requirements.txt
    ```
