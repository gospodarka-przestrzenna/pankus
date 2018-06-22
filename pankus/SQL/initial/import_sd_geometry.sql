--'import_sd_geometry.sql' writes 'sd_geometry' table with data exported from python script

INSERT INTO sd_geometry VALUES (
    :sd_id,
    :point
)
