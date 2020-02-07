# Script to setup everything needed to host the server.
import os
import json

try:
    from werkzeug.security import generate_password_hash
except ImportError:
    raise RuntimeError("Please run 'python -m pip install -r requirements.txt' first. Some packages are missing.")

print("Starting setup to host todo server.")

BASE_PATH = os.path.dirname(__file__)

path = os.path.join(BASE_PATH, "src", "app", "user_manager", "login-default.json")
password = input("Please input a password for your user: ")

if not os.path.isfile(path):
    raise RuntimeError(f"{path} not found.")

with open(path, mode="r") as fh:
    data = json.load(fh)

data["user"] = "default"
data["pass"] = generate_password_hash(password)

with open(path, mode="w") as fh:
    json.dump(data, fh)

print(f"Login:\n User: default\n Password: your_password")

input("Please setup a database with the sql setup file provided in /python/\nPress enter to continue.")

print("Please provide a connection string. An example could look like this:\n"
      "mysql://user:pass@localhost:3306/todo\n")

connection_string = input()

path = os.path.join(BASE_PATH, "src", "app", "db_connector", "connection.json")

if not os.path.isfile(path):
    raise RuntimeError(f"{path} not found.")

with open(path, mode="r") as fh:
    data = json.load(fh)

data["connection_string"] = connection_string

with open(path, mode="w") as fh:
    json.dump(data, fh)

print("Setup complete. Run the application by using 'gunicorn --bind 0.0.0.0:port server:app'")


