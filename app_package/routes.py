from flask import json, jsonify, request, render_template, make_response
from psycopg2 import sql, extras

from app_package.db import db_pool
from app_package import app

# Will need to change the db connection process and stuff to work with postgres

################################################
# Index
################################################
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

################################################
# Customers
################################################
@app.route('/customers')
def customers_page():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    query = """SELECT CustomerID, Name, PhoneNumber, RewardsPts 
            FROM Customers ORDER BY CustomerID ASC;"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return render_template('customers.html', rows=result)

@app.route('/new-customer', methods=['POST'])
def insert_new_customer():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    query =  """INSERT INTO Customers 
                (Name, PhoneNumber, RewardsPts) 
                VALUES (%s, %s, %s);"""
    data = (info["name"], info["phone"], info["points"])

    cursor.execute(query, data)
    db_conn.commit()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Customer added!', 200)

@app.route('/search-customers-name', methods=['POST'])
def search_customers_by_name():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    search_term = request.get_json(force=True)["input"]
    query =  """SELECT CustomerID, Name, PhoneNumber, RewardsPts 
                    FROM Customers WHERE Name = %s;"""
    data = (search_term,)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/search-customers-phone', methods=['POST'])
def search_customers_by_phone_number():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    search_term = request.get_json(force=True)["input"]
    query =  """SELECT CustomerID, Name, PhoneNumber, RewardsPts 
                    FROM Customers WHERE PhoneNumber = %s;"""
    data = (search_term,)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/search-customers-pts', methods=['POST'])
def search_customers_by_points():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    search_terms = request.get_json(force=True)
    query =  """SELECT CustomerID, Name, PhoneNumber, RewardsPts 
                FROM Customers WHERE RewardsPts >= %s AND RewardsPts <= %s;"""
    data = (search_terms["lower"], search_terms["upper"])

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/delete-customer', methods=['POST'])
def delete_customer():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    customer_id = request.get_json(force=True)["customer_id"]
    query =  """DELETE FROM Customers WHERE CustomerID = %s;"""
    data = (customer_id,)

    cursor.execute(query, data)
    db_conn.commit()

    cursor.close()
    db_pool.putconn(db_conn)
    message = 'Customer with ID ' + customer_id + ' removed from the database'
    return make_response(message, 200)

@app.route('/update-customer', methods=['POST'])
def update_customer():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    data = (info["name"], info["phone"], info["points"], info["id"])
    query = """UPDATE Customers 
            SET Name = %s,
                PhoneNumber = %s,
                RewardsPts = %s
            WHERE CustomerID = %s;"""

    cursor.execute(query, data)
    db_conn.commit()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Updated customer information', 200)

################################################
# Manage Orders
################################################

@app.route('/orders')
def orders_page():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    query =  """SELECT Orders.OrderID, Inventory.Name, Inventory.Description, Inventory.UnitCost, 
                OrderItems.Quantity, (Inventory.UnitCost * OrderItems.Quantity), 
                OrderItems.OrderItemID AS Total FROM Inventory
                JOIN OrderItems on OrderItems.PLU = Inventory.PLU
                JOIN Orders on OrderItems.OrderID = Orders.OrderID
                ORDER BY Orders.OrderID ASC;"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return render_template('orders.html', results=result)

@app.route('/search-orders-cust-id', methods=['POST'])
def search_orders_by_cust_id():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    search_term = request.get_json(force=True)["id"]
    query =  """SELECT Orders.OrderID, Inventory.Name, Inventory.Description, Inventory.UnitCost, 
                OrderItems.Quantity, (Inventory.UnitCost * OrderItems.Quantity) AS Total
                FROM Inventory
                JOIN OrderItems on OrderItems.PLU = Inventory.PLU
                JOIN Orders on OrderItems.OrderID = Orders.OrderID
                JOIN Customers on Orders.CustomerID = Customers.CustomerID
                AND Customers.CustomerID = %s
                ORDER BY Orders.OrderID ASC;"""
    data = (search_term,)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/search-orders-name', methods=['POST'])
def search_orders_by_name():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    search_term = request.get_json(force=True)["name"]
    query = """SELECT Orders.OrderID, Inventory.Name, Inventory.Description, Inventory.UnitCost, 
                OrderItems.Quantity, (Inventory.UnitCost * OrderItems.Quantity) AS Total
                FROM Inventory
                JOIN OrderItems on OrderItems.PLU = Inventory.PLU
                JOIN Orders on OrderItems.OrderID = Orders.OrderID
                JOIN Customers on Orders.CustomerID = Customers.CustomerID
                AND Customers.Name = %s
                ORDER BY Orders.OrderID ASC;"""
    data = (search_term,)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/search-orders-phone', methods=['POST'])
