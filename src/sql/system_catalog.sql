DROP TABLE IF EXISTS LocalMapping;
DROP TABLE IF EXISTS VerticalFragment;
DROP TABLE IF EXISTS HorizontalFragment;
DROP TABLE IF EXISTS DerivedHorizontalFragment;
DROP TABLE IF EXISTS Site;
DROP TABLE IF EXISTS Fragment;
DROP TABLE IF EXISTS Attribute;

CREATE TABLE Attribute (
    AttributeID INT NOT NULL AUTO_INCREMENT,
    RelationName VARCHAR(255) NOT NULL,
    AttributeName VARCHAR(255) NOT NULL,
    DataType VARCHAR(255) NOT NULL,
    isKey BOOL NOT NULL DEFAULT 0,
    PRIMARY KEY (AttributeID)
);

CREATE TABLE Fragment (
    FragmentID VARCHAR(255) NOT NULL,
    FragmentationType CHAR(1) NOT NULL,
    RelationName VARCHAR(255) NOT NULL,
    PRIMARY KEY (FragmentID)
);

CREATE TABLE VerticalFragment (
    FragmentID VARCHAR(255) NOT NULL,
    AttributeID INT NOT NULL,
    FOREIGN KEY (FragmentID) REFERENCES Fragment(FragmentID),
    FOREIGN KEY (AttributeID) REFERENCES Attribute(AttributeID),
    PRIMARY KEY (FragmentID, AttributeID)
);

CREATE TABLE HorizontalFragment (
    FragmentID VARCHAR(255) NOT NULL,
    Predicate MEDIUMTEXT,
    FOREIGN KEY (FragmentID) REFERENCES Fragment(FragmentID)
);

CREATE TABLE DerivedHorizontalFragment (
    FragmentID VARCHAR(255) NOT NULL,
    LeftAttributeID INT NOT NULL,
    RightAttributeID INT NOT NULL,
    RightFragmentID VARCHAR(255) NOT NULL,
    PRIMARY KEY (FragmentID, LeftAttributeID, RightAttributeID, RightFragmentID),
    FOREIGN KEY (FragmentID) REFERENCES Fragment(FragmentID),
    FOREIGN KEY (LeftAttributeID) REFERENCES Attribute(AttributeID),
    FOREIGN KEY (RightAttributeID) REFERENCES Attribute(AttributeID),
    FOREIGN KEY (RightFragmentID) REFERENCES Fragment(FragmentID)
);

CREATE TABLE Site (
    SiteID VARCHAR(255) NOT NULL,
    IP VARCHAR(255) NOT NULL,
    UserName VARCHAR(255),
    Password VARCHAR(255),
    PRIMARY KEY (SiteID)
);

CREATE TABLE LocalMapping (
    FragmentID VARCHAR(255) NOT NULL,
    SiteID VARCHAR(255) NOT NULL,
    DBName VARCHAR(255),
    DBUser VARCHAR(255),
    DBPass VARCHAR(255),
    LocalTableName VARCHAR(255),
    PRIMARY KEY (FragmentID, SiteID),
    FOREIGN KEY (FragmentID) REFERENCES Fragment(FragmentID),
    FOREIGN KEY (SiteID) REFERENCES Site(SiteID)
);

/*------------ populate catalogue */

INSERT INTO Attribute (RelationName, AttributeName, DataType, isKey) 
VALUES  ('Movie', 'MovieID', 'INT', 1),
        ('Movie', 'Name', 'VARCHAR(255)', 0),
        ('Movie', 'Genre', 'VARCHAR(255)', 0),
        ('Movie', 'Summary', 'MEDIUMTEXT', 0),
        ('Movie', 'IMDBRating', 'FLOAT(2,1)', 0),
        ('Movie', 'MinAllowedAge', 'INT', 0),

        ('Theater', 'TheaterID', 'INT', 1),
        ('Theater', 'Location', 'VARCHAR(255)', 0),
        ('Theater', 'NumScreens', 'INT', 0),

        ('Screen', 'ScreenID', 'INT', 1),
        ('Screen', 'TheaterID', 'INT', 0),
        ('Screen', 'ScreenName', 'VARCHAR(255)', 0),
        ('Screen', 'NumSeats', 'INT', 0),

        ('Show', 'ShowID', 'INT', 1),
        ('Show', 'MovieID', 'INT', 0),
        ('Show', 'ScreenID', 'INT', 0),
        ('Show', 'Time', 'DATETIME', 0),
        ('Show', 'Price', 'FLOAT(7,2)', 0),

        ('User', 'EMail', 'VARCHAR(255)', 1),
        ('User', 'Name', 'VARCHAR(255)', 0),
        ('User', 'PhNo', 'VARCHAR(15)', 0),
        ('User', 'DOB', 'DATE', 0),

        ('Reservation', 'ReservationID', 'INT', 1),
        ('Reservation', 'ShowID', 'INT', 0),
        ('Reservation', 'UserEMail', 'VARCHAR(255)', 0),
        ('Reservation', 'SeatNo', 'INT', 0);


