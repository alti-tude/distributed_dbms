DROP PROCEDURE IF EXISTS getFragments;
DROP PROCEDURE IF EXISTS getSites;
DROP PROCEDURE IF EXISTS getHorizontalFragments;
DROP PROCEDURE IF EXISTS getVerticalFragments;


DELIMITER $$
CREATE PROCEDURE getFragments(IN relation_name VARCHAR(255))
BEGIN
    SELECT  *
    FROM    Fragment
    WHERE   RelationName = relation_name;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getSites(IN fragment_id VARCHAR(255))
BEGIN
    SELECT  *
    FROM    LocalMapping 
            NATURAL JOIN Site
    WHERE   FragmentID = fragment_id;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getHorizontalFragments(IN relation_name VARCHAR(255))
BEGIN
    SELECT  *
    FROM    Fragment 
            NATURAL JOIN HorizontalFragment
    WHERE   RelationName = relation_name;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getVerticalFragments(IN relation_name VARCHAR(255))
BEGIN
    SELECT  *
    FROM    Fragment 
            NATURAL JOIN VerticalFragment
            NATURAL JOIN Attribute
    WHERE   RelationName = relation_name;
END $$
DELIMITER ;