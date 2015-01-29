#!/usr/bin/python

from pandocfilters import toJSONFilter, Str
import sys, re, os

# Change current working directory
abspath = os.path.abspath(sys.argv[0])
abspath = os.path.abspath(os.path.join(abspath, os.pardir))
dname = os.path.dirname(abspath)
os.chdir(dname)
print "Current:" + os.getcwd()

def mixrange(s):
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l,h = map(int, i.split('-'))
            r+= range(l,h+1)
    return r

def calculateMinWhitespace(filename, includeLineNumbersArray):
  whitespaceCurrentLineNumber = 1

  currentMin = sys.maxint
  with open(os.path.join(os.getcwd(), filename)) as whitespaceIncludeFile:
    for whitespaceIncludeLine in whitespaceIncludeFile:
      writeLine = True

      # Included line numbers provided
      if includeLineNumbersArray is not None:
        # Check if the line number is in the list provided
        if whitespaceCurrentLineNumber not in includeLineNumbersArray:
          writeLine = False

      if writeLine == True:
        # See what the minimum whitespace size is
        currentMin = min(currentMin, len(whitespaceIncludeLine) - len(whitespaceIncludeLine.lstrip()))

      whitespaceCurrentLineNumber += 1

  return currentMin

def processIncludeLine(filename, includeLineNumbersArray, highlightLineNumbersArray, highlightCharacter, shouldTrimWhitespace):
  currentLineNumber = 1

  output = ""

  print "Including: " + filename + " " + str(includeLineNumbersArray) + " " + str(highlightLineNumbersArray) + " " + highlightCharacter + " " + str(shouldTrimWhitespace)

  if shouldTrimWhitespace == True:
    whiteSpaceToTrim = calculateMinWhitespace(filename, includeLineNumbersArray)

  with open(filename) as includeFile:
    for includeLine in includeFile:
      writeLine = True
      writeHighlight = False

      # Included line numbers provided
      if includeLineNumbersArray is not None:
        # Check if the line number is in the list provided
        if currentLineNumber not in includeLineNumbersArray:
          writeLine = False

      # Included highlight line numbers provided
      if highlightLineNumbersArray is not None:
        # Check if the line number is in the highlight list provided
        if currentLineNumber in highlightLineNumbersArray:
          writeHighlight = True

      if writeLine == True:
        if writeHighlight == True:
          output += highlightCharacter + ' '

        if shouldTrimWhitespace == True:
          includeLine = includeLine[whiteSpaceToTrim:]

        output += includeLine

      currentLineNumber += 1

  return output

foundInclude = False
includeSoFar = ""

def includesource(key, value, format, meta):
  global foundInclude
  global includeSoFar

  if key == 'Str':
    if foundInclude == True:
      includeSoFar += value + " "
    elif foundInclude == False and value.strip().startswith('[:includesource'):
      foundInclude = True
      includeSoFar += value + " "
    
    if foundInclude == True:
      matchObj = re.match( r'\s*\[:includesource ([a-zA-Z_\/.]*),?\s?([0-9 -]+)?,?\s?([0-9 -]+)?,?\s?(.)?,?\s?(trim|notrim)?\]\s*', includeSoFar)

      if matchObj:
        # Full Include directive found
        # Parse out options
        foundInclude = False

        filename = matchObj.group(1)
        includeLineNumbers = matchObj.group(2)
        highlightLineNumbers = matchObj.group(3)
        highlightCharacter = matchObj.group(4)
        shouldTrimWhitespace = matchObj.group(5)

        if includeLineNumbers is not None:
          includeLineNumbersArray = mixrange(includeLineNumbers)

        if highlightLineNumbers is not None:
          highlightLineNumbersArray = mixrange(highlightLineNumbers)

        if highlightCharacter is None:
          highlightCharacter = "*"

        if shouldTrimWhitespace is None:
          shouldTrimWhitespace = False
        elif shouldTrimWhitespace == "trim":
          shouldTrimWhitespace = True
        else:
          shouldTrimWhitespace = False

        return Str(processIncludeLine(filename, includeLineNumbersArray, highlightLineNumbersArray, highlightCharacter, shouldTrimWhitespace))
      else:
        # Full include directive not found yet
        # Return empty array to remove it
        return []

if __name__ == "__main__":
  toJSONFilter(includesource)
