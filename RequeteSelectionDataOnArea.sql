select * from velovdata where station_name = 11 and  ( extract(HOUR FROM last_update_fme) = 20 or extract(HOUR FROM last_update_fme) = 21 )
