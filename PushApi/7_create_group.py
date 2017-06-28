#!/usr/bin/env python

import json
import requests

import config

group_name = ''  # TODO Define the group name.


def push_group():
    """
    Adds a group containing all the identities from the config.
    :return: Web request status code.
    """
    identity_api_url = config.get_mapped_identity_api_url()
    coveo_headers = config.get_headers_with_push_api_key()

    members = ''  # TODO Fill the member lists.

    # Constructs the API call payload.
    identity = json.dumps(
        {
            "Identity": {
                "Name": group_name,
                "Type": "GROUP",
                "AdditionalInfo": {}
            },
            "Members": members,
            "WellKnowns": [{
                "Name": "Everyone",
                "Type": "GROUP",
                "AdditionalInfo": {}
            }]
        })

    # Print request
    print '\nCall: PUT ' + identity_api_url
    print 'Headers: ' + str(coveo_headers)
    print 'Provider data: ' + identity

    r = requests.put(identity_api_url, headers=coveo_headers, data=identity)

    print r.status_code


def main():
    """
    Main function of the script.
    Push a new group to the existing security provider.
    """
    push_group()


if __name__ == '__main__':
    main()
