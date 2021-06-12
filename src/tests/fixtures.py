PROP_NAME_RESOURCE_PATH = "resource_path"


def get_default_document_filter():
    return {PROP_NAME_RESOURCE_PATH: "periodictable/reactivenonmetals/hydrogen"}


def get_default_json():
    return {
        "state": "gas",
        "weight": 1.008,
        "energy_levels": 1,
        "electronegativity": 2.20,
    }
