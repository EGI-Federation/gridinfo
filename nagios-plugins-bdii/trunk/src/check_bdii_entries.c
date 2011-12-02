/**
* Copyright (c) CERN 2011.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at #
*    http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS
* OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
**/

#define _XOPEN_SOURCE
#include <stdio.h> 
#include <errno.h>
#include <unistd.h>
#include <limits.h>
#include <ldap.h>
#define __USE_MISC
#include <time.h>  
#include <sys/time.h>  
#include <stdlib.h>

/* NAGIOS CODES */
int    OK = 0;   
int    WARNING = 1;
int    CRITICAL = 2;
int    UNKNOWN = 3;
char*  statuscode[] = {"OK", "WARNING", "CRITICAL", "UNKNOWN"};

/* Print Usage Function */
void usage(){
  printf("\n");
  printf("Usage: check_bdii_entries -H host [OPTION] \n");
  printf("\n");
  printf("Options: \n");
  printf("\t-p\tThe port of the BDII\n");
  printf("\t-b\tThe base of the BDII\n");
  printf("\t-f\tThe filter to use for the search\n");
  printf("\t-f\tNote: Shortcuts 'site', 'service' and 'stats' can be used\n");
  printf("\n");
  printf("\t-w\tWarning threshold <time/freshness warning>:<entry warning>\n");
  printf("\t-c\tCritical threshold <time/freshness critical>:<entry critical>\n");
  printf("\t-t\tTimeout in seconds (not implemented)\n");
  printf("\n");
  return;
}
 
