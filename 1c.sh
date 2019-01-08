#!/usr/bin/env bash
# do not split function call with ifdef

patch -p1 << EOF
diff --git a/common/drive.c b/common/drive.c
index 4b0825f..edb63c0 100644
--- a/common/drive.c
+++ b/common/drive.c
@@ -17,6 +17,7 @@
  */

 #include <stdio.h>
+#include <stdlib.h>
 #include <unistd.h>
 #include <sys/stat.h>
 #include <time.h>
EOF