INSERT INTO Fragment 
VALUES  ('Theater_D', 'H', 'Theater'),
        ('Theater_H', 'H', 'Theater'),
        ('Theater_M', 'H', 'Theater'),

        ('Screen_D', 'D', 'Screen'),
        ('Screen_H', 'D', 'Screen'),
        ('Screen_M', 'D', 'Screen'),

        ('Show_D', 'D', 'Show'),
        ('Show_H', 'D', 'Show'),
        ('Show_M', 'D', 'Show'),

        ('Movie_1', 'V', 'Movie'),
        ('Movie_2', 'V', 'Movie'),

        ('Reservation', 'N', 'Reservation'),
        ('User', 'N', 'User');

/*------------------------------------VERTICAL FRAGMENTATION*/

INSERT INTO VerticalFragment
SELECT 'Movie_1', AttributeID
FROM    Attribute
WHERE   RelationName = 'Movie' AND 
        (
            AttributeName = 'MovieID' OR
            AttributeName = 'Name' OR
            AttributeName = 'Genre' OR
            AttributeName = 'IMDBRating'
        );

INSERT INTO VerticalFragment
SELECT 'Movie_2', AttributeID
FROM    Attribute
WHERE   RelationName = 'Movie' AND 
        (
            AttributeName = 'MovieID' OR
            AttributeName = 'Summary' OR
            AttributeName = 'MinAllowedAge'
        );

/*------------------------------------HORIZONTAL FRAGMENTATION*/
INSERT INTO HorizontalFragment
VALUES ('Theater_D', 'Location = "Delhi"');

INSERT INTO HorizontalFragment
VALUES ('Theater_M', 'Location = "Mumbai"');

INSERT INTO HorizontalFragment
VALUES ('Theater_H', 'Location = "Hyderabad"');

/*------------------------------------DERIVED HORIZONTAL FRAGMENTATION*/
SET @ScreenTheaterID  = 0;
SET @TheaterTheaterID = 0;

SELECT  AttributeID INTO @ScreenTheaterID
FROM    Attribute
WHERE   RelationName = 'Screen' AND AttributeName = 'TheaterID';

SELECT  AttributeID INTO @TheaterTheaterID
FROM    Attribute
WHERE   RelationName = 'Theater' AND AttributeName = 'TheaterID';

SELECT @ScreenTheaterID, @TheaterTheaterID;

INSERT INTO DerivedHorizontalFragment
SELECT 'Screen_D', @ScreenTheaterID, @TheaterTheaterID, 'Theater_D';

INSERT INTO DerivedHorizontalFragment
SELECT 'Screen_H', @ScreenTheaterID, @TheaterTheaterID, 'Theater_H';

INSERT INTO DerivedHorizontalFragment
SELECT 'Screen_M', @ScreenTheaterID, @TheaterTheaterID, 'Theater_M';


SET @ShowScreenID  = 0;
SET @ScreenScreenID = 0;

SELECT  AttributeID INTO @ShowScreenID
FROM    Attribute
WHERE   RelationName = 'Show' AND AttributeName = 'ScreenID';

SELECT  AttributeID INTO @ScreenScreenID
FROM    Attribute
WHERE   RelationName = 'Screen' AND AttributeName = 'ScreenID';

SELECT @ShowScreenID, @ScreenScreenID;

INSERT INTO DerivedHorizontalFragment
SELECT 'Show_D', @ShowScreenID, @ScreenScreenID, 'Screen_D';

INSERT INTO DerivedHorizontalFragment
SELECT 'Show_H', @ShowScreenID, @ScreenScreenID, 'Screen_H';

INSERT INTO DerivedHorizontalFragment
SELECT 'Show_M', @ShowScreenID, @ScreenScreenID, 'Screen_M';

/*----------------------------------------------------SITE*/

INSERT INTO Site
VALUES  ('Hyderabad', '10.3.5.215', 'user', 'iiit123'),
        ('Mumbai', '10.3.5.214', 'user', 'iiit123'),
        ('Delhi', '10.3.5.213', 'user', 'iiit123');

/*-----------------------------------------------------LOCAL MAPPING*/

INSERT INTO LocalMapping
VALUES  ('Theater_D', 'Delhi', 'Samosa', 'Samose', 'Samosa', 'Theater'),
        ('Theater_H', 'Hyderabad', 'Samosa', 'Samose', 'Samosa', 'Theater'),
        ('Theater_M', 'Mumbai', 'Samosa', 'Samose', 'Samosa', 'Theater'),

        ('Screen_D', 'Delhi', 'Samosa', 'Samose', 'Samosa', 'Screen'),
        ('Screen_H', 'Hyderabad', 'Samosa', 'Samose', 'Samosa', 'Screen'),
        ('Screen_M', 'Mumbai', 'Samosa', 'Samose', 'Samosa', 'Screen'),

        ('Show_D', 'Delhi', 'Samosa', 'Samose', 'Samosa', 'Screening'),
        ('Show_H', 'Hyderabad', 'Samosa', 'Samose', 'Samosa', 'Screening'),
        ('Show_M', 'Mumbai', 'Samosa', 'Samose', 'Samosa', 'Screening'),

        ('Movie_1', 'Hyderabad', 'Samosa', 'Samose', 'Samosa', 'Movie'),
        ('Movie_2', 'Mumbai', 'Samosa', 'Samose', 'Samosa', 'Movie'),
        ('Reservation', 'Hyderabad', 'Samosa', 'Samose', 'Samosa', 'Reservation'),
        ('User', 'Delhi', 'Samosa', 'Samose', 'Samosa', 'User');