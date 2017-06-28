#!/usr/bin/env python

import json
import requests
import zlib
import base64
import dateutil.parser

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

    # Use url as document id
    document_id = post['URL']
    # Retrieve content from the post
    content = post['content']

    compresseddata = zlib.compress(content.encode('utf8'), zlib.Z_BEST_COMPRESSION) # Compress the file content
    encodeddata = base64.b64encode(compresseddata)  # Base64 encode the compressed content

    # create documentId querystring parameter
    params = {
        'documentId': document_id
    }

    body = json.dumps({
        "FileExtension": ".html",
        "CompressedBinaryData": encodeddata,
        "connectortype": "wordpress",
        "title": post['title'],
        "categories": post['categories'].keys(),
        "tags": post['tags'].keys(),
        "date": dateutil.parser.parse(post['date']).strftime('%Y-%m-%d %H:%M:%S')
    })

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
    # Get posts from the JSON data extracted from Wordpress
    with open('wordpress_data.json', 'r') as infile:
        posts = json.load(infile)

    # set status to REBUILD
    set_source_status('REBUILD')

    # loop through each post and add to Coveo
    for post in posts:
        # add document to source
        add_document(post)

    # set status back to IDLE
    set_source_status('IDLE')


if __name__ == '__main__':
    main()
