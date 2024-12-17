from utils.logger import Logger

class IncidentResponse:
    def __init__(self):
        self.logger = Logger()

    def log_incident(self, message):
        print("Logging incident...")
        self.logger.log(message)
        print("Incident logged successfully.")
