import time
from psycopg2.extras import execute_values

def seed(cursor):
  seed_inventory(cursor)
  seed_customers(cursor)
  seed_employees(cursor)
  seed_orders(cursor)
  seed_order_items(cursor)
  seed_shifts(cursor)
  seed_employee_shifts(cursor)


def seed_inventory(cursor):
  execute_values(cursor,
    "INSERT INTO `Inventory` (`Name`, `Description`, `UnitCost`, `Quantity`) VALUES %s",
    [
        ('Organic Carrots', 'Price per Bundle of 4', 2.47, 9),
	    ('Red Potatoes', 'Price per 5lb bag', 5.86, 25),
		('Fresh Peaches', 'Price per peach', 0.79, 54)
    ]
  )

def seed_customers(cursor):
  execute_values(cursor,
    "INSERT INTO `Customers` (`Name`, `PhoneNumber`, `RewardsPts`) VALUES %s",
    [
        ('Toph', '123-456-7890', 100),
		('Katara', '987-654-3210', 300), 
		('Zuko', '999-888-7777', 250)
    ]
  )

def seed_employees(cursor):
  execute_values(cursor,
    "INSERT INTO `Employees` (`Name`, `HourlyWage`, `Responsibilities`, `SickDays`) VALUES %s",
    [
        ('Will', 15, 'Restock shelves', 4), 
		('Tessa', 15, 'Cashier', 6), 
		('Jem', 15, 'Customer service', 5)
    ]
  )

def seed_orders(cursor):
  execute_values(cursor,
    "INSERT INTO `Orders` (`CustomerID`, `EmployeeID`) VALUES %s",
    [
        (1, 1), 
        (2, 2), 
        (3, 3)
    ]
  )

def seed_order_items(cursor):
  execute_values(cursor,
    "INSERT INTO `OrderItems` (`Quantity`, `OrderID`, `PLU`) VALUES %s",
    [
        (4, 2, 2), 
        (6, 1, 1), 
        (1, 3, 2)
    ]
  )

def seed_shifts(cursor):
  execute_values(cursor,
    "INSERT INTO `Shifts` (`Day`, `StartTime`, `EndTime`) VALUES %s",
    [
        ('Monday', '08:00:00', '12:00:00'), 
		('Tuesday', '10:00:00', '14:00:00'), 
		('Wednesday', '14:00:00', '18:00:00')
    ]
  )

def seed_employee_shifts(cursor):
  execute_values(cursor,
    "INSERT INTO `EmployeeShifts` (`EmployeeID`, `ShiftID`) VALUES %s",
    [
        (1, 1), 
        (2, 2), 
        (3, 3)
    ]
  )
