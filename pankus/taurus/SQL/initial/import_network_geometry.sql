--'import_network_geometry'.sql' writes 'network_geometry' table with data exported from python script

INSERT INTO network_geometry VALUES (
    :start,
    :end,
    :linestring
)
