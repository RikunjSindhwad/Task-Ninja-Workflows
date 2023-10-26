#!/usr/local/bin/python
import sys
import argparse
import time
import requests
import json

URL = "https://reverse-whois.whoisxmlapi.com/api/v2"


def read_file_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        sys.stderr.write(f"Error: The file '{file_path}' was not found.\n")
        return []
    except PermissionError:
        sys.stderr.write(f"Error: You do not have permission to read '{file_path}'.\n")
        return []
    except Exception as e:
        sys.stderr.write(f"An error occurred while reading the file '{file_path}': {str(e)}\n")
        return []


def save_list_to_file(file_path, data):
    try:
        with open(file_path, 'w') as file:
            for item in data:
                file.write(str(item) + '\n')
        sys.stderr.write(f"List saved to '{file_path}' successfully.\n")
    except Exception as e:
        sys.stderr.write(f"An error occurred while saving the list to '{file_path}': {str(e)}\n")


def get_fields(input_type):
    return {
        "email": [
            "RegistrantContact.Email",
            "AdminContact.Email",
            "BillingContact.Email",
            "TechContact.Email"
        ],
        "org": [
            "RegistrantContact.Organization",
            "AdminContact.Organization",
            "BillingContact.Organization",
            "TechContact.Organization"
        ],
        "phone": [
            "RegistrantContact.Telephone",
            "AdminContact.Telephone",
            "BillingContact.Telephone",
            "TechContact.Telephone"
        ],
        "domain": ["DomainName"]
    }.get(input_type, [])


def reverse_whois(input_value, api_key, input_type, historic, retry_wait=5, max_retries=5):
    final_result = set()
    fields = get_fields(input_type)
    search_type = "historic" if historic else "current"
    sys.stderr.write(f"[Start] Identifying {search_type} Domains Through '{input_type}': '{input_value}'\n")
    exact_match = "*" not in input_value
    headers = {"Content-Type": "application/json", "X-Authentication-Token": api_key}
    
    for field in fields:
        advanced_terms = [{'field': field, 'term': input_value}]
        retries = 0
        
        while retries < max_retries:
            try:
                search_body = {
                    "apiKey": api_key,
                    "searchType": search_type,
                    "mode": "purchase",
                    'exactMatch': exact_match,
                    "advancedSearchTerms": advanced_terms
                }
                resp = requests.post(URL, headers=headers, json=search_body)
                
                if resp.status_code == 200:
                    final_result.update(json.loads(resp.text)["domainsList"])
                    break
                elif resp.status_code == 429:
                    sys.stderr.write(f"[Info] Rate limited. Retrying in {retry_wait} seconds...\n")
                    time.sleep(retry_wait)
                    retries += 1
                else:
                    sys.stderr.write(f"[Error] Unexpected status code {resp.status_code}. Continuing to the next input...\n")
                    break
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")
                break
        else:
            sys.stderr.write(f"Max retries reached for input '{input_value}'. Continuing to the next input...\n")

    sys.stderr.write(f"[Done] Identified Total '{len(final_result)}' Domains Through '{input_type}':'{input_value}'\n")
    return final_result


def process_items(item_list, item_type, api_key, historic, retry_wait, max_retries):
    final_result = set()
    for item in item_list:
        result = reverse_whois(item.strip(), api_key, item_type, historic, retry_wait, max_retries)
        final_result.update(result)
    return final_result


def main():
    parser = argparse.ArgumentParser(description="Reverse WHOIS lookup script by robensive (Rikunj Sindhwad)")
    parser.add_argument("--api_key", help="Your Reverse WHOIS API key (whoisxmlapi.com)", required=True)
    parser.add_argument("--output", help="Output file path", required=True)
    # Input files
    parser.add_argument("--org_list", help="File containing a list of organizations (use * for wildcard)")
    parser.add_argument("--phone_list", help="File containing a list of phone numbers (use * for wildcard)")
    parser.add_argument("--domain_list", help="File containing a list of domain names (use * for wildcard)")
    parser.add_argument("--email_list", help="File containing a list of email addresses (use * for wildcard)")
    # Individual inputs
    parser.add_argument("--email", help="Single email address (use * for wildcard)")
    parser.add_argument("--org", help="Single organization (use * for wildcard)")
    parser.add_argument("--phone", help="Single phone number (use * for wildcard)")
    parser.add_argument("--domain", help="Single domain name (use * for wildcard)")
    # Additional arguments
    parser.add_argument("--sleep", help="Sleep time between each request (default 2 seconds)", type=int, default=2)
    parser.add_argument("--maxretry", help="Max retry on failure (default=5)", type=int, default=5)
    parser.add_argument("--historic", help="Get Historical domains too (default false)", action='store_true', default=False)
    
    args = parser.parse_args()

    input_files = {
        'org': args.org_list,
        'phone': args.phone_list,
        'domain': args.domain_list,
        'email': args.email_list
    }

    input_args = {
        'org': args.org,
        'phone': args.phone,
        'domain': args.domain,
        'email': args.email
    }

    final_result = set()

    for item_type, file_path in input_files.items():
        if file_path:
            items = read_file_lines(file_path)
            result = process_items(items, item_type, args.api_key, args.historic, args.sleep, args.maxretry)
            final_result.update(result)

    for item_type, item_value in input_args.items():
        if item_value:
            result = process_items([item_value], item_type, args.api_key, args.historic, args.sleep, args.maxretry)
            final_result.update(result)

    save_list_to_file(args.output, final_result)


if __name__ == "__main__":
    main()
