-- gets the metadata of the database related to the key

SELECT value FROM metadata WHERE key = :key
