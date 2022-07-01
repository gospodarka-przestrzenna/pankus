with recursive 
path_(start_id,end_id,segment_id,segment_start,segment_end) as 
(
SELECT 
	start_id,end_id,0,predecessor_id,end_id 
FROM 
	distance 
WHERE 
	start_id!=end_id AND
	predecessor_id is not NULL AND 
	start_id=:start
UNION
SELECT 
	path_.start_id,path_.end_id,path_.segment_id+1,distance.predecessor_id,distance.end_id 
FROM 
	path_,distance 
WHERE
	path_.start_id=distance.start_id AND  
	path_.segment_start=distance.end_id AND 
	distance.end_id!=distance.start_id
)
insert into path select * from path_;