--'import_od_properties.sql' writes od_properties table with data exported from python script

INSERT INTO od_properties VALUES (
    :od_id,
    :name,
    :value
)
