#!/bin/sh
#get sites list
echo 'List of registered sites:'
curl http://localhost:5000/sites/ -v --silent
echo "\r ========================= \r"

#create site
echo 'Create site:'
SITE_ID="$(curl http://localhost:5000/sites/ -X POST -d 'url=http://cthtuf.name' --silent)"
echo "Created site id is $SITE_ID"
echo "\r ========================= \r"

echo 'Delete site'
echo "$(curl http://localhost:5000/site/1/ -X DELETE -v --silent)"
echo "\r ========================= \r"

echo "Get site $SITE_ID data"
echo "$(curl http://localhost:5000/site/$SITE_ID/ --silent)"
echo "\r ========================= \r"

echo "Get site $SITE_ID rules"
echo "$(curl http://localhost:5000/site/$SITE_ID/rules/ -v --silent)"
echo "\r ========================= \r"

echo "Add rules to site $SITE_ID"
echo "$(curl http://localhost:5000/site/$SITE_ID/rules/ -X POST -d 'title=true&favicon=false' -v --silent)"
echo "\r ========================= \r"

echo "Get site $SITE_ID rules"
echo "$(curl http://localhost:5000/site/$SITE_ID/rules/ -v --silent)"
echo "\r ========================= \r"

echo "Check new site"
echo "$(curl http://localhost:5000/site/$SITE_ID/check/ --silent)"
echo "\r ========================= \r"

echo "Get site rule 'favicon'"
echo "$(curl http://localhost:5000/site/$SITE_ID/rule/favicon/ --silent)"
echo "\r ========================= \r"

echo "Change site rule"
echo "$(curl http://localhost:5000/site/$SITE_ID/rules/ -X PUT -d 'favicon=lala&meta=ls' -v --silent)" 
echo "\r ========================= \r"

echo "Delete site rule"
echo "$(curl http://localhost:5000/site/$SITE_ID/rule/title/ -X DELETE --silent -v)"
echo "\r ========================= \r"

echo "Get site rules"
echo "$(curl http://localhost:5000/site/$SITE_ID/rules/ --silent)"