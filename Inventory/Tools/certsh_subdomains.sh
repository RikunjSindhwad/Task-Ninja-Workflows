#!/bin/sh

# Argscheck
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 [domain] [output_file]"
    exit 1
fi

# Variables
DOMAIN=$1
OUTPUT_FILE=$2

# Query
query="SELECT lower(NAME_VALUE) NAME_VALUE FROM certificate_and_identities WHERE plainto_tsquery('certwatch', '%.$DOMAIN') @@ identities (CERTIFICATE) AND NAME_TYPE LIKE 'san:%';"

# Get and Save Subdomains
(echo $DOMAIN; echo $query | \
    psql --csv -t -h crt.sh -p 5432 -U guest certwatch | \
    grep '\.'$DOMAIN'$' | grep -v '#\| ' | \
    sed -e 's:^*\.::g' -e 's:.*@::g' -e 's:^\.::g') | sort -u | tee "$OUTPUT_FILE"

echo "Output saved to $OUTPUT_FILE"