def search_orders_by_phone():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    search_term = request.get_json(force=True)["phone"]
    query = """SELECT Orders.OrderID, Inventory.Name, Inventory.Description, Inventory.UnitCost, 
                OrderItems.Quantity, (Inventory.UnitCost * OrderItems.Quantity) AS Total
                FROM Inventory
                JOIN OrderItems on OrderItems.PLU = Inventory.PLU
                JOIN Orders on OrderItems.OrderID = Orders.OrderID
                JOIN Customers on Orders.CustomerID = Customers.CustomerID
                AND Customers.PhoneNumber = %s
                ORDER BY Orders.OrderID ASC;"""
    data = (search_term,)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/search-orders-employee', methods=['POST'])
def search_orders_by_employee():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    search_term = request.get_json(force=True)["employee"]
    query = """SELECT Orders.OrderID, Inventory.Name, Inventory.Description, Inventory.UnitCost, 
                OrderItems.Quantity, (Inventory.UnitCost * OrderItems.Quantity) AS Total
                FROM Inventory
                JOIN OrderItems on OrderItems.PLU = Inventory.PLU
                JOIN Orders on OrderItems.OrderID = Orders.OrderID
                JOIN Employees on Orders.EmployeeID = Employees.EmployeeID
                AND Employees.Name = %s
                ORDER BY Orders.OrderID ASC;"""
    data = (search_term,)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/update-orders', methods=['POST'])
def update_orders():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    OrderItemID = request.get_json(force=True)['id']
    quantity = int(request.get_json(force=True)['quantity'])
    data = (quantity, OrderItemID)
    # Update Quantity of items ordered
    query = """UPDATE OrderItems
            SET Quantity = %s
            WHERE OrderItemID = %s;"""

    cursor.execute(query, data)
    db_conn.commit()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Inventory added!', 200)

@app.route('/delete-order-item', methods=['POST'])
def delete_order_item():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    OrderItemID = request.get_json(force=True)["info"]
    query = """DELETE FROM OrderItems WHERE OrderItemID = %s;"""
    data = (OrderItemID,)

    cursor.execute(query, data)
    db_conn.commit()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('OrderItem deleted!', 200)

################################################
# Place an Order
################################################

@app.route('/customerOrder')
def customerOrder_page():
    return render_template('customerOrder.html')

@app.route('/get-customer-id', methods=['POST'])
def get_customer_id():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    search_term = request.get_json(force=True)["name"]
    query = """SELECT CustomerID FROM Customers WHERE Name = %s;"""
    data = (search_term,)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/insert-order', methods=['POST'])
def insert_order():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    query =  """INSERT INTO Orders (CustomerID, EmployeeID) VALUES (%s, %s);"""
    data = (info["CustomerID"], info["EmployeeID"])

    cursor.execute(query, data)
    db_conn.commit()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Order added!', 200)

@app.route('/get-order-id', methods=['POST'])
def get_order_id():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    query = """SELECT MAX(OrderID) FROM Orders;"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/search-order-item', methods=['POST'])
def search_order_item():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    search_term = request.get_json(force=True)["name"]
    query = """SELECT PLU, Name, Description, UnitCost
                FROM Inventory
                WHERE Name LIKE %s
                ORDER BY Name;"""
    data = (["%" + search_term + "%"])

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/place-order', methods=['POST'])
def place_order():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    for item in info:
        query =  """INSERT INTO OrderItems (Quantity, OrderID, PLU) VALUES (%s, %s, %s);"""
        data = (item['quantity'], item['OrderID'], item['PLU'])

        cursor.execute(query, data)
        db_conn.commit()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Order added!', 200)

@app.route('/customer-order-dropdown', methods=['POST'])
def customer_order_dropdown():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    query = """SELECT Name FROM Customers ORDER BY Name;"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/employee-order-dropdown', methods=['POST'])
def employee_order_dropdown():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    query = """SELECT EmployeeID FROM Employees ORDER BY EmployeeID ASC;"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/cust-order-inv-dropdown', methods=['POST'])
def cust_order_inv_dropdown():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    query = """SELECT Name FROM Inventory;"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

