--DROP TABLE Volunteers;
--DROP TABLE VolunteerRewards;
--DROP TABLE RedeemedRewards;
--DROP TABLE PossibleRewards;


CREATE TABLE IF NOT EXISTS Volunteers (
    id INTEGER PRIMARY KEY,
	isStudent BOOLEAN,
	rewardTier INTEGER,
    name VARCHAR(50),
    num_hours INTEGER
);

CREATE TABLE IF NOT EXISTS PossibleRewards (
	rewardName VARCHAR(50) PRIMARY KEY,
	hourThreshold INTEGER
);


CREATE TABLE IF NOT EXISTS VolunteerRewards (
	volunteerID INTEGER,
	rewardName VARCHAR(50),
	
	FOREIGN KEY (volunteerID) REFERENCES Volunteers (id),
	FOREIGN KEY (rewardName) REFERENCES PossibleRewards (rewardName)
);


CREATE TABLE IF NOT EXISTS RedeemedRewards (
	volunteerID INTEGER,
	rewardName VARCHAR(50),
	dateRedeemed DATE,
	
	FOREIGN KEY (volunteerID) REFERENCES Volunteers (id),
	FOREIGN KEY (rewardName) REFERENCES PossibleRewards (rewardName)
);


-- Inserting values for PossibleRewards table
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("Free Can of Nestea", 2);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("Free Booking Slot", 2);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("Patch Kit", 10);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("Bike Coop Bottle", 20);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("Tire Levers", 30);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("Bike Coop Shirt", 40);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("ParkTool Multitool", 50);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("ParkTool Apron", 60);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("Bike Lube", 70);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("50$ MSRP Credit", 80);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("10% off MSRP Catalogue", 90);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("20% off MSRP Catalogue", 100);
--INSERT INTO PossibleRewards (rewardName, hourThreshold) VALUES ("???", 120);