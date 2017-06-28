#!/usr/bin/env python

import json
import io
import requests
import sys

import config

# Endpoints
wp_oauth2_authorize_url = 'https://public-api.wordpress.com/oauth2/authorize'
wp_oauth2_token_url = 'https://public-api.wordpress.com/oauth2/token'
wp_posts_api_url = 'https://public-api.wordpress.com/rest/v1.1/sites/{siteId}/posts/'

wordpress_headers = {}


# Get Wordpress Access_Token
def get_wp_access_token(wp_client_id, wp_client_secret, wp_username, wp_password):
  # log in to Wordpress to get access_token
    data = {
        'client_id' : wp_client_id,
        'client_secret' : wp_client_secret,
        'grant_type' : 'password',
        'username' : wp_username,
        'password' : wp_password
    }
    print 'Calling: POST ' + wp_oauth2_token_url
    r = requests.post(wp_oauth2_token_url, data=data)

    print 'Response: ' + r.text
    oauth2_response = json.loads(r.text)

    wp_access_token = oauth2_response['access_token']

    print "Wordpress API access_token: " + wp_access_token
    return wp_access_token


# Get Wordpress posts
def get_wp_posts():
    page_num = 1
    posts = []
    while True:
        print 'Calling: GET ' + wp_posts_api_url + '?context=edit&page=' + str(page_num)

        r = requests.get(wp_posts_api_url + '?context=edit&page=' + str(page_num), headers=wordpress_headers)
        page_num += 1

        posts_response = json.loads(r.text)

        if len(posts_response[u'posts']) == 0:
            break

        for post in posts_response[u'posts']:
            formatedPost = {
                u'url': post[u'URL'],
                u'title': post[u'title'],
                u'date': post[u'date'],
                u'content': post[u'content'],
                u'categories': post[u'categories'].keys(),
                u'tags': post[u'tags'].keys()
            }

            posts.append(formatedPost)


     return posts



def main():
    # Make a list of command line arguments, omitting the [0] element which is the script itself.
    args = sys.argv[1:]

    # construct WP API URLs
    global wp_posts_api_url
    wp_posts_api_url = wp_posts_api_url.format(
        siteId = config.wp_site_id
    )

    # get wordpress access_token
    wp_access_token = get_wp_access_token(config.wp_client_id, config.wp_client_secret, config.wp_username, config.wp_password)

    # create Authorization (access_token) and content-type (json) headers
    global wordpress_headers
    wordpress_headers = {
        'Authorization': 'Bearer ' + wp_access_token,
        'content-type': 'application/json'
    }

    # get wordpress posts
    posts = get_wp_posts()

    # Write posts in a file
    with io.open('wordpress_data.json', 'w', encoding='utf8') as f:
        f.write( json.dumps(posts, ensure_ascii=False, indent=4) )


if __name__ == '__main__':
    main()
