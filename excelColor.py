# -*- coding: utf-8 -*-  
import xlrd  
import xlwt
import sys
from datetime import date,datetime

import os  
	  
def file_name():   
	L=[]   
	for root, dirs, files in os.walk("./"):  
		for file in files:  
			if os.path.splitext(file)[1] == '.xls':  
				L.append(os.path.join(root, file))  
	return L  


def isRight(timelist):
	if len(timelist) <= 0:
		return False
	condition1 = False
	condition2 = False
	
	for ts in timelist:
		try:
			if ts == '':
			  continue
			print "ts:",ts
			t = datetime.strptime(ts,'%H:%M')
			hour = t.hour
			minite = t.minute
			if hour < 8 or (hour ==8 and minite<=30):
				condition1 = True
			if hour >= 18:
				condition2 = True
		except:
			continue
	print  "condition1:", condition1 ,"condition2",condition2
	return condition2 and condition1
def read_excel(excels):  
	# 打开文件  
	workbook = xlrd.open_workbook(excels)
	# 新文件
	new_workbook = xlwt.Workbook()

	# 获取旧表名
	sheetName = workbook.sheet_names()[0]

	worksheet = new_workbook.add_sheet(sheetName)
	#颜色设置
	pattern = xlwt.Pattern() # Create the Pattern
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
	pattern.pattern_fore_colour = 5 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
	style = xlwt.XFStyle() # Create the Pattern
	style.pattern = pattern # Add Pattern to Style

	pattern2 = xlwt.Pattern() # Create the Pattern
	pattern2.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
	pattern2.pattern_fore_colour = 1 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
	style2 = xlwt.XFStyle() # Create the Pattern
	style2.pattern = pattern2 # Add Pattern to Style

	# print workbook.sheet_names() # [u'sheet1', u'sheet2']  

	table = workbook.sheet_by_index(0)
	col = table.ncols
	row = table.nrows

	# print "col",col ,"row",row
	#  print "h:",row,"lie",col
	for c in range(0,col):
		for r in range(0,row):
			# ctype :  0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
			vtyps = table.cell(r,c).ctype
			print type(vtyps),vtyps
			worksheet.col(r).width = 256*20
			values = table.cell_value(r,c)
			if vtyps == 0:
				worksheet.write(r, c, values, style)
			if vtyps != 1:
				continue
			timelist = values.split(" ")
			if isRight(timelist) == False:
				worksheet.write(r, c, values, style)
			else:
				worksheet.write(r, c, values)
	
	try:
		new_workbook.save('data/'+excels)
	except:
		print "some exception"
if __name__ == '__main__':  
	excelFileList = file_name()
	for excels in excelFileList:
		read_excel(excels)
	print "over"