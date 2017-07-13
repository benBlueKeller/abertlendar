from datetime import datetime

def par_sheet(values):
	values
	teams = [];
	for i, row in values:
		# look for the first row that has saturday in column A
		if row[0].rstip().lstrip().upper() == 'SATURDAY':
			week_1 = dict(row_0 = i, days = dict())
			for i, col in row:
				trimmed = col.rstrip().lstrip()
				#checks for weekdays by finding alpha strings
				if trimmed.isalpha() == True:
					weekday = trimmed
				elif trimmed != '':
					#split parts apart to add leading zeros to month\day
					spl = trimmed.split("/", 2)
					if len(spl[0]) != 2:
						spl[0] =  '0' + spl[0] 
					if len(spl[1]) != 2:
						spl[1] = '0' + spl[1]
					time = datetime.strptime("/".join(spl), "%m/%d/%Y")
					week_1['days'][weekday] = time
			return week_1





				






