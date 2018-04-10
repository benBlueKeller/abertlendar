from datetime import datetime
from datetime import timedelta

class ScooperError(Exception):
    """Exception for when given scooper not on schedule"""
    def __init__(self, scooper, scoopers, message="Scooper given not found on schedule"):
        super(ScooperError, self).__init__()
        self.scooper = scooper
        self.scoopers = scoopers
        self.message = message


def scooper_match(query_scooper, possible_match):
    if ":" in possible_match:
        scooper_match(query_scooper, possible_match.split(":"))
    if isinstance(possible_match, (set, list)):
        for scooper in possible_match:
            if scooper_match(query_scooper, scooper):
                return True
        return False

    query_scooper = query_scooper.upper()
    possible_match = possible_match.upper()
    if query_scooper == possible_match:
        return True
    split_scooper = possible_match.split(' ')
    check = ''
    for i, word in enumerate(split_scooper):
        if len(check) > 0:
            check += ' '
        check += split_scooper[i]
        if check == query_scooper:
            return True
    return False


def par_sheet(values, pytz=None):
    class Shifts(list):
        def on_day(self, date):
            these = []
            for shift in self:
                if ((date.day, date.month, date.year) ==
                     (shift["start"].day, shift["start"].month, shift["start"].year)):
                    these.append(shift)
            return these
    shifts = Shifts()
    this_week = False
    for irow, row in enumerate(values):
        # look for the first row that has saturday in column A
        if len(row) > 0:
            if row[0].rstrip().lstrip().upper() == 'SATURDAY':
                weekdays = []
                for col in row:
                    trimmed = col.rstrip().lstrip()
                    #checks for weekdays by finding alpha strings
                    if trimmed.isalpha() == True:
                        weekday = trimmed
                    elif trimmed != '' and '/' in trimmed:
                        #split parts apart to add leading zeros to month\day
                        spl = trimmed.split("/", 2)
                        if len(spl[0]) != 2:
                            spl[0] =  '0' + spl[0]
                        if len(spl[1]) != 2:
                            spl[1] = '0' + spl[1]
                        try:
                            date = datetime.strptime("/".join(spl), "%m/%d/%Y")
                            weekdays.append((date, weekday))
                        except ValueError as Err:
                            if len(weekdays) == 7:
                                pass
                            else:
                                raise Err
                this_week = weekdays

            elif this_week:
                counter = 0
                shift = []
                row_shifts = []

                for col in row:
                    shift.append(col)
                    counter += 1
                    if counter >= 3:
                        row_shifts.append(shift)
                        counter = 0
                        shift = []

                for ishift, shift in enumerate(row_shifts):
                    if ishift < len(this_week) and "-" in shift[2]:
                        date, weekday = this_week[ishift]
                        time_str = shift[2].strip()
                        if " " in time_str and not "@" in time_str:
                            time_str, duty = time_str.split(" ", 1)
                        # BUG: ValueError; for format "@ # #:##-{}" start_time will be wrong
                        try:
                            start_str, end_str = time_str.split('-', 1)
                            start_hours, start_minutes = start_str.split(':', 1)
                            start_hours = int(start_hours)
                            start_minutes = int(start_minutes)
                            # assuming 4am ealiest start
                                # >4pm starts have shift before
                            if start_hours < 4 or bool(shifts.on_day(date)) and shifts.on_day(date)[::-1][0]["start"].hour > start_hours:
                                start_hours += 12
                            start_time = date + timedelta(hours=start_hours, minutes=start_minutes)
                        except ValueError:
                            print('WARNING: ValueError while finding shift start time from ' + time_str)
                        try:
                            end_hours, end_minutes = end_str.split(':', 1)
                            end_hours = int(end_hours) + 12 # assuming all shifts end in pm
                            end_minutes = int(end_minutes)
                            end_time = date + timedelta(hours=end_hours, minutes=end_minutes)
                        except ValueError: # for line and close shifts parse from length
                            try:
                                hours_from_start = float(shift[1])
                                if hours_from_start >= 6:
                                    hours_from_start += 0.5 # length does not include breaks
                                end_time = start_time + timedelta(hours=hours_from_start)
                            except ValueError:
                                end_time = start_time + timedelta(hours=1)
                        if pytz and (start_time.tzinfo is None
                                or start_time.tzinfo.utcoffset(start_time) is None):
                            start_time = pytz.localize(start_time)
                        if pytz and (end_time.tzinfo is None
                                or end_time.tzinfo.utcoffset(end_time) is None):
                            end_time = pytz.localize(end_time)
                        shifts.append(dict(name = shift[0],
                            length=shift[1],
                            start= start_time,
                            end = end_time,
                            time_str = time_str,
                            row = irow))
    return shifts

def par_sheet_dict(values):
    shifts = par_sheet(values)
    scoopers = set()
    time_min = shifts[0]["start"]
    time_max = shifts[0]["end"]
    for shift in shifts:
        scoopers = scoopers.union([shift["name"].upper()])
        if shift["start"] < time_min:
            time_min = shift["start"]
        if shift["end"] > time_max:
            time_max = shift["end"]
    return dict(shifts=shifts, scoopers=scoopers, time_max=time_max, time_min=time_min)
