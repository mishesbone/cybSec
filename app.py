from flask import Flask, render_template

app = Flask(__name__)

# Mock incident data
incident_logs = [
    {"timestamp": "2024-07-21 12:30:00", "threat_name": "malware.exe", "severity": "High", "description": "Detected in system32 folder."},
    {"timestamp": "2024-07-21 13:00:00", "threat_name": "ransomware.zip", "severity": "Critical", "description": "Detected during vulnerability scan."},
]

# Root route
@app.route("/")
def home():
    return "Welcome to eoy Cybersecurity Solution! Visit /incidents to view incident logs."

# Incidents page
@app.route("/incidents")
def incidents():
    return render_template("incidents.html", incidents=incident_logs)

# Favicon handler
@app.route("/favicon.ico")
def favicon():
    return "", 204

# Index route
@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
