from reversewhois import * 
import sys
import argparse

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
            return [Fields.admin_contact_email, Fields.registrant_contact_email, Fields.tech_contact_email,Fields.billing_contact_email]
        case "org":
            return [Fields.admin_contact_organization,Fields.billing_contact_organization,Fields.registrant_contact_organization,Fields.tech_contact_organization]
        case "phone":
            return [Fields.admin_contact_telephone,Fields.billing_contact_telephone,Fields.registrant_contact_telephone,Fields.tech_contact_telephone]
        case "domain":
            return [Fields.domain_name]
            
def reverseWhois(input,client,type):
    
    finalResult = []
    
    fields = getFeilds(type)
    # print(fields)
    print(f"[Start] Identifying Domains Through '{type}' against '{input}'",file=sys.stderr)
    for field in fields:
        advanced_terms = [{
            'field': field,
            'term': input
        }]
        try:
            result = client.purchase(advanced_terms=advanced_terms,responseFormat=Client.JSON_FORMAT,searchType="historic",mode="purchase")
        except Exception as e:
            print(f"Error: {e}",file=sys.stderr)
            sys.exit(1)
        domainList = result.domains_list
        for domain in domainList:
            finalResult.append(domain['domain_name'])    
    # finalResult = list(set(finalResult))
    print(f"[Done] Identified Total '{len(finalResult)}' Domains Through '{type}' against '{input}'",file=sys.stderr)
    # print(finalResult[1])
    return finalResult

parser = argparse.ArgumentParser(description="Reverse WHOIS lookup script by robensive (Rikunj Sindhwad)")
parser.add_argument("--api_key", help="Your Reverse WHOIS API key (whoisxmlapi.com)",required=True)
parser.add_argument("--output", help="Output file path", required=True)
parser.add_argument("--org_list", help="File containing a list of organizations")
parser.add_argument("--phone_list", help="File containing a list of phone numbers")
parser.add_argument("--domain_list", help="File containing a list of domain names")
parser.add_argument("--email_list", help="File containing a list of email addresses")

# Parse the command line arguments
args = parser.parse_args()

apiKey = args.api_key
output = args.output

orgListfile = args.org_list if args.org_list else ""
phoneListfile = args.phone_list if args.phone_list else ""
domainListfile = args.domain_list if args.domain_list else ""
emailListfile = args.email_list if args.email_list else ""


client = Client(api_key=apiKey)
LastResult = []
if orgListfile != "":
    orgList = read_file_lines(orgListfile)
    for org in orgList:
        org = org.strip()
        result = reverseWhois(org,client,"org")
        LastResult.extend(result)
if phoneListfile != "":
    phoneList = read_file_lines(phoneListfile)
    for phone in phoneList:
        phone = phone.strip()
        result = reverseWhois(phone,client,"phone")
        LastResult.extend(result)
if domainListfile != "":
    domainList = read_file_lines(domainListfile)
    for domain in domainList:
        domain = domain.strip()
        result = reverseWhois(domain,client,"domain")
        LastResult.extend(result)
if emailListfile != "":
    emailList = read_file_lines(emailListfile)
    for email in emailList:
        email = email.strip()
        result = reverseWhois(email,client,"email")
        LastResult.extend(result)


finalResult = list(dict.fromkeys(LastResult))
save_list_to_file(output,finalResult)
