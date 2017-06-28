#!/usr/bin/env python

use_dev_environment = False
use_qa_environment = False

# WordPress constants
wp_site_id = 'coveopushdemo.wordpress.com'
wp_client_id = '49298'
wp_client_secret = 'CLIENT-SECRET'
wp_username = 'USERNAME'
wp_password = 'PASSWORD'

# Coveo constants
coveo_push_environment = 'push' + ('dev' if use_dev_environment else 'qa' if use_qa_environment else '')
coveo_platform_url = 'platform' + ('dev' if use_dev_environment else 'qa' if use_qa_environment else '')
coveo_organization_id = ''
coveo_source_id = ''
coveo_push_api_key = ''
coveo_security_provider_name = ''

identities = [
    'user1@domain.com',
    'user2@domain.com'
]

# Endpoints
coveo_document_api_url = 'https://{pushEnv}.cloud.coveo.com/v1/organizations/{organizationId}/sources/{sourceId}/documents'
coveo_document_batch_api_url = 'https://{pushEnv}.cloud.coveo.com/v1/organizations/{organizationId}/sources/{sourceId}/documents/batch'
coveo_permission_batch_api_url = 'http://{pushEnv}.cloud.coveo.com/v1/organizations/{organizationId}/providers/{providerId}/permissions/batch'
coveo_security_provider_api_url = 'https://{platformEnv}.cloud.coveo.com/rest/organizations/{organizationId}/securityproviders/{providerId}'
coveo_mapped_identity_api_url = 'https://{pushEnv}.cloud.coveo.com/v1/organizations/{organizationId}/providers/{providerId}/mappings'
coveo_identity_api_url = 'https://{pushEnv}.cloud.coveo.com/v1/organizations/{organizationId}/providers/{providerId}/permissions'
coveo_status_api_url = 'https://{pushEnv}.cloud.coveo.com/v1/organizations/{organizationId}/sources/{sourceId}/status'
coveo_file_container_url = 'https://{pushEnv}.cloud.coveo.com/v1/organizations/{organizationId}/files'


# Construct Coveo API URLs
def get_document_api_url():
    return coveo_document_api_url.format(
        pushEnv=coveo_push_environment,
        organizationId=coveo_organization_id,
        sourceId=coveo_source_id
    )


def get_document_batch_api_url():
    return coveo_document_batch_api_url.format(
        pushEnv=coveo_push_environment,
        organizationId=coveo_organization_id,
        sourceId=coveo_source_id
    )


def get_permission_batch_api_url():
    return coveo_permission_batch_api_url.format(
        pushEnv=coveo_push_environment,
        organizationId=coveo_organization_id,
        providerId=coveo_security_provider_name
    )


def get_security_provider_api_url():
    return coveo_security_provider_api_url.format(
        platformEnv=coveo_platform_url,
        organizationId=coveo_organization_id,
        providerId=coveo_security_provider_name
    )


def get_mapped_identity_api_url():
    return coveo_mapped_identity_api_url.format(
        pushEnv=coveo_push_environment,
        organizationId=coveo_organization_id,
        providerId=coveo_security_provider_name
    )


def get_identity_api_url():
    return coveo_identity_api_url.format(
        pushEnv=coveo_push_environment,
        organizationId=coveo_organization_id,
        providerId=coveo_security_provider_name
    )


def get_status_api_url():
    return coveo_status_api_url.format(
        pushEnv=coveo_push_environment,
        organizationId=coveo_organization_id,
        sourceId=coveo_source_id
    )


def get_file_container_api_url():
    return coveo_file_container_url.format(
        pushEnv=coveo_push_environment,
        organizationId=coveo_organization_id
    )


# Create Authorization (access_token) and content-type (json) headers
def get_headers_with_push_api_key():
    return {
        'Authorization': 'Bearer ' + coveo_push_api_key,
        'content-type': 'application/json'
    }
