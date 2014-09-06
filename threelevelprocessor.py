#!/usr/bin/python

import sys, re

if len(sys.argv) != 3:
  raise ValueError("Usage: input output")

inputFileStr = sys.argv[1]
outputFileStr = sys.argv[2]

print "Input file:" + inputFileStr + " Output:" + outputFileStr

chapter =\
"""
---
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

exercise =\
"""
---
template: exercise
name: {0}

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

```java
!INCLUDE "Class.java" 2-4 3,4 * trim
```

???
IG
"""

hashtagTypes = {"exercise" : exercise, "image" : image, "code" : code}

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

    return hashtagTypes[hashtag].format(hashtagPartitions[0])

outputFile = open(outputFileStr,'w')

# Write out layouts
layouts=\
"""
name: chapter
layout: true
class: center, middle

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

outputFile.write(layouts)

with open(inputFileStr) as inputFile:
  for line in inputFile:
    indentLevel = len(line) - len(line.lstrip())

    if indentLevel == 0:
      # Its a chapter
      lineOutput = processChapter(line)
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
