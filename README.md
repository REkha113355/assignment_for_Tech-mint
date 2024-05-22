# Automation Script for Teachmint

This repository contains an automation script for logging into the Teachmint platform, navigating through various sections, and performing tasks such as entering OTP, selecting certificate types, and generating certificates.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
  - [get_webdriver_instance](#get_webdriver_instance)
  - [enter_phone_number_otp](#enter_phone_number_otp)
  - [login](#login)
  - [navigate_to_certificates](#navigate_to_certificates)
  - [select_certificate_type](#select_certificate_type)
  - [search_and_select_student](#search_and_select_student)
  - [generate_certificate](#generate_certificate)
  - [validate_certificate_history](#validate_certificate_history)
  - [click_administrator_icon](#click_administrator_icon)
  - [main](#main)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.6+
- Google Chrome browser
- Internet connection

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your_username/teachmint_automation.git
    cd teachmint_automation
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

    **Note:** The `requirements.txt` file should contain the following packages:

    ```
    selenium
    webdriver_manager
    ```

## Usage

1. **Run the script:**

    ```bash
    python assignment.py
    ```

2. **Observe the terminal for output messages indicating the progress and any errors encountered.**

## Functions

### get_webdriver_instance

Initializes a Selenium WebDriver instance with specified options and capabilities for Chrome. Opens the Teachmint login page.

### enter_phone_number_otp

Enters the user's phone number and OTP for authentication. Handles scenarios where the skip button for password creation may not be found.

### login

Logs into the Teachmint platform using the provided credentials. Waits for the dashboard to load before proceeding.

### navigate_to_certificates

Navigates to the Certificates section from the dashboard.

### select_certificate_type

Selects the type of certificate to be generated from a dropdown menu.

### search_and_select_student

Searches for a student by name and selects the student from the search results.

### generate_certificate

Generates a certificate for the selected student and initiates the download.

### validate_certificate_history

Validates the presence of the generated certificate in the certificate history.

### click_administrator_icon

Clicks the administrator icon to navigate to the administrator section.

### main

The main function that orchestrates the login, navigation, and certificate generation process.

## Error Handling

The script includes robust error handling to manage scenarios such as:

- Elements not found
- Timeouts
- General exceptions

Error messages are printed to the console to aid in debugging and understanding the script's execution flow.

## Contributing

1. **Fork the repository.**
2. **Create a new branch:**

    ```bash
    git checkout -b feature/your_feature
    ```

3. **Make your changes and commit them:**

    ```bash
    git commit -m 'Add some feature'
    ```

4. **Push to the branch:**

    ```bash
    git push origin feature/your_feature
    ```

5. **Submit a pull request.**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This README file provides a comprehensive overview of the automation script, including installation instructions, function descriptions, and error handling mechanisms. By following this guide, users should be able to set up and run the script with ease.
