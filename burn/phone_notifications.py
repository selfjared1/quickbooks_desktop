import requests
import configparser


def get_access_token_from_ini(file_path):
    # Create a ConfigParser object to read the .ini file
    config = configparser.ConfigParser()

    # Read the config file
    config.read(file_path)

    # Get the access token from the 'pushbullet' section
    access_token = config['pushbullet']['access_token']

    return access_token


def send_pushbullet_notification(title, body, access_token):
    # Pushbullet API endpoint
    url = "https://api.pushbullet.com/v2/pushes"

    # HTTP headers
    headers = {
        "Access-Token": access_token,
        "Content-Type": "application/json"
    }

    # Notification data
    data = {
        "type": "note",  # Type of push, "note" is for a simple notification
        "title": title,
        "body": body
    }

    # Make the POST request to Pushbullet API
    response = requests.post(url, json=data, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")

def notify_jared_process_is_done():

    # Get the access token from the ini file
    ini_file_path = 'config.ini'  # Path to your ini file
    access_token = get_access_token_from_ini(ini_file_path)

    # The notification title and body
    notification_title = "Process Finished"
    notification_body = "Your process has finished!"

    # Send the notification via Pushbullet
    send_pushbullet_notification(notification_title, notification_body, access_token)