DROP TABLE IF EXISTS Theater;
DROP TABLE IF EXISTS Showing;
DROP TABLE IF EXISTS Movie;

CREATE TABLE Theater (
    TheaterID INT NOT NULL,
    Location VARCHAR(255) NOT NULL,
    NumScreens INT,
    PRIMARY KEY (TheaterID)
);

CREATE TABLE Showing (
    ShowID INT NOT NULL,
    MovieID INT NOT NULL,
    TheaterID INT NOT NULL,
    Time DATETIME NOT NULL,
    Price FLOAT(7,2) NOT NULL,
    PRIMARY KEY (ShowID)
);

CREATE TABLE Movie (
    MovieID INT NOT NULL AUTO_INCREMENT,
    Summary MEDIUMTEXT,
    MinAllowedAge INT,
    PRIMARY KEY (MovieID)
);
