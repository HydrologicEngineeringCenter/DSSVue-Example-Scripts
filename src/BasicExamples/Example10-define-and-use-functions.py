
def printString(stringToPrint) :
  "Prints a tag plus the supplied string"
  tag = "function printString : "
  print tag + stringToPrint

def addString(string_1, string_2) :
  "Concatenates 2 strings and returns the result"
  concatenatedString = string_1 + string_2
  return concatenatedString

testString = "this is a test"
printString(testString)
wholeString = addString("part1:", "part2")
printString(wholeString)
printString(addString("this is ", "another test"))