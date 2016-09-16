#!/usr/bin/env bash

if [ $1 = 'local' ]; then
    psql -d $2 -f sql/add_test_data.sql
    exit;
elif [ $1 = 'heroku' ]; then
    heroku pg:psql < sql/add_test_data.sql
    exit;
else
    echo 'usage:'
    echo 'add_test_data.sh local database_name'
    echo 'add_test_data.sh heroku'
fi
