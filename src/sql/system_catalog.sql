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

-- #TODO store port
CREATE TABLE Site (
    SiteID VARCHAR(255) NOT NULL,
    IP VARCHAR(255) NOT NULL,
    Port INT NOT NULL,
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

