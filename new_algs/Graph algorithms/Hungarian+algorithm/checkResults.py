from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/mnt/c/chromedriver.exe')
driver.get("http://www.hungarianalgorithm.com/solve.php")

template = 'cell_'
row = 0
with open("input.txt", 'r') as file:
	for line in file:
		x = line.split()
		rowLen = len(x)
		for count, floatV in enumerate(x):
			inputBox = template + str(row) + '_' + str(count)
			print("document.getElementByName({}).setAttribute('value','{}')".format(inputBox, floatV))
			#driver.execute_script("document.getElementById('{}').setAttribute('value','{}')".format(inputBox, floatV))
			elem = driver.find_element_by_name(inputBox)
			elem.send_keys(floatV)

		row+=1
close()
