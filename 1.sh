#!/usr/bin/env bash
# do not split function call with ifdef

patch -p1 << EOF
diff --git a/common/drive_minrmt.c b/common/drive_minrmt.c
index 59a40a7..04fed3e 100644
--- a/common/drive_minrmt.c
+++ b/common/drive_minrmt.c
@@ -2585,11 +2585,12 @@ read_label( drive_t *drivep )
 	if (( nread == 0 )  /* takes care of sun */
 	      ||            /* now handle SGI */
 	      (nread < 0 && saved_errno == ENOSPC )) {
-		mlog( MLOG_NORMAL | MLOG_DRIVE,
 #ifdef DUMP
+		mlog( MLOG_NORMAL | MLOG_DRIVE,
 		      _("encountered EOD : assuming blank media\n") );
 #endif
 #ifdef RESTORE
+		mlog( MLOG_NORMAL | MLOG_DRIVE,
 		      _("encountered EOD : end of data\n") );
 #endif
 		( void )rewind_and_verify( drivep );
diff --git a/common/main.c b/common/main.c
index b3605d1..0c23eb4 100644
--- a/common/main.c
+++ b/common/main.c
@@ -581,12 +581,14 @@ main( int argc, char *argv[] )
 		sigaction( SIGTERM, &sa, NULL );
 		sigaction( SIGQUIT, &sa, NULL );

+#ifdef DUMP
 		ok = drive_init2( argc,
 				  argv,
-#ifdef DUMP
 				  gwhdrtemplatep );
 #endif /* DUMP */
 #ifdef RESTORE
+		ok = drive_init2( argc,
+				  argv,
 				  ( global_hdr_t * )0 );
 #endif /* RESTORE */
 		if ( ! ok ) {
@@ -629,12 +631,14 @@ main( int argc, char *argv[] )
 	 * time-consuming chore. drive_init3 will synchronize with each slave.
 	 */
 	if ( ! init_error ) {
+#ifdef DUMP
 		ok = drive_init2( argc,
 				  argv,
-#ifdef DUMP
 				  gwhdrtemplatep );
 #endif /* DUMP */
 #ifdef RESTORE
+		ok = drive_init2( argc,
+				  argv,
 				  ( global_hdr_t * )0 );
 #endif /* RESTORE */
 		if ( ! ok ) {
--
2.19.1
EOF