import logging

from rdflib.namespace import Namespace
from rdflib.namespace import RDF

from ckanext.dcat.profiles import RDFProfile

DCT = Namespace("http://purl.org/dc/terms/")
pod = Namespace("https://project-open-data.cio.gov/v1.1/schema/")
log = logging.getLogger(__name__)


class GISProfile(RDFProfile):
    """
    An RDF profile for the Delaware Valley Regional Planning Commission's
    GIS data catalog.
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

        # need to reach into the rdf graph to get the "accessLevel" field.
        # first loop over all the datasets, and for the this dataset (id'd by dataset_ref),
        # pull the field out of the "triple" (subject, predicate, object) that it's in.
        # see <https://rdflib.readthedocs.io/en/stable/gettingstarted.html> for more info

        # there may be a more efficient way, but for now this works

        for s, p, o, g in self.g.quads((None, RDF.type, None, None)):
            if s == dataset_ref:
                for subj, pred, obj in g:
                    if "accessLevel" in pred:
                        if str(obj) == "public":
                            dataset_dict["use_limitations"] = "unrestricted_without_agreement"
                        elif str(obj) == "org":
                            dataset_dict["use_limitations"] = "restricted_all_staff"

                break  # no need to continue further in the loop once we have this

        return dataset_dict
