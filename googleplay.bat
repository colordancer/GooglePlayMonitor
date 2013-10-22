@echo off
java -jar googleplay.jar -f crawler.conf list TOOLS -s apps_topselling_free -n 100 -o 0
@pause