import calendar, datetime, sys

try    : year = int(sys.argv[1])
except : year = datetime.datetime.now().year

Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday = range(7);
dayNames = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
monthNames = ["!!!!","January","February","March","April","May","June","July","August","September","October","November","December"]

federalHolidayNames = [
#  These are the official names by law
#  ---------------------------------------
   "New Year's Day",
   "Birthday of Martin Luther King, Jr.",
   "Washington's Birthday",
   "Memorial Day",
   "Independence Day",
   "Labor Day",
   "Columbus Day",
   "Veterans Day",
   "Thanksgiving Day",
   "Christmas Day"
]

def adjustToWeekday(date) :
   '''
   Return the nearest weekday (Mon - Fri) to the specified date
   '''
   weekday = date.weekday()
   if weekday == Saturday :
      date -= datetime.timedelta(1)
   elif weekday == Sunday :
      date += datetime.timedelta(1)
   return date
   
def ordinalStr(number) :
   '''
   Format a number as an ordinal string
   '''
   if number == -1 : 
      return "last"
   else :
      digit = number % 10
      if   digit == 1 : return "%dst" % number
      elif digit == 2 : return "%dnd" % number   
      elif digit == 3 : return "%drd" % number
      else            : return "%dth" % number   
   
def nthWeekday(n, weekday, month, year) : 
   '''
   Return the nth specified weekday of the specified month and year
   '''
   weeks = calendar.monthcalendar(year, month)
   if n == -1 :
      for i in range(len(weeks))[::-1] :
         if weeks[i][weekday] != 0 : return datetime.date(year, month, weeks[i][weekday])
   else :
      count = 0
      for week in weeks :
         if week[weekday] != 0 : count += 1
         if count == n : return datetime.date(year, month, week[weekday])
      raise ValueError("%s, %d has no %s %s" % (monthNames[month], year, ordinalStr(n), dayNames[weekday]))      

def getHolidayDate(holidayName, year) :
   '''
   Return the date that the federal holiday is celebrated in the specified year
   '''
   if   holidayName == federalHolidayNames[0] : return adjustToWeekday(datetime.date(year, 1, 1))
   elif holidayName == federalHolidayNames[1] : return nthWeekday(3, Monday, 1, year)
   elif holidayName == federalHolidayNames[2] : return nthWeekday(3, Monday, 2, year)
   elif holidayName == federalHolidayNames[3] : return nthWeekday(-1, Monday, 5, year)
   elif holidayName == federalHolidayNames[4] : return adjustToWeekday(datetime.date(year, 7, 4))
   elif holidayName == federalHolidayNames[5] : return nthWeekday(1, Monday, 9, year)
   elif holidayName == federalHolidayNames[6] : return nthWeekday(2, Monday, 10, year)
   elif holidayName == federalHolidayNames[7] : return adjustToWeekday(datetime.date(year, 11, 11))
   elif holidayName == federalHolidayNames[8] : return nthWeekday(4, Thursday, 11, year)
   elif holidayName == federalHolidayNames[9] : return adjustToWeekday(datetime.date(year, 12, 25))
   else : raise ValueError("Unknown holiday name: %s" % holidayName)

def getAllHolidays(year) :
   '''
   Return a dictionary of all federal holiday in the specified year
   '''
   holidays = {}
   for holidayName in federalHolidayNames :
      date = getHolidayDate(holidayName, year)
      if date.year == year : holidays[date] = holidayName
   holidayName = federalHolidayNames[0]      
   date = getHolidayDate(holidayName, year+1)
   if date.year == year : holidays[date] = holidayName
   return holidays   
   
def main() :   
   print("Federal holidays in %d" % year)
   holidays = getAllHolidays(year)
   for date in sorted(holidays.keys()) :
      print("\t%s : %s" % (date.strftime("%a, %d %b %Y"), holidays[date]))
         
if __name__ == "__main__" : main()                            