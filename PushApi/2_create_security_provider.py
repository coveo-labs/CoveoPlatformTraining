#!/usr/bin/env python

import json
import requests
import sys

import config

# Endpoints

coveo_securityprovider_api_url = ''  # TODO find URL to call, see https://platform.cloud.coveo.com/docs
security_provider_name = config.coveo_security_provider_name  # YOUR-SECURITY-PROVIDER-NAME


# Add a securityprovider
def add_securityprovider():
    coveo_headers = config.get_headers_with_push_api_key()

    securityprovider = json.dumps({
        # TODO - Fill in payload, see https://developers.coveo.com/display/CloudPlatform/Creating+an+Identity+Provider+for+a+Secured+Push+Type+Source
    })

    # Print request
    print 'Call: PUT ' + coveo_securityprovider_api_url
    print 'Headers: ' + str(coveo_headers)
    print 'SecurityProvider: ' + securityprovider

    r = requests.put(coveo_securityprovider_api_url, headers=coveo_headers, data=securityprovider)

    print r.status_code


def main():
    # Make a list of command line arguments, omitting the [0] element which is the script itself.
    args = sys.argv[1:]

    add_securityprovider()


if __name__ == '__main__':
    main()
