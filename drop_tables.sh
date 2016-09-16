#!/usr/bin/env bash

if [ $1 = 'local' ]; then
    psql -d $2 -f sql/drop_tables.sql   
    exit;
elif [ $1 = 'heroku' ]; then
    heroku pg:psql < sql/drop_tables.sql
    exit;
else
    echo 'usage:' 
    echo 'drop_tables.sh local database_name'
    echo 'drop_tables.sh heroku'
fi


