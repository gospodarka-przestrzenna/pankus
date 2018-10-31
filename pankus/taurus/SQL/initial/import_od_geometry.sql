--'import_od_geometry.sql' writes 'od_geometry' table with data exported from python script

INSERT INTO od_geometry VALUES (
    :od_id,
    :point
)
