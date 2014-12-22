#!/usr/bin/python

import sys, re

if len(sys.argv) != 3:
  raise ValueError("Usage: input output")

inputFileStr = sys.argv[1]
outputFileStr = sys.argv[2]

print "Input file:" + inputFileStr + " Output:" + outputFileStr

def mixrange(s):
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l,h = map(int, i.split('-'))
            r+= range(l,h+1)
    return r

outputFile = open(outputFileStr,'w')

def calculateMinWhitespace(filename, includeLineNumbersArray):
  whitespaceCurrentLineNumber = 1

  currentMin = sys.maxint
  with open(filename) as whitespaceIncludeFile:
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

  print "Including: " + filename + " " + str(includeLineNumbersArray) + " " + str(highlightLineNumbersArray) + " " + highlightCharacter + " " + str(shouldTrimWhitespace)

  if shouldTrimWhitespace == True:
    whiteSpaceToTrim = calculateMinWhitespace(filename, includeLineNumbersArray)

  with open(filename) as includeFile:
    for includeLine in includeFile:
      writeLine = True
      writeHighlight = False

      # Included line numbers provided
      if includeLineNumbers is not None:
        # Check if the line number is in the list provided
        if currentLineNumber not in includeLineNumbersArray:
          writeLine = False

      # Included highlight line numbers provided
      if highlightLineNumbers is not None:
        # Check if the line number is in the highlight list provided
        if currentLineNumber in highlightLineNumbersArray:
          writeHighlight = True

      if writeLine == True:
        if writeHighlight == True:
          outputFile.write(highlightCharacter + ' ')

        if shouldTrimWhitespace == True:
          includeLine = includeLine[whiteSpaceToTrim:]

        outputFile.write(includeLine)

      currentLineNumber += 1

with open(inputFileStr) as inputFile:
  for line in inputFile:
    matchObj = re.match( r'\s*!INCLUDE \"(.*)\"\s?([0-9,-]+)?\s?([0-9,-]+)?\s?(.)?\s?(trim|notrim)?\s*', line)

    if matchObj:
      # Include directive found
      # Parse out options

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

      processIncludeLine(filename, includeLineNumbersArray, highlightLineNumbersArray, highlightCharacter, shouldTrimWhitespace)

    else:
      # Just write out the line
      outputFile.write(line)

inputFile.close()
outputFile.close()
