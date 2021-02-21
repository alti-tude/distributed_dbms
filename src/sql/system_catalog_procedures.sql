DROP PROCEDURE IF EXISTS getFragments;
DROP PROCEDURE IF EXISTS getSites;
DROP PROCEDURE IF EXISTS getHorizontalFragments;
DROP PROCEDURE IF EXISTS getVerticalFragments;
DROP PROCEDURE IF EXISTS getDerivedHorizontalFragments;


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

DELIMITER $$
CREATE PROCEDURE getDerivedHorizontalFragments(IN relation_name VARCHAR(255))
BEGIN
    SELECT  FragmentID as LeftFragmentID, Fragment.RelationName as LeftRelationName, 
            LeftAttribute.AttributeName as LeftAttributeName, RightFragmentID, 
            RightAttribute.RelationName as RightRelationName,
            RightAttribute.AttributeName as RightAttributeName
    FROM    Fragment
            NATURAL JOIN DerivedHorizontalFragment
            JOIN Attribute as LeftAttribute 
            JOIN Attribute as RightAttribute
    WHERE   Fragment.RelationName = relation_name
            AND LeftAttributeID = LeftAttribute.AttributeID
            AND RightAttributeID = RightAttribute.AttributeID;
END $$
DELIMITER ;
