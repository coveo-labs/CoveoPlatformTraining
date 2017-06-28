# Indexing data using the Push API

Your goal is to create a Push connector to add data from a WordPress blog into a Push source in your index.

## Before you start

Scripts are written in **Python**. So you need to have Python **2.7** installed on your machine if you wish to use our starting points.
You can use other languages if you prefer (JavaScript/NodeJS for example).

The blog we are using for this tutorial is [CoveoPushDemo.WordPress.com](https://coveopushdemo.wordpress.com).
We already extracted the data for you in a .json file.

There is good documentation on [Coveo developers site](https://developers.coveo.com).


## Create a Coveo Org

An organization might have been already created for you. If so, skip to the next section.

First, you need to register in the platform.

1. Go to [Platform Swagger UI](https://platform.cloud.coveo.com/docs)
1. Expand `POST /rest/organizations`
1. Click on the `on/off` button to the right to authenticate.
1. Register user (or Login with a Google email)
1. Go back to [Platform Swagger UI](https://platform.cloud.coveo.com/docs)
1. Expand `POST /rest/organizations` again
1. Create an org - *Be mindful of the name, id can be different.*

## Access your organization

1. Go in https://platform.cloud.coveo.com
1. Provide your credentials.
1. In the drop down list in the top right corner, find your organization.

If you only have access to this one organization, it will be the only one available in the drop down.

## Create your first source:

1. Index first source: Sitemap Connector on http://www.mcplusa.com/sitemap_index.xml

## Create a Custom Connector Lab

Reference: https://developers.coveo.com/display/public/CloudPlatform/Push+API+Usage+Overview

The PushAPI repertory contains incomplete python script that you will use to interact with the Push API. In these scripts, look for TODOs to find the places where you should add your code the the scripts.

You will need to know your organization and source ids, this is the easiest way to find this information: https://developers.coveo.com/display/public/CloudPlatform/Parameters+and+API+Calls

### Push documents without security

1. Review the JSON data we extracted from the WordPress blog: `wordpress_data.json`.
1. Create Push source in https://platform.cloud.coveo.com setting it as a Private source and checking the option to create an API key.
1. Validate the key’s privileges. You should have `Content/Sources` (View and Edit).
1. Set up mappings for the metadata that you wish to map to fields on your documents. You can look into 
1. Update `config.py` with your info (org name, source id, keys).
1. Update `1_push_from_worpress.py` and complete the script (look for **TODOs**) to push the data

  Some helpful references:
  https://developers.coveo.com/display/CloudPlatform/Pushing+Items+to+a+Source
  https://developers.coveo.com/display/CloudPlatform/Push+API+Reference
  Swagger: https://platform.cloud.coveo.com/docs

  You can use the **Content Browser** in the [Admin UI](https://platform.cloud.coveo.com/admin) to see if your content was added to the index.

### Add security to your source

Refer to https://developers.coveo.com/display/CloudPlatform/Pushing+Identities+to+an+Identity+Provider to understand how to push new identities to your organization.

You can create a new user identity on its own but, to be able to view the documents that this user have access to, you need to map to the user that will login to your search page. For example, if you login with Google, you will need to map your new user identity to your Google email. This allows the security provider to give you access to all your different usernames accross all sources.

Refering to the aforementioned documentation, you can either create the identity and then map it to another email or simply start by creating the mapping. The user identity will automatically created.

1. Change your source to be **Secured**.
1. Add these privileges to your API key: `Content/Security identities` and `Content/Security identity providers` with both **View** and **Edit**.
1. Create new Security provider. For this, complete the script `2_create_security_provider.py`
1. Create identities in the new Security provider. Using the email addresses (defined in `config.py`) ideally ones that can be used with Google, use the script `3_create_identities.py` to add them.

### Push data with security
1. Using `4_push_secured.py`, push Wordpress content again with permission on documents.
  Set up permissions, choosing user should see the content based on Title

  You can use the **Content Browser** in the [Admin UI](https://platform.cloud.coveo.com/admin) to see if your content was added to the index. You should less items now for Wordpress, only the ones for your user.

### Push documents in batch

The following documentation (https://developers.coveo.com/display/public/CloudPlatform/Batch+Pushing+Encrypted+Files+and+Permissions+to+a+Source) explains how you can push a batch of documents at once to your source. This removes the need to call the Push API multiple times and will speed up the process of pushing documents.

1. Update the `5_push_batch.py` script to handle:
    1. Create the content JSON file.
    2. Request your S3 upload link.
    3. Upload your JSON file to S3.
    4. Push it from S3 to your source.
2. After a few minutes, ensure that all your documents are now indexed.

The same documentation explains how you can push permissions in batch. You should modify your script to handle that too. For example, you might want to push all the identities that you defined in the config file in one batch. You can use the file S3 upload link for all of these operations.

  
### Use extensions

1. In the [Admin UI](https://platform.cloud.coveo.com/admin), create a new extension. 
    -As an example, you could create an extension that adds all metadatas from a document to one single additional metadata. This can be very useful when debugging.
    -https://developers.coveo.com/display/public/CloudPlatform/Inspecting+All+Available+Metadata+Values
2. Create the required field for your extension. If you used the above example, you need to create a field to contain your new metadata.
3. On your source, create the mapping to map your new metadata to your new field. Keep in mind that if both your metadata and your field have the same name, the mapping is optional.
4. Apply the extension to your source. This is done via the API as described here: https://developers.coveo.com/display/public/CloudPlatform/Applying+an+Indexing+Pipeline+Extension+to+a+Source+with+the+API
5. You will now need to rebuild your source. In the context of a push source, this means to push all your documents again.

All your documents will now go through the extension script when they are indexed. Open one document in the content browser to confirm that it worked. If you used the allmetadatavalue example, you should now see the new field on every document.

### Add security with groups

Instead of using a list of users, you can define a group and use it to define the permissions of a document. The members of a group can be identities that you created in the previous steps or other groups.

1. Modify the script `7_create_group` to handle the addition of a new group with its members.
2. You can now push a document using this group as allowed entity. To do this, either modify your `3_create_identities.py` to use this group or interact directly with the Push API.
3. You should now see the group and its members and in the permissions of the documents.

### Want to do more?

Consider these activities:

* Secure documents using Groups instead of Users.
  https://developers.coveo.com/display/CloudPlatform/Batch+Pushing+Encrypted+Files+and+Permissions+to+a+Source
