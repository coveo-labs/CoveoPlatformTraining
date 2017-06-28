#!/usr/bin/env python

import json
import requests

import config


# Add an identity in a security provider
def push_identity(email):
    identity_api_url = config.get_mapped_identity_api_url()
    coveo_headers = config.get_headers_with_push_api_key()

    identity = json.dumps({
        "Identity": {
            "Name": email,
            "Type": "USER",
            "AdditionalInfo": {}
        },
        "Mappings": [{
            "Name": email,
            "Provider": "Email Security Provider",
            "Type": "USER",
            "AdditionalInfo": {}
        }],
        "WellKnowns": [{
            "Name": "Everyone",
            "Type": "GROUP",
            "AdditionalInfo": {}
        }]
    })

    #print request
    print '\nCall: PUT ' + identity_api_url
    print 'Headers: ' + str(coveo_headers)
    print 'Provider data: ' + identity

    r = requests.put(identity_api_url, headers=coveo_headers, data=identity)

    print r.status_code


def main():
    for identity in config.identities:
        push_identity(identity)


if __name__ == '__main__':
    main()
