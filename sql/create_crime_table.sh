psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DROP TABLE IF EXISTS crime_data ;

    CREATE TABLE crime_data (
        case_number                 text not NULL,
        unique_key                  text not null primary key,
        date                        timestamp with time zone not NULL,
        block                       text not NULL,
        beat                        text not null,
        ward                        text not null,
        community_area              text not null,
        primary_type                text not NULL,
        description                 text not NULL,
        location_description        text not NULL,
        arrest                      bool not NULL,
        latitude                    float,
        longitude                   float
    );

   create index if not exists crime_data_primary_type_idx on crime_data(primary_type);
   create index if not exists crime_data_date_idx on crime_data(date);
EOSQL
