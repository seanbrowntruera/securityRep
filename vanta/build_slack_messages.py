import json
import logging

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

device_owners = []


def grab_records(file_name, issue):
    with open(file_name, "r") as file:
        records = BeautifulSoup(file.read(), "html.parser")
        devices = records.find_all("a", {"class": "sc-jJEJSO bLdkYb"})
        for dev in devices:
            text = dev.text
            text = text.split()
            text = text[0] + " " + text[1] + " " + text[2]
            build_owner(text, issue)
    return device_owners


def build_owner(device, issue):
    try:
        dev_owner = {}
        f_name = device.split("_")[0]
        dev_owner["name"] = f_name
        dev_owner["device"] = device
        # Check if user has other tasks to complete
        found_user, index = check_device_owner(f_name)
        if found_user:
            device_owners[index]["issue"].append(issue)
            return f"Info added to {device_owners[index]}"
        else:
            dev_owner["issue"] = []
            dev_owner["issue"].append(issue)
        device_owners.append(dev_owner)
        logging.info(f"[+] {f_name} info collected.")
        return f"{f_name} added."
    except Exception as e:
        logging.error(f"[+] Unable to collect info error: {e}")


def check_device_owner(name):
    # Check if user has other tasks to complete
    for index in range(len(device_owners)):
        if name in device_owners[index].get("name"):
            return True, index
    return False, None


def password_manager_records():
    pms = grab_records("password_manager_records.html", "password mannager")
    return pms


def anti_virus_records():
    av = grab_records("anti_virus_records.html", "antivirus software")
    return av


def disk_encryption():
    de = grab_records("disk_encryption.html", "disk encryption")
    return de


def build_slack_message():
    password_manager_records()
    anti_virus_records()
    disk_encryption()

    # Build message to send to Slack
    for dev in device_owners:
        name = dev.get("name")
        device = dev.get("device")
        if len(dev.get("issue")) > 1:
            issues = ", or ".join(dev.get("issue"))
        else:
            issue = dev.get("issue")
        string = f"Hi {name}, it looks like you don't have a {issues} on your device: {device}! Please see this link to add it https://truera.atlassian.net/wiki/spaces/~6372aff19341d1f136038a3a/pages/77594672/Security+Setup"
        logging.info(string + "\n")
    print(len(device))


print(build_slack_message())