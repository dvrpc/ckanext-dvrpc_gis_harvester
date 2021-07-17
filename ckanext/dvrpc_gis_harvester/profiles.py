from ckanext.dcat.profiles import RDFProfile


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
        dataset_dict["use_limitations"] = "unrestricted_without_agreement"
        dataset_dict["agency_owner"] = "dvrpc"

        return dataset_dict
