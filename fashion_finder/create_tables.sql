-- Create brand table
CREATE TABLE IF NOT EXISTS brand (
    BrandID INT NOT NULL PRIMARY KEY,
    BrandName VARCHAR(100) NOT NULL
);
-- Create category table
CREATE TABLE IF NOT EXISTS category (
    CategoryID INT NOT NULL PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL
);
-- Create size table
CREATE TABLE IF NOT EXISTS size (
    SizeID INT NOT NULL PRIMARY KEY,
    SizeName VARCHAR(10) NOT NULL
);
-- Create colour table
CREATE TABLE IF NOT EXISTS colour (
    ColourID INT NOT NULL PRIMARY KEY,
    ColourName VARCHAR(30) NOT NULL
);
-- Create clothing item table
CREATE TABLE IF NOT EXISTS clothing_item (
    ItemID INT NOT NULL PRIMARY KEY,
    ItemName VARCHAR(150) NOT NULL,
    Description VARCHAR(255),
    SizeID INT NOT NULL REFERENCES size(SizeID),
    ColourID INT NOT NULL REFERENCES colour(ColourID),
    Price DECIMAL(10, 2) NOT NULL,
    ImageURL VARCHAR(255),
    BrandID INT NOT NULL REFERENCES brand(BrandID),
    CategoryID INT NOT NULL REFERENCES category(CategoryID)
);