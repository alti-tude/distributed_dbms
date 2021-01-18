from DDBMS.DBConstructs import Attribute, strFormat, numericFormatOfType

class Movie1:
    rel_name = "Movie1"

    class Attributes:
        MovieID = Attribute("MovieID", int, numericFormatOfType(int))
        Name = Attribute("Name", str, strFormat)
        Genre = Attribute("Genre", str, strFormat)
        IMDBRating = Attribute("IMDBRating", float, numericFormatOfType(float))


class Movie2:
    rel_name = "Movie2"

    class Attributes:
        MovieID = Attribute("MovieID", int, numericFormatOfType(int))
        Summary = Attribute("Summary", str, strFormat)
        MinAllowedAge = Attribute("MinAllowedAge", int, numericFormatOfType(int))
