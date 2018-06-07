DROP TABLE IF EXISTS Packages;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS PeersMap;

CREATE TABLE Packages (
	pName TEXT UNIQUE NOT NULL,
	pDesc TEXT,
	pVersion TEXT,
	pAuthor TEXT,
	pDependences TEXT,
	pFiles TEXT NOT NULL
);

CREATE TABLE Users (
	IP TEXT UNIQUE NOT NULL
);

CREATE TABLE PeersMap (
	pName TEXT NOT NULL,
	IP TEXT NOT NULL,
	UNIQUE(pName,IP)
);
