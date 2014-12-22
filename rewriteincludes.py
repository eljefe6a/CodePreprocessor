#!/usr/bin/python

import sys, re, os

if len(sys.argv) != 2:
  raise ValueError("Usage: input")

inputFileStr = sys.argv[1]

print "Input file:" + inputFileStr

outputFile = open(inputFileStr + ".tmp",'w')

with open(inputFileStr) as inputFile:
  for line in inputFile:
    output = line

    # A code include always starts with a "```"
    if line.startswith("```"):
      nextline = next(inputFile)

      matchObj = re.match( r'\s*!INCLUDE \"(.*)\"\s?([0-9,-]+)?\s?([0-9,-]+)?\s?(.)?\s?(trim|notrim)?\s*', nextline)

      if matchObj:
        # Include directive found
        # Parse out options

        filename = matchObj.group(1)
        includeLineNumbers = matchObj.group(2)
        highlightLineNumbers = matchObj.group(3)
        highlightCharacter = matchObj.group(4)
        shouldTrimWhitespace = matchObj.group(5)

        output = "![:include " + filename

        if includeLineNumbers is not None:
          output += ", "
          # Replace all commas with spaces
          output += includeLineNumbers.replace(",", " ")

        if highlightLineNumbers is not None:
          output += ", "
          # Replace all commas with spaces
          output += highlightLineNumbers.replace(",", " ")

        if highlightCharacter is not None:
          output += ", " + highlightCharacter

        if shouldTrimWhitespace is not None:
          output += ", " + shouldTrimWhitespace

        # Add the final ]
        output += "]\n"

        # Gobble the terminating "```"
        nextline = next(inputFile)

        if nextline.strip() != "```":
          print "Next line wasn't expected was:" + nextline
      else:
        output = line + nextline

    
    outputFile.write(output)

inputFile.close()
outputFile.close()

os.remove(inputFileStr)
os.rename(inputFileStr + ".tmp", inputFileStr)