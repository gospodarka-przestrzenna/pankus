WITH
    min_connection_mst(src,minimum) AS (
        SELECT
            source.bmst_supernode as src,
            min(bmst_connection.weight) as minimum
        FROM
            bmst_connection,
            bmst AS source,
            bmst AS destination
        WHERE
            source.level=(SELECT max(level) FROM bmst) AND
            destination.level=(SELECT max(level) FROM bmst) AND
            source.bmst_supernode!=destination.bmst_supernode AND
            source.bmst_id=bmst_connection.bmst_start_id AND
            destination.bmst_id=bmst_connection.bmst_end_id
        GROUP BY
            source.bmst_supernode
    ),
    connection_mst(src,dst,level,minimum) AS (
        SELECT DISTINCT
            source.bmst_id as src,
            destination.bmst_id as dst,
            (source.level+1),
            minconn.minimum
        FROM
            min_connection_mst as minconn,
            bmst_connection,
            bmst AS source,
            bmst AS destination

        WHERE
            bmst_connection.weight=minconn.minimum AND
            minconn.src=source.bmst_supernode AND
            source.bmst_id=bmst_connection.bmst_start_id AND
            destination.bmst_id=bmst_connection.bmst_end_id AND
            source.level=(SELECT max(level) FROM bmst) AND
            destination.level=(SELECT max(level) FROM bmst) AND
            source.bmst_supernode!=destination.bmst_supernode
    )
INSERT INTO bmst_used_connection SELECT * from connection_mst;


WITH RECURSIVE
    connection_mst(src_supernode,dst_supernode) AS (
        SELECT DISTINCT
            source.bmst_supernode as src,
            destination.bmst_supernode as dst
        FROM
            bmst_used_connection,
            bmst AS source,
            bmst AS destination
        WHERE
            bmst_used_connection.bmst_start_id=source.bmst_id AND
            bmst_used_connection.bmst_end_id=destination.bmst_id
    ),
    supernodes(i) AS (
        SELECT DISTINCT
            bmst.bmst_supernode
        FROM
            bmst
        WHERE
            level=(SELECT max(level) FROM bmst)
    ),
    sprndecrt(nsn,src,dst) AS (
        SELECT
            sn.i,
            c.src_supernode,
            c.dst_supernode
        FROM
            supernodes as sn,
            connection_mst as c
        WHERE
            c.src_supernode = sn.i OR
            c.dst_supernode = sn.i
        UNION
        SELECT
            sprndecrt.nsn,
            c.src_supernode,
            c.dst_supernode
        FROM
            connection_mst as c,
            sprndecrt
        WHERE
            c.dst_supernode = sprndecrt.dst OR
            c.dst_supernode = sprndecrt.src OR
            c.src_supernode = sprndecrt.dst OR
            c.src_supernode = sprndecrt.src
    ),
    supernodes_info(nsn,src) AS (
        SELECT
            min(nsn),
            src
        FROM
            sprndecrt
        GROUP BY
            src
    ),
    to_insert(id,level,sn) AS (
        SELECT DISTINCT
            bmst.bmst_id,
            (select max(level)+1 from bmst) as level,
            supernodes_info.nsn
        FROM
            supernodes_info,
            bmst
        WHERE
            bmst.bmst_supernode=supernodes_info.src AND
            bmst.level=(select max(level) from bmst)
    ) INSERT INTO bmst SELECT * FROM to_insert;