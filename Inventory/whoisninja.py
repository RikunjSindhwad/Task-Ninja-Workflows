#!/usr/local/bin/python
import sys
import argparse
import time
import requests
import json
url = "https://reverse-whois.whoisxmlapi.com/api/v2"

def read_file_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        sys.stderr.write(f"Error: The file '{file_path}' was not found.")
        return []
    except PermissionError:
        sys.stderr.write(f"Error: You do not have permission to read '{file_path}'.")
        return []
    except Exception as e:
        sys.stderr.write(f"An error occurred while reading the file '{file_path}': {str(e)}")
        return []    

def save_list_to_file(file_path, data):
    try:
        with open(file_path, 'w') as file:
            for item in data:
                file.write(str(item) + '\n')
        sys.stderr.write(f"List saved to '{file_path}' successfully.")
    except Exception as e:
        sys.stderr.write(f"An error occurred while saving the list to '{file_path}': {str(e)}\n")


def getFeilds(input):
    match input:
        case "email":
            return ["RegistrantContact.Email","AdminContact.Email","BillingContact.Email","TechContact.Email"]
        case "org":
            return ["RegistrantContact.Organization","AdminContact.Organization","BillingContact.Organization","TechContact.Organization"]
        case "phone":
            return ["RegistrantContact.Telephone","AdminContact.Telephone","BillingContact.Telephone","TechContact.Telephone"]
        case "domain":
            return ["DomainName"]
            
def reverseWhois(input, api_key, type, historic, retry_wait=5, max_retries=5):
    finalResult = []
    fields = getFeilds(type)  # Consider renaming this to getFields
    default = "current"
    if historic:
        default = "historic"
    print(f"[Start] Identifying {default} Domains Through '{type}': '{input}'", file=sys.stderr)
    exactMatch = True  # Fixed the typo from exectMatch to exactMatch
    if "*" in input:
        exactMatch = False
    for field in fields:
        advanced_terms = [{'field': field, 'term': input}]
        retries = 0  # Initialize retry counter
        while retries < max_retries:
            try:
                search_body = {
                    "apiKey": api_key,
                    "searchType": default,
                    "mode": "purchase",
                    'exactMatch': exactMatch,
                    "advancedSearchTerms": advanced_terms
                }
                resp = requests.post(url, headers=headers, json=search_body)
                if resp.status_code == 200:
                    domainList = json.loads(resp.text)["domainsList"]
                    break  # Break out of the retry loop if request is successful
                elif resp.status_code == 429:
                    print(f"[Info] Rate limited. Retrying in {retry_wait} seconds...", file=sys.stderr)
                    time.sleep(retry_wait)  # Wait for X seconds before retrying
                    retries += 1  # Increment retry counter
                else:
                    print(f"[Error] Unexpected status code {resp.status_code}. Exiting.", file=sys.stderr)
                    sys.exit(1)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Max retries reached. Exiting.", file=sys.stderr)
            sys.exit(1)
            
        for domain in domainList:
            finalResult.append(domain)
    finalResult = list(set(finalResult))
    print(f"[Done] Identified Total '{len(finalResult)}' Domains Through '{type}':'{input}'", file=sys.stderr)
    return finalResult

def process_items(item_list, item_type, api_key, historic, retry_wait, max_retries):
    for item in item_list:
        item = item.strip()
        result = reverseWhois(item, api_key, item_type, historic, retry_wait, max_retries)
        return result


parser = argparse.ArgumentParser(description="Reverse WHOIS lookup script by robensive (Rikunj Sindhwad)")
parser.add_argument("--api_key", help="Your Reverse WHOIS API key (whoisxmlapi.com)",required=True)
parser.add_argument("--output", help="Output file path", required=True)
parser.add_argument("--org_list", help="File containing a list of organizations (user * for wildcard)")
parser.add_argument("--phone_list", help="File containing a list of phone numbers (user * for wildcard)")
parser.add_argument("--domain_list", help="File containing a list of domain names (user * for wildcard)")
parser.add_argument("--email_list", help="File containing a list of email addresses (user * for wildcard)")
parser.add_argument("--email", help="Single email address (user * for wildcard)")
parser.add_argument("--org", help="Single organization (user * for wildcard)")
parser.add_argument("--phone", help="Single phone number (user * for wildcard)")
parser.add_argument("--domain", help="Single domain name (user * for wildcard)")
parser.add_argument("--sleep", help="Sleep time between each request (default 2 seconds)",type=int,default=2)
parser.add_argument("--maxretry", help="Max retry on failure (default=5)",type=int,default=5)
parser.add_argument("--historic", help="Get Historical domains too (default false)",action='store_true',default=False)

# Parse the command line arguments
args = parser.parse_args()
headers = {"Content-Type": "application/json",
           "X-Authentication-Token": args.api_key
           }

apiKey = args.api_key
output = args.output

orgListfile = args.org_list if args.org_list else ""
phoneListfile = args.phone_list if args.phone_list else ""
domainListfile = args.domain_list if args.domain_list else ""
emailListfile = args.email_list if args.email_list else ""

input_files = {
    'org': orgListfile,
    'phone': phoneListfile,
    'domain': domainListfile,
    'email': emailListfile
}


sleep = args.sleep
historic = args.historic
LastResult = []
for item_type, file_path in input_files.items():
    if file_path:
        item_list = read_file_lines(file_path)
        result = process_items(item_list, item_type, apiKey, historic, sleep, args.sleep, args.maxretry)
        LastResult.extend(result)

input_args = {
    'org': args.org,
    'phone': args.phone,
    'domain': args.domain,
    'email': args.email
}

for item_type, item_value in input_args.items():
    if item_value:
        process_items([item_value], item_type, apiKey, historic, args.sleep, args.maxretry)

finalResult = list(dict.fromkeys(LastResult))
save_list_to_file(output,finalResult)
