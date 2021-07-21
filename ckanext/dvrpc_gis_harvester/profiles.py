import logging

from ckanext.dcat.profiles import RDFProfile

log = logging.getLogger(__name__)


class GISProfile(RDFProfile):
    """
    An RDF profile based on the DCAT-AP for data portals in Europe

    More information and specification:

    https://joinup.ec.europa.eu/asset/dcat_application_profile

    """

    def parse_dataset(self, dataset_dict, dataset_ref):
        dataset_dict["staff_contact"] = "Sean Lawrence"
        dataset_dict["staff_contact_email"] = "slawrence@dvrpc.org"
        dataset_dict["category"] = "GIS"
        dataset_dict["posting_frequency"] = "as_needed"
        dataset_dict["agency_owner"] = "dvrpc"
        dataset_dict["tags"] = []
        if "notes" not in dataset_dict:
            dataset_dict["notes"] = "No description"

        # remove Shapefiles from list of resources
        # (these should be accessed via filesystem)
        if "resources" in dataset_dict:
            updated_resources = []
            for resource in dataset_dict["resources"][:]:
                if resource["name"] != "Shapefile":
                    updated_resources.append(resource)
            dataset_dict["resources"] = updated_resources

        # this one still needs work
        dataset_dict["use_limitations"] = "unrestricted_without_agreement"

        return dataset_dict
