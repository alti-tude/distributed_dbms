DROP PROCEDURE IF EXISTS getFragments;
DROP PROCEDURE IF EXISTS getSites;
DROP PROCEDURE IF EXISTS getHorizontalFragments;
DROP PROCEDURE IF EXISTS getVerticalFragments;
DROP PROCEDURE IF EXISTS getDerivedHorizontalFragments;
DROP PROCEDURE IF EXISTS insertDerivedHorizontalFragment;


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


DELIMITER $$
CREATE PROCEDURE insertDerivedHorizontalFragment(IN LeftRelation VARCHAR(255), IN LeftAttribute VARCHAR(255), IN LeftFrag VARCHAR(255), IN RightRelation VARCHAR(255), IN RightAttribute VARCHAR(255), IN RightFrag VARCHAR(255))
BEGIN
	SET @LeftID  = 0;
	SET @RightID = 0;

	SELECT  AttributeID INTO @LeftID
	FROM    Attribute
	WHERE   RelationName = LeftRelation AND AttributeName = LeftAttribute;

	SELECT  AttributeID INTO @RightID
	FROM    Attribute
	WHERE   RelationName = RightRelation AND AttributeName = RightAttribute;

	INSERT INTO DerivedHorizontalFragment
	SELECT LeftFrag, @LeftID, @RightID, RightFrag;

END $$
DELIMITER ;