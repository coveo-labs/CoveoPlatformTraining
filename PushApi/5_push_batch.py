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


def upload_batch_to_s3(upload_link, batch):
    """
    Upload the given json file to S3.
    :param upload_link: Link to the S3 bucket.
    :param batch: JSON file in a valid format as specified by the Push API spec.
    :return: Web request's status code.
    """
    s3_headers = {
        # TODO Add the required headers for this S3 API call.
    }

    # print request
    print 'Calling: PUT ' + upload_link

    r = requests.put(upload_link, headers=s3_headers, data=json.dumps(batch))

    print r.status_code


def push_document_batch(fileId):
    """
    Push the previously uploaded documents to the Push source.
    The Push API knows which source is concerned based on the given file id.
    :param fileId: File id to push.
    :return: Web request's status code.
    """
    coveo_document_batch_api_url = config.get_document_batch_api_url()
    coveo_headers = config.get_headers_with_push_api_key()

    # create documentId querystring parameter
    params = {
        # TODO Add the required header to push the json file you uploaded to S3 to your source.
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
        # TODO Add the required header to push the json file you uploaded to S3 to your source.
    }

    # print request
    print '\nCall: PUT ' + coveo_permission_batch_api_url
    print 'Headers: ' + str(coveo_headers)
    print 'Params: ' + str(params)

    r = requests.put(coveo_permission_batch_api_url, headers=coveo_headers, params=params)

    print r.status_code


def main():
    """
    Main function of the script.
    Loops through every posts, adds them to a json, uploads it and push it to the source.
    :return:
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
        # TODO Add every documents to the AddOrUpdate's value. This dictionary will then be
        # TODO serialized as a json string.

    # TODO Get your S3 bucket infos.
    uploadUrl = ''
    fileId = ''

    upload_batch_to_s3(s3_container['uploadUri'], create_permission_batch())
    push_permission_batch(s3_container['fileId'])

    upload_batch_to_s3(s3_container['uploadUri'], batch)
    push_document_batch(s3_container['fileId'])

    set_source_status('IDLE')


if __name__ == '__main__':
    main()
