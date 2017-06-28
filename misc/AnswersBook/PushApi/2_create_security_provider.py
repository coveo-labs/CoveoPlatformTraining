#!/usr/bin/env python

import json
import requests

import config

# Endpoints

# Add a securityprovider
def add_securityprovider():
    coveo_headers = config.get_headers_with_push_api_key()
    securityprovider_api_url = config.get_security_provider_api_url()

    securityprovider = json.dumps({
        "name": config.coveo_security_provider_name,
        "type": "EXPANDED",
        "nodeRequired": False,
        "caseSensitive": False,
        "referencedBy": [{
            "id": config.coveo_source_id,
            "type": "SOURCE"
        }],
        "cascadingSecurityProviders": {
            "Email Security Provider": {
                "name": "Email Security Provider",
                "type": "EMAIL"
            }
        }
    })

    #print request
    print 'Call: PUT ' + securityprovider_api_url
    print 'Headers: ' + str(coveo_headers)
    print 'SecurityProvider: ' + securityprovider

    r = requests.put(securityprovider_api_url, headers=coveo_headers, data=securityprovider)

    print r.status_code


def main():
    add_securityprovider()


if __name__ == '__main__':
    main()
