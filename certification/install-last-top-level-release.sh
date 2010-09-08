#!/bin/bash

wget http://grid-deployment.web.cern.ch/grid-deployment/glite/repos/3.2/glite-BDII.repo -O /etc/yum.repos.d/glite-BDII.repo 
yum install -y glite-BDII

MY_DOMAIN=$(hostname -d)
MY_HOST=$(hostname -f)

# Create site-info.def
cat <<EOF > /root/site-info.def 
SITE_NAME="Test Site"
BDII_HOST=${MY_HOST}

EOF
    
/opt/glite/yaim/bin/yaim -c -s /root/site-info.def -n BDII_top
