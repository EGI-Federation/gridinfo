#!/bin/bash
repo='http://grid-deployment.web.cern.ch/grid-deployment/glite/repos/3.2/glite-BDII_top.repo'
wget ${repo} -O /etc/yum.repos.d/glite-BDII_top.repo 
yum install -y glite-BDII_top

MY_DOMAIN=$(hostname -d)
MY_HOST=$(hostname -f)

# Create site-info.def
cat <<EOF > /root/site-info.def 
SITE_NAME="Test Site"
BDII_HOST=${MY_HOST}

EOF
    
/opt/glite/yaim/bin/yaim -c -s /root/site-info.def -n BDII_top
