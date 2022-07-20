# ckanext-dvrpc_gis_harvester

This is a custom harvester built to import DVRPC's GIS datasets into our CKAN instance. For installation in general, see the Ansible role: <https://github.com/dvrpc/ckan-ansible/tree/main/roles/dvrpc_gis_harvester>.

When setting up the harvest (at URL/harvest) there are multiple settings. These are the ones that have specific requirements:

  * Url: https://arcgis.dvrpc.org/dvrpc/apps/data.json
  * Source Type: Generic DCAT RDF Harvester
  * Configuration: {"rdf_format":"json-ld"}
  * Organization: the ckan org this is under (dvrpc)

The profiles.py file in ckanext/dvrpc_gis_harvester does the majority of the work of the plugin.

Note that there are some fields in the GIS DCAT that are not standard/aren't automatically handled by the CKAN DCAT plugin that this is built on top of. For instance, there is no "agency" field. So a little extra work is required to use it (and in this case rename it to "source"):

```python
from rdflib.term import URIRef

# use rdflib's graph.value() convenience function to get the value of source (which is
# named "agency" in the GIS data catalog)
# see <https://rdflib.readthedocs.io/en/stable/intro_to_graphs.html#graph-methods-for-accessing-triples>
source = self.g.value(
    subject=dataset_ref,
    predicate=URIRef("http://www.w3.org/ns/dcat#agency"),
)
dataset_dict["source"] = source
```

In general, you can preface the non-standard field name with "http://www.w3.org/ns/dcat#" and it should work. If not, try using this resource to determine the value: <https://issemantic.net/rdf-converter>. Good luck.
