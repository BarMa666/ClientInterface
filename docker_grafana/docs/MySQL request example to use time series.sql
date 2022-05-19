SELECT 
  UNIX_TIMESTAMP(CONVERT_TZ(date,'+00:00','-7:00')) as time,
  field_value as value
FROM data_main 
WHERE (UNIX_TIMESTAMP(CONVERT_TZ(date,'+00:00','-7:00')) BETWEEN ${__from:date:seconds} AND ${__to:date:seconds}) AND data_main.field_id = 1 
ORDER BY date ASC;