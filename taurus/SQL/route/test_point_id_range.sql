select count(id)==(max(id)+1) from (select distinct id from point)