################################################
# Employees
################################################
@app.route('/employees')
def employees_page():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    query =  """SELECT EmployeeID, Name, HourlyWage, Responsibilities, 
                SickDays FROM Employees ORDER BY EmployeeID ASC;"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return render_template('employees.html', rows=result)

@app.route('/get-shifts', methods=['POST'])
def get_shifts_for_employee():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    # Get the ID of the employee to view shifts for
    employee_id = request.get_json(force=True)['employee_id']
    query = """SELECT Employees.Name, Shifts.ShiftID, Shifts.Day, 
            Shifts.StartTime, Shifts.EndTime FROM Shifts
            JOIN EmployeeShifts ON Shifts.ShiftID = EmployeeShifts.ShiftID
            JOIN Employees ON EmployeeShifts.EmployeeID = Employees.EmployeeID
            WHERE Employees.EmployeeID = %s;"""
    data = (employee_id,)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/new-employee', methods=['POST'])
def insert_new_employee():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    query = """INSERT INTO Employees 
                (Name, HourlyWage, Responsibilities, SickDays) 
                VALUES (%s, %s, %s, %s);"""
    data = (info["name"], info["wage"], info["duties"], info["sick_days"])

    cursor.execute(query, data)
    db_conn.commit()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Employee added!', 200)

@app.route('/search-employees-id', methods=['POST'])
def search_employees_by_id():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    query =  """SELECT EmployeeID, Name, HourlyWage, Responsibilities, 
                SickDays FROM Employees WHERE EmployeeID = %s;"""
    data = (info["id"],)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/search-employees-name', methods=['POST'])
def search_employees_by_name():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    query =  """SELECT EmployeeID, Name, HourlyWage, Responsibilities, 
                SickDays FROM Employees WHERE Name = %s;"""
    data = (info["name"],)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/search-employees-duties', methods=['POST'])
def search_employees_by_duties():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    query =  """SELECT EmployeeID, Name, HourlyWage, Responsibilities, 
                SickDays FROM Employees WHERE Responsibilities = %s;"""
    data = (info["duties"],)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/search-employees-wage', methods=['POST'])
def search_employees_by_wage():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    query =  """SELECT EmployeeID, Name, HourlyWage, Responsibilities, 
                SickDays FROM Employees WHERE HourlyWage = %s;"""
    data = (info["wage"],)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/search-employees-sick-days', methods=['POST'])
def search_employees_by_sick_days():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    query =  """SELECT EmployeeID, Name, HourlyWage, Responsibilities, 
                SickDays FROM Employees WHERE SickDays = %s;"""
    data = (info["sickdays"],)

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/delete-employee', methods=['POST'])
def delete_employee():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    # Delete from the Employees table
    employee_id = request.get_json(force=True)["employee_id"]
    query =  """DELETE FROM Employees WHERE EmployeeID = %s;"""
    data = (employee_id,)
    cursor.execute(query, data)
    db_conn.commit()

    # delete rows with null foreign keys from the EmployeeShifts table
    query = """DELETE FROM EmployeeShifts WHERE EmployeeID IS NULL OR ShiftID IS NULL"""
    cursor.execute(query, data)
    db_conn.commit()

    cursor.close()
    db_pool.putconn(db_conn)
    message = 'Employee with ID ' + employee_id + ' removed from the database'
    return make_response(message, 200)

@app.route('/update-employee', methods=['POST'])
def update_employee():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    data = (info["name"], info["wage"], info["duties"], info["sick_days"], info["id"])
    query = """UPDATE Employees 
                SET Name = %s,
                    HourlyWage = %s,
                    Responsibilities = %s,
                    SickDays = %s
                WHERE EmployeeID = %s;"""
    cursor.execute(query, data)
    db_conn.commit()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Updated employee information', 200)


################################################
# Shifts
################################################
@app.route('/shifts')
def shifts_page():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    query = """SELECT ShiftID, Day, StartTime, EndTime 
                FROM Shifts ORDER BY ShiftID ASC;"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return render_template('shifts.html', rows=result)

@app.route('/new-shift', methods=['POST'])
def insert_new_shift():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    info = request.get_json(force=True)

    # check if the shift already exists
    query = """SELECT Day, StartTime, EndTime FROM Shifts 
            WHERE Day = %s AND StartTime = %s AND EndTime = %s;"""
    data = (info["day"], info["start_time"], info["end_time"])
    cursor.execute(query, data)
    result = cursor.fetchall()
    if result:
        cursor.close()
        db_pool.putconn(db_conn)
        return make_response('Shift already exists!', 500)
    else:
        query = """INSERT INTO Shifts (Day, StartTime, EndTime)  
                VALUES (%s, %s, %s);"""
        data = (info["day"], info["start_time"], info["end_time"])
        cursor.execute(query, data)
        db_conn.commit()
        cursor.close()
        db_pool.putconn(db_conn)
        return make_response('Shift added!', 200)

@app.route('/get-employees', methods=['POST'])
def get_employees_for_shift():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    # Get the ID of the employee to view shifts for
    shift_id = request.get_json(force=True)['shift_id']
    query =  """SELECT Shifts.ShiftID, Employees.Name FROM Shifts
                JOIN EmployeeShifts ON Shifts.ShiftID = EmployeeShifts.ShiftID
                JOIN Employees ON EmployeeShifts.EmployeeID = Employees.EmployeeID
                WHERE Shifts.ShiftID = %s;"""
    data = (shift_id,)
    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/assign-shifts-dropdown', methods=['POST'])
