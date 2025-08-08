CREATE TABLE Organisms (
	alias TEXT,
	dans_bigscape BOOLEAN,
	Full_Name TEXT NOT NULL,
	Genus TEXT NOT NULL,
	Espece TEXT NOT NULL,
	Genre_espece TEXT,
	taxo_id INTEGER,
	Taxo_Clade TEXT
);


CREATE TABLE Taxonomy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	Taxo_Fam TEXT,
	Taxo_Order TEXT,
	Taxo_Class TEXT,
	Taxo_Phylum TEXT
);
