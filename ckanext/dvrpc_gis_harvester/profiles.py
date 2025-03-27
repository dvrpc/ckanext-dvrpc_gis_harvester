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

        # use rdflib's graph.value() convenience function to get the value of source (which is
        # named "agency" in the GIS data catalog)
        # see <https://rdflib.readthedocs.io/en/stable/intro_to_graphs.html#graph-methods-for-accessing-triples>
        source = self.g.value(
            subject=dataset_ref,
            predicate=URIRef("http://www.w3.org/ns/dcat#agency"),
        )
        dataset_dict["source"] = source

        # assign geo-spatial data type
        dataset_dict["dataset_level"] = "Geospatial"

        # parse the extras/theme field (which looks like a list, but is a string),
        # and put additional values into the category list
        dataset_dict["category"] = []
        if "extras" in dataset_dict:
            for each in dataset_dict["extras"]:
                if each["key"] == "theme":
                    if "Biota" in each["value"]:
                        dataset_dict["category"].append("Environment")
                    if "Boundaries" in each["value"]:
                        dataset_dict["category"].append("Boundaries")
                    if "Demographics" in each["value"]:
                        dataset_dict["category"].append("Demographics & Housing")
                    if "Equity and Diversity" in each["value"]:
                        dataset_dict["category"].append("Equity & Diversity")
                    if "Economy" in each["value"]:
                        dataset_dict["category"].append("Economy")
                    if "Environment" in each["value"]:
                        dataset_dict["category"].append("Environment")
                    if "Freight" in each["value"]:
                        dataset_dict["category"].append("Freight & Aviation")
                    if "Geology" in each["value"]:
                        dataset_dict["category"].append("Environment")
                    if "Hydrography" in each["value"]:
                        dataset_dict["category"].append("Environment")
                    if "Imagery and Elevation" in each["value"]:
                        dataset_dict["category"].append("Imagery")
                    if "Location" in each["value"]:
                        dataset_dict["category"].append("Boundaries")
                    if "Parcels" in each["value"]:
                        dataset_dict["category"].append("Planning")
                    if "Planning" in each["value"]:
                        dataset_dict["category"].append("Planning")
                    if "Long-Range Plan" in each["value"]:
                        dataset_dict["category"].append("Long-Range Plan")
                    if "Structures" in each["value"]:
                        dataset_dict["category"].append("Planning")
                    if "Bicycle and Pedestrian" in each["value"]:
                        dataset_dict["category"].append("Bicycle & Pedestrian")
                    if "Roadways" in each["value"]:
                        dataset_dict["category"].append("Roadways")
                    if "TIP" in each["value"]:
                        dataset_dict["category"].append("TIP")
                    if "Transit" in each["value"]:
                        dataset_dict["category"].append("Transit")
                    if "Transportation" in each["value"]:
                        dataset_dict["category"].append("Transit")    
                    if "Safety and Health" in each["value"]:
                        dataset_dict["category"].append("Safety & Health")
                    if "Utilities" in each["value"]:
                        dataset_dict["category"].append("Environment")

        if "notes" not in dataset_dict:
            dataset_dict["notes"] = "No description"

        # We don't use tags in CKAN, but in the GIS datasets, we use the "keywords"
        # field (which gets automatically converted to "tags") to contain posting freq
        dataset_dict["posting_frequency"] = "as_needed"

        if "tags" in dataset_dict:
            for tag in dataset_dict["tags"]:
                if tag["name"] == "daily":
                    dataset_dict["posting_frequency"] = "daily"
                if tag["name"] == "weekly":
                    dataset_dict["posting_frequency"] = "weekly"
                if tag["name"] == "quarterly":
                    dataset_dict["posting_frequency"] = "quarterly"
                if tag["name"] == "biannually":
                    dataset_dict["posting_frequency"] = "biannually"
                if tag["name"] == "annually":
                    dataset_dict["posting_frequency"] = "annually"

        # now delete all the tags
        dataset_dict["tags"] = []

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
                    if resource["name"].lower() == "network location" and "access_url" in resource:
                        resource["local_path"] = resource["access_url"]
                        if resource.get("url"):
                            resource["url"] = ""
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
            dataset_dict["private"] = "True"

        return dataset_dict
