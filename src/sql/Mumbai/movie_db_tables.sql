DROP TABLE IF EXISTS Theater;
DROP TABLE IF EXISTS Screen;
DROP TABLE IF EXISTS Screening;
DROP TABLE IF EXISTS Movie;

CREATE TABLE Theater (
    TheaterID INT NOT NULL,
    Location VARCHAR(255) NOT NULL,
    NumScreens INT,
    PRIMARY KEY (TheaterID)
);

CREATE TABLE Screen (
    ScreenID INT NOT NULL,
    TheaterID INT NOT NULL,
    ScreenName VARCHAR(255) NOT NULL,
    NumSeats INT,
    PRIMARY KEY (ScreenID)
);

CREATE TABLE Screening (
    ShowID INT NOT NULL,
    MovieID INT NOT NULL,
    ScreenID INT NOT NULL,
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