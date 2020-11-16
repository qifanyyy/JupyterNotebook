#!/Python27/python
import xlrd
import MySQLdb

# Open the workbook and define the worksheet
book = xlrd.open_workbook("TabulatedSLA.xlsx")
sheet = book.sheet_by_index(0)

# Establish a MySQL connection
database = MySQLdb.connect (host="localhost", user = "root", passwd = "toor", db = "cloud")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

empty_table = "delete from sla;delete from rank"

cursor.execute(empty_table)
cursor.close()

cursor = database.cursor()
# Create the INSERT INTO sql query
query = """INSERT INTO sla VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
      product      = sheet.cell(r,0).value
      customer = sheet.cell(r,1).value
      rep          = sheet.cell(r,2).value
      date     = sheet.cell(r,3).value
      actual       = sheet.cell(r,4).value
      expected = sheet.cell(r,5).value
      open        = sheet.cell(r,6).value
      closed       = sheet.cell(r,7).value
      city     = sheet.cell(r,8).value
      state        = sheet.cell(r,9).value
      zip         = sheet.cell(r,10).value
      pop          = sheet.cell(r,11).value
      region   = sheet.cell(r,12).value
      # Assign values from each row
      values = (product, customer, rep, date, actual, expected, open, closed, city, state, zip, pop, region)

      # Execute sql Query
      cursor.execute(query, values)

# Close the cursor
cursor.close()
sheet = book.sheet_by_index(1)


# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
query = """INSERT INTO rank VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
      product      = sheet.cell(r,0).value
      customer = sheet.cell(r,1).value
      rep          = sheet.cell(r,2).value
      date     = sheet.cell(r,3).value
      actual       = sheet.cell(r,4).value
      expected = sheet.cell(r,5).value
      open        = sheet.cell(r,6).value
      closed       = sheet.cell(r,7).value
      city     = sheet.cell(r,8).value
      state        = sheet.cell(r,9).value
      zip         = sheet.cell(r,10).value
      pop          = sheet.cell(r,11).value
      region   = sheet.cell(r,12).value
      print (date,'\n')
      # Assign values from each row
      values = (product, customer, rep, date, actual, expected, open, closed, city, state, zip, pop, region)

      # Execute sql Query
      cursor.execute(query, values)

# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