/* Main Function */
int  main( int argc, char **argv ) {

  /*  OPTIONS */
   char*   hostname = NULL;
   int     port = 2170;
   char*   base = "o=grid";
   char*   filter = NULL;
   char*   warn_levels = NULL;
   char*   crit_levels = NULL;
   char*   attributes[] = {"modifyTimestamp",NULL};
   int     entry_warn;
   int     entry_crit;
   int     time_warn;
   int     time_crit;
   int     retcode = OK;
   
   /* Get Options */
   int          option = 0;
   while ((option = getopt(argc, argv, "H:p:t:b:w:c:f:")) != -1) {
      switch (option) {
      case 'h': 
	usage();
	exit(WARNING);
      case 'H': 
	hostname=optarg;     
	break;
      case 'p': 
	port = atoi(optarg); 
	break;
      case 'b': 
	base = optarg;       
	break;
      case 'f': 
	filter = optarg;       
	break;
      case 'w': 
	warn_levels = optarg;       
	break;
      case 'c': 
	crit_levels = optarg;       
	break;
      case 't': 
	break;
      default:  
	usage();
	exit (WARNING);
      }
   }

   /* Check the Hostname parameter */
   if ( ! hostname ) {
     fprintf(stderr,"Error: Hostname ( -H option ) not specified.\n");
     usage();
     exit (UNKNOWN);
   }
 
   /* Check the filter */
   if ( filter ) {
     int result;
     result = strcmp ( filter, "site" );
     if ( result == 0 ){
       filter = "(objectClass=GlueSite)";
     }
     result = strcmp ( filter, "service" );
     if ( result == 0 ){
       filter = "(objectClass=GlueService)";
     }
     result = strcmp ( filter, "stats" );
     if ( result == 0 ){
       filter = "(|(objectClass=UpdateStats)(objectClass=InfoSystemStats))";
       base = "o=infosys";
     }
   }else{
     filter = "(objectClass=GlueService)";
   }

   /*  Check the warning limits  */
   if ( warn_levels ){
     if ( sscanf(warn_levels, "%d:%d", &time_warn, &entry_warn) != 2 ){
       fprintf(stderr,"Error: Invalid format for warning levels, %s\n", warn_levels);
       usage();
       exit (UNKNOWN);
     }
   }else{
       fprintf(stderr,"Error: Warning levels ( -w option ) are not set.\n");
       usage();
       exit (UNKNOWN);
   }

   /*  Check the critical limits  */
   if ( crit_levels ){
     if ( sscanf(crit_levels, "%d:%d", &time_crit, &entry_crit) != 2 ){
       fprintf(stderr,"Error: Invalid format for critical levels, %s\n", crit_levels);
       usage();
       exit (UNKNOWN);
     }
   }else{
     fprintf(stderr,"Error: Critical levels ( -c option )are not set.\n");
     usage();
     exit (UNKNOWN);
   }

   /*  LDAP Variables  */
   LDAP*         ld; 
   LDAPMessage*  result;
   LDAPMessage*  entry;
   char**        values;
   int           rc=0;

   /*  Get Start Time */
   struct timeval start;
   gettimeofday(&start, NULL);

   /* Get an LDAP connection */
   if ( (ld = ldap_init( hostname, port )) == NULL ) { 
     perror( "ldap_init" ); 
     exit( UNKNOWN ); 
   } 

   /*  Bind anonymously to the LDAP server */
   rc = ldap_simple_bind_s( ld, NULL, NULL ); 
   if ( rc != LDAP_SUCCESS ) { 
     printf("CRITICAL: ldap_simple_bind_s: %s\n", ldap_err2string(rc)); 
     exit( CRITICAL ); 
   }

   /*  Do the LDAP search */
   if ( ( rc = ldap_search_ext_s( ld, base, LDAP_SCOPE_SUBTREE, 
     filter, attributes, 0, NULL, NULL, LDAP_NO_LIMIT, 
     LDAP_NO_LIMIT, &result ) ) != LDAP_SUCCESS ) { 
     printf("CRITICAL: ldap_search_ext_s: %s\n", ldap_err2string(rc)); 
     exit( CRITICAL ); 
   } 
   
   /* Get End Time */
   struct timeval end;
   gettimeofday(&end, NULL);
   time_t end_time = time(NULL);
   
    /* Get the number of results */
   int num_results = ldap_count_entries(ld,result);

   /* Calculate the response time */
   int diff_seconds;
   int diff_useconds;
   diff_seconds = end.tv_sec - start.tv_sec ;
   diff_useconds = end.tv_usec - start.tv_usec ;
   if (diff_useconds < 0 ){
     diff_seconds = diff_seconds - 1;
     diff_useconds = diff_useconds + 1000000 ;
   }

   float response_time = diff_seconds + ( diff_useconds * 0.000001);

   /* Get the last modified time and calculate the freshness*/
   double freshness = -1.0;
   entry = ldap_first_entry(ld, result); 
   if ( entry  !=  NULL ){
     if ( ( values = ldap_get_values( ld, entry, "modifyTimestamp" ) ) != NULL ){
       time_t modify_time;       
       struct tm parsed_time;
       strptime(values[0], "%Y%m%d%H%M%S", &parsed_time );
       modify_time = timegm(&parsed_time);
       if ( modify_time ){
	 freshness = difftime(end_time, modify_time);
       }
     }
   }

   /*  Do the Nagios ooutput */
   int return_code;
   return_code = strcmp ( filter, "(|(objectClass=UpdateStats)(objectClass=InfoSystemStats))" );
   if ( return_code == 0 ){
     if ( freshness > time_warn ){ 
       retcode = WARNING;
     }
     if ( freshness > time_crit ){
       retcode = CRITICAL;
     }
     printf("%s: freshness=%.0fs, entries=%d |freshness=%.0fs;entries=%d\n",
	    statuscode[retcode],
	    freshness,
	    num_results,
	    freshness,
	    num_results
	    );
   }else{
     if ( ( response_time > time_warn ) || ( num_results < entry_warn ) ){ 
       retcode = WARNING;
     }
     if ( ( response_time > time_crit ) || ( num_results < entry_crit ) ){
       retcode = CRITICAL;
     }
     printf("%s: time=%.2fs, entries=%d |time=%.2fs;entries=%d\n",
	    statuscode[retcode],
	    response_time,
	    num_results,
	    response_time,
	    num_results
	    );
   }

   /* Close LDAP Connection */
   ldap_msgfree( result ); 
   ldap_unbind( ld ); 
   
   return( retcode ); 

} /* End Main Function */

