CodePreprocessor
================

Python based code pre-processor to include source code and highlight it with asterisks or your choice of a character.

Usage:
./preprocesscode.py input.md output.md

In the Markdown:
!INCLUDE "Class.java"
Will include Class.java

!INCLUDE "Class.java" 2-4 3 *

Will include lines 2 to 4 from Class.java and highlight line 3 with *

!INCLUDE "Class.java" 2-4 3,4 * trim

Will include lines 2 to 4 from Class.java and highlight lines 3 and 4 with *
then trim the whitespace to the minimum needed for lines 2 to 4.
