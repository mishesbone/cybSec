import os
import random

class ThreatDetection:
    def __init__(self):
        self.threat_signatures = ["malware.exe", "keylogger.py", "ransomware.zip"]

    def scan_system(self):
        print("Scanning system files for threats...")
        threats_found = []
        files = ["user_data.txt", "malware.exe", "safe_doc.docx", "ransomware.zip"]

        for file in files:
            if file in self.threat_signatures:
                threats_found.append(file)
        return threats_found
