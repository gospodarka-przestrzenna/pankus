--'import_sd_properties.sql' writes sd_properties table with data exported from python script

INSERT INTO sd_properties VALUES (
    :sd_id,
    :name,
    :value
)
