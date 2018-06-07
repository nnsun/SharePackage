DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS packages;
DROP TABLE IF EXISTS p2u;

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
