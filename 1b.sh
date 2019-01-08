#!/usr/bin/env bash
# do not split function call with ifdef

patch -p1 << EOF
diff --git a/common/types.h b/common/types.h
index 50c841e..096c5b7 100644
--- a/common/types.h
+++ b/common/types.h
@@ -35,7 +35,9 @@
 /*
  * Should be, but isn't, defined in uuid/uuid.h
  */
+#ifndef UUID_STR_LEN
 #define UUID_STR_LEN	36
+#endif

 /* fundamental page size - probably should not be hardwired, but
  * for now we will
EOF