#!/usr/bin/env bash

if [ $1 = 'local' ]; then
    psql -d $2 -f sql/create_tables.sql
    exit;
elif [ $1 = 'heroku' ]; then
    heroku pg:psql < sql/create_tables.sql
    exit;
else
    echo 'usage:' 
    echo 'create_tables.sh local database_name'
    echo 'create_tables.sh heroku'
fi


