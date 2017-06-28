#!/usr/bin/env python

import json
import requests
import sys

import config

# Endpoints
coveo_identity_api_url = config.get_mapped_identity_api_url()
security_provider_name = config.coveo_security_provider_name  # YOUR-SECURITY-PROVIDER-NAME

# Add an identity in a security provider
def push_identity(email):
    identity_api_url = coveo_identity_api_url.format(
        organizationId = config.coveo_organization_id,
        providerId = security_provider_name
    )
    coveo_headers = config.get_headers_with_push_api_key()

    identity = json.dumps({
        # TODO - Fill in payload, see https://developers.coveo.com/display/CloudPlatform/Pushing+Identities+to+an+Identity+Provider
    })

    #print request
    print '\nCall: PUT ' + identity_api_url
    print 'Headers: ' + str(coveo_headers)
    print 'Provider data: ' + identity

    r = requests.put(identity_api_url, headers=coveo_headers, data=identity)

    if r.status_code == 202:
        print 'SUCCESS'
    else:
        print r.text

def main():
    # Make a list of command line arguments, omitting the [0] element which is the script itself.
    args = sys.argv[1:]

    for identity in config.identities:
        push_identity(identity)


if __name__ == '__main__':
    main()
