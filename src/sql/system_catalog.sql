CREATE TABLE Attribute (
    AttributeID INT NOT NULL AUTO_INCREMENT,
    RelationName VARCHAR(255) NOT NULL,
    AttributeName VARCHAR(255) NOT NULL,
    DataType VARCHAR(255) NOT NULL,
    isKey BOOL NOT NULL DEFAULT 0,
    PRIMARY KEY (AttributeID)
);

CREATE TABLE Fragment (
    FragmentID INT NOT NULL AUTO_INCREMENT,
    FragmentationType CHAR(1) NOT NULL,
    RelationName VARCHAR(255) NOT NULL,
    PRIMARY KEY (FragmentID)
);

CREATE TABLE VerticalFragment (
    FragmentID INT NOT NULL,
    AttributeID INT NOT NULL,
    FOREIGN KEY (FragmentID) REFERENCES Fragment(FragmentID),
    FOREIGN KEY (AttributeID) REFERENCES Attribute(AttributeID),
    PRIMARY KEY (FragmentID, AttributeID)
);

CREATE TABLE HorizontalFragment (
    FragmentID INT NOT NULL,
    AttributeID INT NOT NULL,
    Operator VARCHAR(30) NOT NULL,
    Value TEXT NOT NULL,
    FOREIGN KEY (FragmentID) REFERENCES Fragment(FragmentID),
    FOREIGN KEY (AttributeID) REFERENCES Attribute(AttributeID),
    PRIMARY KEY (FragmentID, AttributeID, Operator)
);

CREATE TABLE DerivedHorizontalFragment (
    FragmentID INT NOT NULL,
    LeftAttributeID INT NOT NULL,
    RightAttributeID INT NOT NULL,
    RightFragmentID INT NOT NULL,
    PRIMARY KEY (FragmentID, LeftAttributeID, RightAttributeID, RightFragmentID),
    FOREIGN KEY (FragmentID) REFERENCES Fragment(FragmentID),
    FOREIGN KEY (LeftAttributeID) REFERENCES Attribute(AttributeID),
    FOREIGN KEY (RightAttributeID) REFERENCES Attribute(AttributeID),
    FOREIGN KEY (RightFragmentID) REFERENCES Fragment(FragmentID)
);

CREATE TABLE Site (
    SiteID INT NOT NULL AUTO_INCREMENT,
    IP VARCHAR(255) NOT NULL,
    UserName VARCHAR(255),
    Password VARCHAR(255),
    PRIMARY KEY (SiteID)
);

CREATE TABLE LocalMapping (
    FragmentID INT NOT NULL,
    SiteID INT NOT NULL,
    DBName VARCHAR(255),
    DBUser VARCHAR(255),
    DBPass VARCHAR(255),
    LocalTableName VARCHAR(255),
    PRIMARY KEY (FragmentID, SiteID),
    FOREIGN KEY (FragmentID) REFERENCES Fragment(FragmentID),
    FOREIGN KEY (SiteID) REFERENCES Site(SiteID)
);
