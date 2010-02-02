Application:  gLite Info Static Create
Authors:      David.Horat@cern.ch
              Laurence.Field@cern.ch
Version:      0.1 (02/02/2010)
********************************************************************

DESCRIPTION
This application allows the system administrators and developers to create
static information in LDIF format for the BDII.


USAGE
Edit the corresponding .cfg file for your use case and fill in the parameters
needed. Then invoke the application with the module name. E.g.:

./glite-info-static-create.sh site

The resulting LDIF files will be created in the output/ directory.


CORE STRUCTURE
  glite-info-static-create.sh   The main script to invoke
  README.txt                    This file
  usage.txt                     The usage file printed in the script's help
  ChangeLog.txt                 Change log for each version


MODULE STRUCTURE
  [name]/
    [name].1.cfg                Config file to be filled out by the sysadmin
    [name].glue.ifc             Interface to comply with GLUE standard
    [name].wlcg.ifg             Interface to comply with WLCG standard
    [name].glue1.tpl            Template to create an LDIF for GLUE 1.3
    [name].glue2.tpl            Template to create an LDIF for GLUE 2.0


TODO
There are several improvements that could be done:
- Use getops and parse more arguments (template name, cfg file path, etc.)
- Improve script error handling and do more existence checks
- Be able to use several .cfg files in one invocation
- Package it into several RPMs (one for core and one per module)
- Create documentation on howto create a new module


CHANGELOG
0.1 (02/02/2010):
  - First draft
  
