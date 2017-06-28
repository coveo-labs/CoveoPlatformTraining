#!/usr/bin/env python

import json
import requests
import zlib
import base64
import dateutil.parser

import config


def set_source_status(status):
    """
    Sets the source status via the REST API.
    :param status: Desired status. Must be one of the following values: [REBUILD, REFRESH, INCREMENTAL, IDLE].
    :return: Web request's status code.
    """
    # create statusType query string parameter
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


def get_file_container():
    """
    Gets the informations on the S3 bucket.
    :return: Dictionary containing both 'uploadUri' and 'fileId' keys.
    """
    coveo_file_container_api_url = config.get_file_container_api_url()
    coveo_headers = config.get_headers_with_push_api_key()

    # print request
    print 'Calling: POST ' + coveo_file_container_api_url

    # make POST request a file container url
    r = requests.post(coveo_file_container_api_url, headers=coveo_headers)

    print r.status_code

    return json.loads(r.content)


def upload_batch_to_s3(upload_link, batch):
    """
    Upload the given json file to S3.
    :param upload_link: Link to the S3 bucket.
    :param batch: JSON file in a valid format as specified by the Push API spec.
    :return: Web request's status code.
    """
    s3_headers = {
        'content-type': 'application/octet-stream',
        'x-amz-server-side-encryption': 'AES256'
    }

    # print request
    print 'Calling: PUT ' + upload_link

    r = requests.put(upload_link, headers=s3_headers, data=json.dumps(batch))

    print r.status_code


def push_document_batch(file_id):
    """
    Push the previously uploaded documents to the Push source.
    :param file_id: File id to push.
    :return: Web request's status code.
    """
    coveo_document_batch_api_url = config.get_document_batch_api_url()
    coveo_headers = config.get_headers_with_push_api_key()

    # create documentId querystring parameter
    params = {
        'fileId': file_id
    }

    # print request
    print '\nCall: PUT ' + coveo_document_batch_api_url
    print 'Headers: ' + str(coveo_headers)
    print 'Params: ' + str(params)

    r = requests.put(coveo_document_batch_api_url, headers=coveo_headers, params=params)

    print r.status_code


def push_permission_batch(file_id):
    """
        Push the previously uploaded permissions to the security provider.
        :param file_id: File id to push.
        :return: Web request's status code.
        """
    coveo_permission_batch_api_url = config.get_permission_batch_api_url()
    coveo_headers = config.get_headers_with_push_api_key()

    # create documentId querystring parameter
    params = {
        'fileId': file_id
    }

    # print request
    print '\nCall: PUT ' + coveo_permission_batch_api_url
    print 'Headers: ' + str(coveo_headers)
    print 'Params: ' + str(params)

    r = requests.put(coveo_permission_batch_api_url, headers=coveo_headers, params=params)

    print r.status_code


def add_document_to_batch(batch, post):
    """
    Formats a document in a dictionary and adds it to the given list.
    :param batch: The list in which to add the document.
    :param post: The raw document to process.
    """
    # Use url as document id
    document_id = post['URL']
    # Retrieve content from the post
    content = post['content']

    compresseddata = zlib.compress(content.encode('utf8'), zlib.Z_BEST_COMPRESSION)  # Compress the file content
    encodeddata = base64.b64encode(compresseddata)  # Base64 encode the compressed content

    document = {
        'documentId': document_id,
        "FileExtension": ".html",
        "CompressedBinaryData": encodeddata,
        "connectortype": "wordpress",
        "title": post['title'],
        "categories": post['categories'].keys(),
        "tags": post['tags'].keys(),
        "date": dateutil.parser.parse(post['date']).strftime('%Y-%m-%d %H:%M:%S'),
        "Permissions": [{
            "PermissionSets": [{
                "AllowAnonymous": False,
                "AllowedPermissions": [{
                    "IdentityType": "User",
                    "Identity": config.identities[0]
                }],
                "DeniedPermissions": []
            }]
        }]
    }

    batch['AddOrUpdate'].append(document)


def create_permission_batch():
    return {
        "Mappings": [
            {
                "Identity": {
                    "Name": identity,
                    "Type": "User",
                    "AdditionalInfo": {}
                },
                "Mappings": [
                    {
                        "Name": identity,
                        "Type": "User",
                        "AdditionalInfo": {},
                        "Provider": "Email Security Provider"
                    }
                ],
                "WellKnowns": [
                    {
                        "Name": "Everyone",
                        "Type": "Group",
                        "AdditionalInfo": {}
                    }
                ]
            }
            for identity in config.identities]
    }


def main():
    """
    Main function of the script.
    Loops through every posts, adds them to a json, uploads it and push it to the source.
    Also creates mappings for the identities defined in the config and push them in one batch.
    """
    # Get posts from the JSON data extracted from Wordpress
    with open('wordpress_data.json', 'r') as infile:
        posts = json.load(infile)

    set_source_status('REBUILD')

    # Creates the empty dictionary containing the keys required by the PushAPI.
    batch = {
        'AddOrUpdate': [],
        'Delete': []
    }

    for post in posts:
        # Adds every document to the batch json object.
        add_document_to_batch(batch, post)

    s3_container = get_file_container()

    upload_batch_to_s3(s3_container['uploadUri'], create_permission_batch())
    push_permission_batch(s3_container['fileId'])

    upload_batch_to_s3(s3_container['uploadUri'], batch)
    push_document_batch(s3_container['fileId'])

    set_source_status('IDLE')


if __name__ == '__main__':
    main()
