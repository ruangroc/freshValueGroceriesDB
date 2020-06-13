from psycopg2 import connect, extensions
from urllib.parse import urlparse
import time
from seed_database import seed


def createdatabase(database_url):
    result = urlparse(database_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    print('Database name: ', database, ' | Username: ', username)
    print('Password: ', password, ' | host: ', host, ' | port: ', port)
    conn = connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )

    # get the isolation level for autocommit
    # set the isolation level for the connection's cursors
    # will raise ActiveSqlTransaction exception otherwise
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)

    # instantiate a cursor object from the connection
    cursor = conn.cursor()

    # Create Inventory table
    cursor.execute("DROP TABLE IF EXISTS `Inventory`;")
    cursor = conn.cursor()
    sql = '''CREATE TABLE `Inventory` (
                `PLU` int(11) NOT NULL AUTO_INCREMENT,
                `Name` varchar(255) NOT NULL,
                `Description` varchar(255) NOT NULL,
                `UnitCost` decimal(8,2) NOT NULL,
                `Quantity` int(11),
                PRIMARY KEY (`PLU`)
            );'''
    cursor.execute(sql)
    conn.commit()


    # Create Customers table
    cursor.execute("DROP TABLE IF EXISTS `Customers`;")
    cursor = conn.cursor()
    sql = '''CREATE TABLE `Customers` (
                `CustomerID` int(11) NOT NULL AUTO_INCREMENT,
                `Name` varchar(255), 
                `PhoneNumber` varchar(255),
                `RewardsPts` int(11),
                PRIMARY KEY (`CustomerID`)
            );'''
    cursor.execute(sql)
    conn.commit()


    # Create Employees table
    cursor.execute("DROP TABLE IF EXISTS `Employees`;")
    cursor = conn.cursor()
    sql = '''CREATE TABLE `Employees` (
                `EmployeeID` int(11) NOT NULL AUTO_INCREMENT,
                `Name` varchar(255), 
                `HourlyWage` decimal(6,2),
                `Responsibilities` varchar(255),
                `SickDays` int(11),
                PRIMARY KEY (`EmployeeID`)
            );'''
    cursor.execute(sql)
    conn.commit()


    # Create Orders table
    cursor.execute("DROP TABLE IF EXISTS `Orders`;")
    cursor = conn.cursor()
    sql = '''CREATE TABLE `Orders` (
                `OrderID` int(11) NOT NULL AUTO_INCREMENT,
                `CustomerID` int(11),
                `EmployeeID` int(11),
                PRIMARY KEY (`OrderID`),
                CONSTRAINT `fk_cid`
                FOREIGN KEY (`CustomerID`) REFERENCES Customers(`CustomerID`)
                ON DELETE SET NULL,
                CONSTRAINT `fk_eid`
                FOREIGN KEY (`EmployeeID`) REFERENCES Employees(`EmployeeID`)
                ON DELETE SET NULL
            );'''
    cursor.execute(sql)
    conn.commit()


    # Create OrderItems table
    cursor.execute('DROP TABLE IF EXISTS `OrderItems`;')
    cursor = conn.cursor()
    sql = '''CREATE TABLE `OrderItems` (
                `OrderItemID` int(11) NOT NULL AUTO_INCREMENT,
                `Quantity` int(11) NOT NULL,
                `OrderID` int(11),
                `PLU` int(11),
                PRIMARY KEY (`OrderItemID`),
                CONSTRAINT `fk_oid`
                FOREIGN KEY (`OrderID`) REFERENCES Orders(`OrderID`)
                ON DELETE SET NULL,
                CONSTRAINT `fk_plu`
                FOREIGN KEY (`PLU`) REFERENCES Inventory(`PLU`)
                ON DELETE SET NULL
            );'''
    cursor.execute(sql)
    conn.commit()


    # Create Shifts table
    cursor.execute('DROP TABLE IF EXISTS `Shifts`;')
    cursor = conn.cursor()
    sql = '''CREATE TABLE `Shifts` (
                `ShiftID` int(11) NOT NULL AUTO_INCREMENT,
                `Day` varchar(255), 
                `StartTime` time(0),
                `EndTime` time(0),
                PRIMARY KEY (`ShiftID`)
            );'''
    cursor.execute(sql)
    conn.commit()


    # Create EmployeeShifts table
    cursor.execute('DROP TABLE IF EXISTS `EmployeeShifts`;')
    cursor = conn.cursor()
    sql = '''CREATE TABLE `EmployeeShifts` (
                `EmployeeShiftID` int(11) NOT NULL AUTO_INCREMENT,
                `EmployeeID` int(11),
                `ShiftID` int(11),
                PRIMARY KEY (`EmployeeShiftID`),
                CONSTRAINT `fk_es_eid`
                FOREIGN KEY (`EmployeeID`) REFERENCES Employees(`EmployeeID`)
                ON DELETE SET NULL,
                CONSTRAINT `fk_es_sid`
                FOREIGN KEY (`ShiftID`) REFERENCES Shifts(`ShiftID`)
                ON DELETE SET NULL
            );'''
    cursor.execute(sql)
    conn.commit()


    # seed database
    seed(cursor)
    conn.commit()

    # close the cursor to avoid memory leaks
    cursor.close()

    # close the connection to avoid memory leaks
    conn.close()