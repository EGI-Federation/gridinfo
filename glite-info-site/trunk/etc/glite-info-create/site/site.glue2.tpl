dn: GLUE2DomainId=$SITE_NAME,o=glue
objectClass: GLUE2Domain
objectClass: GLUE2AdminDomain
GLUE2DomainId: $SITE_NAME
GLUE2DomainDescription: $SITE_DESC
GLUE2DomainWWW: $SITE_WEB
GLUE2EntityOtherInfo: $OTHERINFO

dn: GLUE2LocationId=location.$SITE_NAME,GLUE2DomainId=$SITE_NAME,o=glue
objectClass: GLUE2Location
GLUE2LocationId: location.$SITE_NAME
GLUE2LocationCountry: $SITE_LOC
GLUE2LocationLatitude: $SITE_LAT
GLUE2LocationLongitude: $SITE_LON
GLUE2LocationDomainForeignKey: $SITE_NAME

dn: GLUE2ContactId=general.contact.$SITE_NAME,GLUE2DomainId=$SITE_NAME,o=glue
objectClass: GLUE2Contact
GLUE2ContactId: general.contact.$SITE_NAME
GLUE2ContactDetail: mailto:$SITE_EMAIL
GLUE2ContactType: general
GLUE2ContactDomainForeignKey: $SITE_NAME

dn: GLUE2ContactId=security.contact.$SITE_NAME,GLUE2DomainId=$SITE_NAME,o=glue
objectClass: GLUE2Contact
GLUE2ContactId: security.contact.$SITE_NAME
GLUE2ContactDetail: mailto:$SITE_SECURITY_EMAIL
GLUE2ContactType: security
GLUE2ContactDomainForeignKey: $SITE_NAME

dn: GLUE2ContactId=sysadmin.contact.$SITE_NAME,GLUE2DomainId=$SITE_NAME,o=glue
objectClass: GLUE2Contact
GLUE2ContactId: sysadmin.contact.$SITE_NAME
GLUE2ContactDetail: mailto:$SITE_EMAIL
GLUE2ContactType: sysadmin
GLUE2ContactDomainForeignKey: $SITE_NAME

dn: GLUE2ContactId=usersupport.contact.$SITE_NAME,GLUE2DomainId=$SITE_NAME,o=glue
objectClass: GLUE2Contact
GLUE2ContactId: usersupport.contact.$SITE_NAME
GLUE2ContactDetail: mailto:$SITE_SUPPORT_EMAIL
GLUE2ContactType: usersupport
GLUE2ContactDomainForeignKey: $SITE_NAME

