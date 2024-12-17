import datetime

class Logger:
    def __init__(self, log_file="logs/incidents.log"):
        self.log_file = log_file

    def log(self, message):
        with open(self.log_file, "a") as file:
            log_message = f"{datetime.datetime.now()} - {message}\n"
            file.write(log_message)
