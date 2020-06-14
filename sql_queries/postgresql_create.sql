/**************************************/
-- INVENTORY
/**************************************/
CREATE TABLE Inventory (
	PLU 			serial,
	Name 			varchar(255) NOT NULL,
	Description 	varchar(255) NOT NULL,
	UnitCost 		decimal(8,2) NOT NULL,
	Quantity 		integer,
	PRIMARY KEY (PLU)
);

INSERT INTO Inventory (Name, Description, UnitCost, Quantity) 
VALUES  ('Organic Carrots', 'Price per Bundle of 4', 2.47, 9),
		('Red Potatoes', 'Price per 5lb bag', 5.86, 25),
		('Fresh Peaches', 'Price per peach', 0.79, 54);


/**************************************/
-- CUSTOMERS
/**************************************/
CREATE TABLE Customers (
	CustomerID 		serial,
	Name 			varchar(255), 
	PhoneNumber 	varchar(255),
	RewardsPts 		integer,
	PRIMARY KEY (CustomerID)
);

INSERT INTO Customers (Name, PhoneNumber, RewardsPts) 
VALUES  ('Toph', '123-456-7890', 100),
		('Katara', '987-654-3210', 300), 
		('Zuko', '999-888-7777', 250);


/**************************************/
-- EMPLOYEES
/**************************************/
CREATE TABLE Employees (
	EmployeeID 			serial,
	Name 				varchar(255), 
	HourlyWage 			decimal(6,2),
	Responsibilities 	varchar(255),
	SickDays 			integer,
	PRIMARY KEY (EmployeeID)
);

INSERT INTO Employees (Name, HourlyWage, Responsibilities, SickDays) 
VALUES  ('Will', 15, 'Restock shelves', 4), 
		('Tessa', 15, 'Cashier', 6), 
		('Jem', 15, 'Customer service', 5);


/**************************************/
-- ORDERS
/**************************************/
CREATE TABLE Orders (
	OrderID 		serial,
	CustomerID 		integer,
	EmployeeID 		integer,
	PRIMARY KEY (OrderID),
	CONSTRAINT fk_cid
	FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
	ON DELETE SET NULL,
	CONSTRAINT fk_eid
	FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
	ON DELETE SET NULL
);

INSERT INTO Orders (CustomerID, EmployeeID)
VALUES (1, 1), (2, 2), (3, 3);


/**************************************/
-- OrderItems
/**************************************/
CREATE TABLE OrderItems (
	OrderItemID 	serial,
	Quantity 		integer NOT NULL,
	OrderID 		integer,
	PLU 			integer,
	PRIMARY KEY (OrderItemID),
	CONSTRAINT fk_oid
	FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
	ON DELETE SET NULL,
	CONSTRAINT fk_plu
	FOREIGN KEY (PLU) REFERENCES Inventory(PLU)
	ON DELETE SET NULL
);

INSERT INTO OrderItems (Quantity, OrderID, PLU)
VALUES (4, 2, 2), (6, 1, 1), (1, 3, 2);


/**************************************/
-- SHIFTS
/**************************************/
CREATE TABLE Shifts (
	ShiftID 	serial,
	Day 		varchar(255), 
	StartTime 	time(0),
	EndTime 	time(0),
	PRIMARY KEY (ShiftID)
);

INSERT INTO Shifts (Day, StartTime, EndTime) 
VALUES  ('Monday', '08:00:00', '12:00:00'), 
		('Tuesday', '10:00:00', '14:00:00'), 
		('Wednesday', '14:00:00', '18:00:00');


/**************************************/
-- EmployeeShifts
/**************************************/
CREATE TABLE EmployeeShifts (
	EmployeeShiftID 	serial,
	EmployeeID 			integer,
	ShiftID 			integer,
	PRIMARY KEY (EmployeeShiftID),
	CONSTRAINT fk_es_eid
	FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
	ON DELETE SET NULL,
	CONSTRAINT fk_es_sid
	FOREIGN KEY (ShiftID) REFERENCES Shifts(ShiftID)
	ON DELETE SET NULL
);

INSERT INTO EmployeeShifts (EmployeeID, ShiftID) 
VALUES (1, 1), (2, 2), (3, 3);
