#!/usr/bin/env python

import json
import re
import requests
import urllib
import sys
import time
import zlib
import base64

import config

# Set the source status
def set_source_status(status):
    # create statusType querystring parameter
    params = {
        'statusType': status
    }

    coveo_status_api_url = config.get_status_api_url()
    coveo_headers = config.get_headers_with_push_api_key()

    #print request
    print 'Calling: POST ' + coveo_status_api_url
    print 'statusType: ' + status

    # make POST request to change status
    r = requests.post(coveo_status_api_url, headers=coveo_headers, params=params)

    print r.status_code


# Add a document
def add_document(post):

    document_id = # TODO - Use post's url as document id
    content = # TODO - Retrieve content from the post

    # Compress and Base64 encode the content
    compresseddata = zlib.compress(content.encode('utf8'), zlib.Z_BEST_COMPRESSION)
    encodeddata = base64.b64encode(compresseddata)

    # set to first email if title starts with A-M, otherwise to the second
    user_email = config.identities[0] if reAtoM.match(post['title']) else config.identities[1]

    print '\nUser %s for title "%s"' % (user_email, post['title'])

    body = json.dumps({
        # TODO - can we suggest adding title, categories, tags, date and a connectortype?
        # TODO - Don't forget to add their mappings on the source.
        # TODO -
        "FileExtension": ".html",
        "CompressedBinaryData": encodeddata
    })

    # create documentId querystring parameter
    params = {
        'documentId': document_id
    }

    coveo_document_api_url = config.get_document_api_url()
    coveo_headers = config.get_headers_with_push_api_key()

    #print request
    print '\nCall: PUT ' + coveo_document_api_url
    print 'Headers: ' + str(coveo_headers)
    print 'Params: ' + str(params)
    print 'Body: ' + body

    r = requests.put(coveo_document_api_url, headers=coveo_headers, params=params, data=body)

    if r.status_code == 202:
        print 'SUCCESS [%s]' % document_id
    else:
        print r.text


def main():
    # Make a list of command line arguments, omitting the [0] element which is the script itself.
    args = sys.argv[1:]

    # Get posts from the JSON data extracted from Wordpress
    with open('wordpress_data.json', 'r') as infile:
        posts = json.load(infile)

    # set status to REBUILD
    set_source_status('REBUILD')

    global reAtoM
    reAtoM = re.compile("^[A-M]", re.IGNORECASE)

    # loop through each post and add to Coveo
    for post in posts:
        add_document(post)


    # set status back to IDLE
    set_source_status('IDLE')



if __name__ == '__main__':
    main()
