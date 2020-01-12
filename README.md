# SLY URL Shortening Service

## By Peter Polle

## Description
This is a URL shortenning service that is availble via a web interface and a an API.

It allows users to:
* Shorten a URL via web interface.
* Deactivate a shortened URL.
* Activate a deactivated URL.
* Assign a custom URL via the web interface
* Shorten a URL via API.
* Delete a URL via an API.
* Assign a custom URL shortcode via an API
* API token authentication

### Prerequisites

The following are needed for the application to run on a local computer:
* python version 3.6
* Django framework
* Django Rest Framework v3.9.4
* Bootstrap v.3
* Text editor (atom, VS code or sublime text)
* Web browser
A crucial point to note: You will need Python version 3 and above installed on your laptop.
If you don't have it installed got to [Python.org](https://www.python.org/downloads/) to install.

## Getting Started
* Clone this repository to your local computer and install all the extensions listed in the ``requirements.txt`` file.
* Ensure you have python3.6 installed in your computer.
* From the terminal navigate to the cloned project folder.
* Switch to the virtual environment by entering  ```source virtual/bin/activate``` from the terminal. 
* Once inside the application, a user will be able to use the application.

## Running the tests

To run the tests, run ``python manage.py test``

## Deployment

To run local server run ``python manage.py runserver``



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details