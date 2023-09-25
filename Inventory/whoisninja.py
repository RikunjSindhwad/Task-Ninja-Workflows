#!/usr/local/bin/python
import sys
import argparse
import time
import requests
import json
url = "https://reverse-whois.whoisxmlapi.com/api/v2"
headers = {"Content-Type": "application/json"}

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
            
def reverseWhois(input,api_key,type):
    
    finalResult = []
    fields = getFeilds(type)
    # print(fields)
    print(f"[Start] Identifying Domains Through '{type}': '{input}'",file=sys.stderr)
    exectMatch = True
    if "*" in input:
        exectMatch = False
    for field in fields:
        advanced_terms = [{
            'field': field,
            'term': input
        }]
        try:
            search_body = {
                "apiKey": api_key,
                "searchType": "historic",
                "mode": "purchase",
                'exactMatch': exectMatch,
                "advancedSearchTerms":advanced_terms
                    }
            resp = requests.post(url,headers=headers,json=search_body)
            domainList = json.loads(resp.text)["domainsList"]
        except Exception as e:
            print(f"Error: {e}",file=sys.stderr)
            sys.exit(1)
        for domain in domainList:
            finalResult.append(domain)
    finalResult = list(set(finalResult))
    print(f"[Done] Identified Total '{len(finalResult)}' Domains Through '{type}':'{input}'",file=sys.stderr)
    return finalResult

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

# Parse the command line arguments
args = parser.parse_args()

apiKey = args.api_key
output = args.output

orgListfile = args.org_list if args.org_list else ""
phoneListfile = args.phone_list if args.phone_list else ""
domainListfile = args.domain_list if args.domain_list else ""
emailListfile = args.email_list if args.email_list else ""
sleep = args.sleep

LastResult = []
if orgListfile != "":
    orgList = read_file_lines(orgListfile)
    for org in orgList:
        org = org.strip()
        result = reverseWhois(org,apiKey,"org")
        LastResult.extend(result)
        time.sleep(sleep)
if phoneListfile != "":
    phoneList = read_file_lines(phoneListfile)
    for phone in phoneList:
        phone = phone.strip()
        result = reverseWhois(phone,apiKey,"phone")
        LastResult.extend(result)
        time.sleep(sleep)
if domainListfile != "":
    domainList = read_file_lines(domainListfile)
    for domain in domainList:
        domain = domain.strip()
        result = reverseWhois(domain,apiKey,"domain")
        LastResult.extend(result)
        time.sleep(sleep)
if emailListfile != "":
    emailList = read_file_lines(emailListfile)
    for email in emailList:
        email = email.strip()
        result = reverseWhois(email,apiKey,"email")
        LastResult.extend(result)
        time.sleep(sleep)
if args.email:
    email = args.email.strip()
    result = reverseWhois(email,apiKey,"email")
    LastResult.extend(result)
if args.org:
    org = args.org.strip()
    result = reverseWhois(org,apiKey,"org")
    LastResult.extend(result)
if args.phone:
    phone = args.phone.strip()
    result = reverseWhois(phone,apiKey,"phone")
    LastResult.extend(result)
if args.domain:
    domain = args.domain.strip()
    result = reverseWhois(domain,apiKey,"domain")
    LastResult.extend(result)

finalResult = list(dict.fromkeys(LastResult))
save_list_to_file(output,finalResult)
