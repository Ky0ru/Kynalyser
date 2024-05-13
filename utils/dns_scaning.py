import os
import re
import json
from utils.DNSDumpsterAPI import DNSDumpsterAPI


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


def debug_whois_scan(results):
    print("Whois scan result:")
    print(json.dumps(results, indent=4))


def run_dns_dumpster_scan(target):
    res = DNSDumpsterAPI().search(target)

    if not res['dns_records']['dns']:
        error_message = {"error": "Domain not found"}
        return error_message

    dns_servers = [
        {"domain": entry['domain'], "ip": entry['ip'], "as": entry['as'], "provider": entry['provider'],
         "country": entry['country']}
        for entry in res.get('dns_records', {}).get('dns', [])
    ]
    mx_records = [
        {"domain": entry['domain'], "ip": entry['ip'], "as": entry['as'], "provider": entry['provider'],
         "country": entry['country']}
        for entry in res.get('dns_records', {}).get('mx', [])
    ]
    host_records = [
        {"domain": entry['domain'], "ip": entry['ip'], "as": entry['as'], "provider": entry['provider'],
         "country": entry['country'], "reverse_dns": entry['reverse_dns']}
        if entry.get('reverse_dns') else {"domain": entry['domain'], "ip": entry['ip'], "as": entry['as'],
                                          "provider": entry['provider'], "country": entry['country']}
        for entry in res.get('dns_records', {}).get('host', [])
    ]
    txt_records = res.get('dns_records', {}).get('txt', [])

    image_data = res.get('image_data').decode('utf-8')
    image_retrieved = image_data is not None

    return {
        "domain": res.get('domain'),
        "dns_servers": dns_servers,
        "mx_records": mx_records,
        "host_records": host_records,
        "txt_records": txt_records,
        "image_retrieved": image_retrieved,
        "image_data": image_data,
    }


def debug_dns_dumpster(results):
    print("DNS dumpster scan result:")
    results_copy = results.copy()
    if 'image_data' in results_copy:
        if results_copy['image_data']:
            results_copy['image_data'] = "Image data retrieved"
    print(json.dumps(results_copy, indent=4))
