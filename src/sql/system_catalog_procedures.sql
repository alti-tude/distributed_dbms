DROP PROCEDURE IF EXISTS getFragments;
DROP PROCEDURE IF EXISTS getSites;

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
            INNER JOIN Site ON Site.SiteID = LocalMapping.SiteID
    WHERE   FragmentID = fragment_id;
END $$
DELIMITER ;