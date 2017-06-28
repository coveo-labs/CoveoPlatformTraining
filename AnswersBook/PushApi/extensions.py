#
#  AllFieldsValues
#

import json

values = dict()

for step in document_api.v1.get_meta_data():
    for metaname, metavalues in step.values.iteritems():
        values[metaname] = metavalues
document_api.v1.add_meta_data({"allfieldvalues": json.dumps(values)})


#
#  CleanCategory - Sort documents in 3 categories: Coveo related, Programming and MC+A related.
#   based on current value in `category`.
#

def get_flattened_meta():
    flattened = dict()
    for step in document_api.v1.get_meta_data():
        for metaname, metavalues in step.values.iteritems():
            flattened[metaname.lower()] = metavalues

    normalized = dict()
    for metaname, metavalues in flattened.iteritems():
        if len(metavalues) == 1:
            normalized[metaname] = metavalues[0]
        elif len(metavalues) > 1:
            normalized[metaname] = ";".join([value.encode('utf-8') for value in metavalues])
    return normalized

cleancategories = {
    "Edge Case": "Coveo related",
    "Template": "Coveo related",
    "jsui": "Coveo related",
    "Sitecore": "Coveo related",
    "Markup": "Programming",
    "Javascript": "Programming",
    "Programming": "Programming",
    "Typescript": "Programming"
}

meta_data = get_flattened_meta()

cleancategory = "MC+A related" # default value if no category 

if "category" in meta_data:
    if meta_data["category"] in cleancategories:
        cleancategory = cleancategories[meta_data["category"]]
    else:
        cleancategory = "Other topics"

document_api.v1.add_meta_data({"cleancategory": cleancategory})
