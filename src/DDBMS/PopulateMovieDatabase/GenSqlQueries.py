from DDBMS.LocalApplicationDB.Movie import Movie1, Movie2

class CONFIG:
    Movie1_file = "./Movie1.sql"
    Movie2_file = "./Movie2.sql"

def addMovie(name, genre, summary, IMDB_rating, min_allowed_age):
    query1  = f"INSERT INTO {Movie1.rel_name} ( {Movie1.Attributes.Name.name}, {Movie1.Attributes.Genre.name}, {Movie1.Attributes.IMDBRating.name} ) "\
            + f"VALUES ( {Movie1.Attributes.Name.format(name)}, {Movie1.Attributes.Genre.format(genre)}, {Movie1.Attributes.IMDBRating.format(IMDB_rating)} );"
    
    query2  = f"INSERT INTO {Movie2.rel_name} ( {Movie2.Attributes.Summary.name}, {Movie2.Attributes.MinAllowedAge.name} ) "\
            + f"VALUES ( {Movie2.Attributes.Summary.format(summary)}, {Movie2.Attributes.MinAllowedAge.format(min_allowed_age)} );"
    
    return query1, query2