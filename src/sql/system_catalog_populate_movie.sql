DELETE FROM `LocalMapping`;
DELETE FROM `VerticalFragment`;
DELETE FROM `HorizontalFragment`;
DELETE FROM `DerivedHorizontalFragment`;
DELETE FROM `Site`;
DELETE FROM `Fragment`;
DELETE FROM `Attribute`;

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
VALUES  ('Hyderabad', 'localhost', 12345, 'user', 'iiit123'),
        ('Mumbai', 'localhost', 12346, 'user', 'iiit123'),
        ('Delhi', 'localhost', 12347, 'user', 'iiit123');

-- INSERT INTO Site
-- VALUES  ('Hyderabad', '10.3.5.215', 12345, 'user', 'iiit123'),
--         ('Mumbai', '10.3.5.214', 12345, 'user', 'iiit123'),
--         ('Delhi', '10.3.5.213', 12345, 'user', 'iiit123');

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