def assign_shifts_dropdown():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    query = """SELECT ShiftID FROM Shifts ORDER BY ShiftID ASC;"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/assign-shift', methods=['POST'])
def assign_shift():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    shift_id = request.get_json(force=True)['shift_id']
    employee_id = request.get_json(force=True)['employee_id']

    # check if assignment already exists
    query = """SELECT EmployeeID, ShiftID FROM EmployeeShifts 
            WHERE EmployeeID = %s AND ShiftID = %s;"""
    data = (employee_id, shift_id)
    cursor.execute(query, data)
    result = cursor.fetchall()
    if result:
        cursor.close()
        db_pool.putconn(db_conn)
        return make_response('Employee already works this shift!', 500)
    else:
        query = """INSERT INTO EmployeeShifts (EmployeeID, ShiftID) VALUES (%s, %s);"""
        data = (employee_id, shift_id)
        cursor.execute(query, data)
        db_conn.commit()
        cursor.close()
        db_pool.putconn(db_conn)
        return make_response('Assigned a shift to an employee!', 200)

@app.route('/delete-shift', methods=['POST'])
def delete_shift():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    shift_id = request.get_json(force=True)["shift_id"]

    # delete from the Employees table
    query =  """DELETE FROM Shifts WHERE ShiftID = %s;"""
    data = (shift_id,)
    cursor.execute(query, data)
    db_conn.commit()

    # delete rows with null foreign keys from the EmployeeShifts table
    query = """DELETE FROM EmployeeShifts WHERE EmployeeID IS NULL OR ShiftID IS NULL"""
    cursor.execute(query)
    db_conn.commit()
    
    cursor.close()
    db_pool.putconn(db_conn)
    message = 'Shift with ID ' + shift_id + ' removed from the database'
    return make_response(message, 200)

@app.route('/update-shift', methods=['POST'])
def update_shift():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    info = request.get_json(force=True)
    data = (info["day"], info["start_time"], info["end_time"], info["id"])
    query = """UPDATE Shifts 
                SET Day = %s,
                    StartTime = %s,
                    EndTime = %s
                WHERE ShiftID = %s;"""
    cursor.execute(query, data)
    db_conn.commit()
    
    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Updated shift information', 200)

################################################
# Inventory
################################################
@app.route('/inventory')
def inventory_page():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    query = """SELECT PLU, Name, Description, UnitCost, Quantity 
                FROM Inventory ORDER BY PLU ASC;"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return render_template('inventory.html', results=result)

@app.route('/new-inventory', methods=['POST'])
def insert_new_inventory():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    item = request.get_json(force=True)['item']
    description = request.get_json(force=True)['description']
    unit = float(request.get_json(force=True)['unit'])
    quantity = int(request.get_json(force=True)['quantity'])

    query = """INSERT INTO Inventory (Name, Description, UnitCost, Quantity) 
                VALUES (%s, %s, %s, %s);"""
    data = (item, description, unit, quantity)
    cursor.execute(query, data)
    db_conn.commit()
    
    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Inventory added!', 200)

@app.route('/search-inventory-name', methods=['POST'])
def search_inventory_by_name():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    search_term = request.get_json(force=True)["name"]
    query = """SELECT PLU, Name, Description, UnitCost, Quantity 
                FROM Inventory WHERE Name LIKE %s;"""
    data = (["%" + search_term + "%"])

    cursor.execute(query, data)
    result = cursor.fetchall()

    cursor.close()
    db_pool.putconn(db_conn)
    return make_response(json.dumps(result, indent=4, sort_keys=True, default=str), 200)

@app.route('/update-inventory', methods=['POST'])
def update_inventory():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    plu = request.get_json(force=True)['plu']
    item = request.get_json(force=True)['item']
    description = request.get_json(force=True)['description']
    unit = float(request.get_json(force=True)['unit'])
    quantity = int(request.get_json(force=True)['quantity'])

    query = """UPDATE Inventory
            SET Name = %s,
                Description = %s,
                UnitCost = %s,
                Quantity = %s
            WHERE PLU = %s;"""
    data = (item, description, unit, quantity, plu)
    cursor.execute(query, data)
    db_conn.commit()
    
    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Inventory added!', 200)

@app.route('/delete-inventory', methods=['POST'])
def delete_inventory():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    plu = request.get_json(force=True)["info"]
    query = """DELETE FROM Inventory WHERE PLU = %s;"""
    data = (plu,)
    cursor.execute(query, data)
    db_conn.commit()
    
    cursor.close()
    db_pool.putconn(db_conn)
    return make_response('Inventory deleted!', 200)
