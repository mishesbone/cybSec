from modules.threat_detection import ThreatDetection
from modules.vulnerability_scanner import VulnerabilityScanner
from modules.incident_response import IncidentResponse

def main():
    print("Starting Cybersecurity and Risk Management Solution...")

    # Initialize modules
    threat_detector = ThreatDetection()
    vulnerability_scanner = VulnerabilityScanner()
    incident_response = IncidentResponse()

    # Perform threat detection
    print("\n[1] Performing Threat Detection...")
    threats = threat_detector.scan_system()
    print(f"Threats Found: {threats}")

    # Perform vulnerability scan
    print("\n[2] Running Vulnerability Scanner...")
    vulnerabilities = vulnerability_scanner.scan()
    print(f"Vulnerabilities Identified: {vulnerabilities}")

    # Log an incident
    print("\n[3] Logging Incident...")
    if threats or vulnerabilities:
        incident_response.log_incident("Potential threats and vulnerabilities found.")
    else:
        print("No incidents to log.")

if __name__ == "__main__":
    main()
