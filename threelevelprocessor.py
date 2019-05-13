#!/usr/bin/python

import sys, re, os

if len(sys.argv) != 3:
  raise ValueError("Usage: input outputdir")

inputFileStr = sys.argv[1]
outputDirStr = sys.argv[2]

if os.path.exists(outputDirStr):
  if os.path.isdir(outputDirStr) == False:
    raise ValueError("outputdir must be a directory")
else:
  os.makedirs(outputDirStr)

print "Input file:" + inputFileStr + " Output Dir:" + outputDirStr

chapter =\
"""
template: chapter
name: {0}

???
IG
"""

section =\
"""
---
template: section
name: {0}

???
IG
"""

regular =\
"""
---
template: regular
name: {0}

???
IG
"""

demo =\
"""
---
template: demo
name: {0}
minutes: {1}

### We will now demonstrate TODO

???
IG
"""

exercise =\
"""
---
template: exercise
name: {0}
minutes: {1}
file:TODO.md

## In this exercise, you will TODO.

## Time: {{{{minutes}}}} minutes

???
IG
"""

image =\
"""
---
template: image
name: {0}

.main-image[![Alt](images/image.jpg)]

???
IG
"""

code =\
"""
---
template: code
name: {0}

![:includesource Class.java, 20, 20, *, trim]

???
IG
"""

twocolumn =\
"""
---
template: regular
name: {0}

.list-container.list-container-75-25[
* TODO
* .image90[![Alt text](images/image.png)]
]

???
IG
"""

hashtagTypes = {"exercise" : exercise, "image" : image, "code" : code, "demo" : demo, "twocolumn" : twocolumn}

def processChapter(line):
  return chapter.format(line.lstrip())

def processSection(line):
  return section.format(line.lstrip())

def processContent(line):
  if not "#" in line:
    return regular.format(line.lstrip())
  else:
    hashtagPartitions = line.strip().partition("#")

    # Parse out hashtag
    hashtag = hashtagPartitions[2]

    # Exercises and demos have times
    if hashtag.startswith("exercise") or hashtag.startswith("demo"):
      hashtagTime = hashtag.strip().partition(" ")

      return hashtagTypes[hashtagTime[0]].format(hashtagPartitions[0].strip(), hashtagTime[2].strip())
    else:
      return hashtagTypes[hashtag].format(hashtagPartitions[0].strip())

outputFile = None

# Write out layouts
layouts=\
"""
name: chapter
layout: true
class: center, middle, chapter

# {{name}}

---
name: section
layout: true
class: center, middle

# {{name}}

---
name: regular
layout: true
class: top-of-slide

<div class="slide-title">{{name}}</div>

---
name: exercise
layout: true
class: top-of-slide

<div class="slide-title">{{name}}</div>

---
name: demo
layout: true
class: top-of-slide

<div class="slide-title">{{name}}</div>

---
name: image
layout: true
class: top-of-slide

<div class="slide-title">{{name}}</div>

---
name: code
layout: true
class: top-of-slide

<div class="slide-title">{{name}}</div>

"""

outputFile = open(outputDirStr + "/header.md",'w')
outputFile.write(layouts)

with open(inputFileStr) as inputFile:
  for line in inputFile:
    indentLevel = len(line) - len(line.lstrip())

    if indentLevel == 0:
      # Its a chapter
      if outputFile != None:
        # Close the previous file
        outputFile.close()

      lineOutput = processChapter(line)

      # Open a new file with the name of the chapter as the file name
      outputFile = open(outputDirStr + "/" + line.lower().replace(" ", "_").replace("?", "").strip() + ".md",'w')
    elif indentLevel == 2:
      # Its a section
      lineOutput = processSection(line)
    elif indentLevel == 4:
      # Its a content slide
      lineOutput = processContent(line)
    else:
      print "Indent level too high. Level:" + str(indentLevel) + " For line:" + line
      lineOutput = line

    outputFile.write(lineOutput)

outputFile.close()
