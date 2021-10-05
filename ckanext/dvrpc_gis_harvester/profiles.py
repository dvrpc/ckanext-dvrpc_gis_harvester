import logging

from rdflib.namespace import Namespace
from rdflib.term import URIRef

from ckanext.dcat.profiles import RDFProfile

DCT = Namespace("http://purl.org/dc/terms/")

log = logging.getLogger(__name__)


class GISProfile(RDFProfile):
    """
    An RDF profile for the Delaware Valley Regional Planning Commission's
    GIS data catalog.
    """

    def parse_dataset(self, dataset_dict, dataset_ref):
        log.debug("Parsing with DVRPC's GISProfile")
        dataset_dict["staff_contact"] = "DVRPC GIS"
        dataset_dict["staff_contact_email"] = "gis@dvrpc.org"
        dataset_dict["category"] = "GIS"
        dataset_dict["posting_frequency"] = "as_needed"
        dataset_dict["agency_owner"] = "dvrpc"
        dataset_dict["agency_owner_alt"] = ""
        dataset_dict["tags"] = []

        if "notes" not in dataset_dict:
            dataset_dict["notes"] = "No description"

        # limit resources imported
        if "resources" in dataset_dict:
            updated_resources = []
            for resource in dataset_dict["resources"][:]:
                if resource["name"] in [
                    "GeoJSON",
                    "Esri Rest API",
                    "DVRPC GIS Catalog",
                    "Metadata XML",
                    "Network Location",
                ]:
                    # change the field that the value for Network Location does
                    if resource["name"] == "Network Location" and "access_url" in resource:
                        resource["local_path"] = resource["access_url"]
                        del resource["url"]
                        del resource["description"]
                    updated_resources.append(resource)

            dataset_dict["resources"] = updated_resources

        # use rdflib's graph.value() convenience function to get the value of accessLevel
        # see <https://rdflib.readthedocs.io/en/stable/intro_to_graphs.html#graph-methods-for-accessing-triples>
        access_level = self.g.value(
            subject=dataset_ref,
            predicate=URIRef("https://project-open-data.cio.gov/v1.1/schema#accessLevel"),
        )

        if str(access_level) == "public":
            dataset_dict["use_limitations"] = "unrestricted_without_agreement"
        elif str(access_level) == "org":
            dataset_dict["use_limitations"] = "restricted_all_staff"

        return dataset_dict
