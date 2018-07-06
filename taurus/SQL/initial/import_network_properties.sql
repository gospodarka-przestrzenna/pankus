--'import_network_properites.sql' writes 'network_properties' table with data exported from python script

INSERT INTO network_properties VALUES (
    :start,
    :end,
    :name,
    :value
)
