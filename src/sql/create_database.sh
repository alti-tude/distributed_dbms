cat system_catalog.sql system_catalog_procedures.sql system_catalog_populate_movie.sql | mysql -u Samosa -p Samosa

if [ "$1" = "Hyderabad" ]
then
    cat Hyderabad/movie_db_tables.sql Hyderabad/small_populate.sql | mysql -u Samosa -p Samosa
elif [ "$1" = "Mumbai" ]
then
    cat Mumbai/movie_db_tables.sql Mumbai/small_populate.sql | mysql -u Samosa -p Samosa
else
    cat Delhi/movie_db_tables.sql Delhi/small_populate.sql | mysql -u Samosa -p Samosa
fi