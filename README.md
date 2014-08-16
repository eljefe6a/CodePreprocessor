CodePreprocessor
================

PreProcessCode
================

Python based code pre-processor to include source code and highlight it with asterisks or your choice of a character.

Usage:
./preprocesscode.py input.md output.md

In the Markdown:

```
  !INCLUDE "Class.java"
```

Will include Class.java

```
  !INCLUDE "Class.java" 2-4 3 *
```

Will include lines 2 to 4 from Class.java and highlight line 3 with an *

```
  !INCLUDE "Class.java" 2-4 3,4 * trim
```

Will include lines 2 to 4 from Class.java and highlight lines 3 and 4 with an *
then trim the whitespace to the minimum needed for lines 2 to 4.

ThreeLevelProcessor
================

Python based code pre-processor to take a three-level outline and create
Remarkjs output. The levels in the outline must be tabs.

Usage:
./preprocesscode.py threelevel.txt output.md

Content levels can include hashtags at the end to give a template type.
The tags are #exercise, #image, and #code. See threelevel.txt for an example.
