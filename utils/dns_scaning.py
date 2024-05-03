import os
import re
import json

def run_whois_scan(target):
    print(f"Running whois scan on {target}...")
    whois_output = os.popen(f"whois {target} -H").read()

    if "NOT FOUND" in whois_output:
        error_message = {"error": "Domain not found"}
        return error_message

    whois_info = {}
    # Extracting Domain Name
    domain_name_match = re.search(r"Domain Name:\s+(.+)", whois_output)
    if domain_name_match:
        whois_info["Domain Name"] = domain_name_match.group(1).strip()

        # Extracting Domain Name
    domain_name_match = re.search(r"domain:\s+(.+)", whois_output, re.IGNORECASE)
    if domain_name_match:
        whois_info["Domain Name"] = domain_name_match.group(1).strip()

    status_match = re.search(r"status:\s+(.+)", whois_output, re.IGNORECASE)
    if status_match:
        whois_info["Status"] = status_match.group(1).strip()

    # Extracting Registrar
    registrar_match = re.search(r"Registrar:\s+(.+)", whois_output)
    if registrar_match:
        whois_info["Registrar"] = registrar_match.group(1).strip()

    registrar_match = re.search(r"registrar:\s+(.+)", whois_output)
    if registrar_match:
        whois_info["Registrar"] = registrar_match.group(1).strip()

    # Extracting Creation Date
    creation_date_match = re.search(r"created:\s+(.+)", whois_output)
    if creation_date_match:
        whois_info["Creation Date"] = creation_date_match.group(1).strip()

    # Extracting Expiry Date
    expiry_date_match = re.search(r"Registry Expiry Date:\s+(.+)", whois_output)
    if expiry_date_match:
        whois_info["Expiry Date"] = expiry_date_match.group(1).strip()

    expiry_date_match = re.search(r"Expiry Date:\s+(.+)", whois_output)
    if expiry_date_match:
        whois_info["Expiry Date"] = expiry_date_match.group(1).strip()

    # Extracting Registrant Information
    registrant_match = re.findall(r"Registrant (.+?):\s+(.+)", whois_output)
    if registrant_match:
        whois_info["Registrant"] = {key.strip(): value.strip() for key, value in registrant_match}
    else:
        registrar_info = {}

        # Extracting Address
        address_match = re.search(r"address:\s+(.+)", whois_output, re.IGNORECASE)
        if address_match:
            registrar_info["Street"] = address_match.group(1).strip()

        # Extracting Country
        country_match = re.search(r"country:\s+(.+)", whois_output, re.IGNORECASE)
        if country_match:
            registrar_info["Country"] = country_match.group(1).strip()

        # Extracting Phone
        phone_match = re.search(r"phone:\s+(.+)", whois_output, re.IGNORECASE)
        if phone_match:
            registrar_info["Phone"] = phone_match.group(1).strip()

        # Extracting Fax
        fax_match = re.search(r"fax-no:\s+(.+)", whois_output, re.IGNORECASE)
        if fax_match:
            registrar_info["Fax"] = fax_match.group(1).strip()

        # Extracting Email
        email_match = re.search(r"e-mail:\s+(.+)", whois_output, re.IGNORECASE)
        if email_match:
            registrar_info["Email"] = email_match.group(1).strip()

        # Extracting Website
        website_match = re.search(r"website:\s+(.+)", whois_output, re.IGNORECASE)
        if website_match:
            registrar_info["Website"] = website_match.group(1).strip()

        if registrar_info:
            whois_info["Registrant"] = registrar_info
    return whois_info
def run_dnsrecon_scan(target):
    print(f"Running dnsrecon scan on {target}...")
    os.popen(f"dnsrecon -d {target} -D /usr/share/wordlists/amass/subdomains-top1mil-5000.txt -t brt --json resultat.json").read()

def debug_whois_scan(results):
    print("Whois scan result:")
    print(json.dumps(results, indent=4))