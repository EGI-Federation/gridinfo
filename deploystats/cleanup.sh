#!/bin/bash
tidy -xml -i -q -o deploystats.xml deploystats.xml
echo "Now view: deploystats.xml"
cat deploystats.xml
