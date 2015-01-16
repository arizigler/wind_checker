#!/bin/bash
cd ~/workspace
if [  -f ./new_report ]; then rm ./new_report; fi
if [  -f ./raw_report ]; then rm ./raw_report; fi
if [  -f ./final_report ]; then rm ./final_report; fi
if [  -f ./.tmp_results ]; then rm ./.tmp_results; fi
reset=0
is_time=$(./check_time.py && echo $?)
if [ $is_time == 1 ]; then rm -f ./morning; exit 1; fi
if [[ $is_time == 0 && ! -f ./morning ]]; then reset=1; touch morning; fi
node server.js >> raw_report
#cat raw_report | grep -v "N/A"  | cut -f 2,4 >> new_report
cat raw_report |  cut -f 4 | cut -d ' ' -f 1 >> new_report
if [[ $reset == 1 ]]; then rm -f last_report max_report; cat new_report | awk '{print 0}' >> last_report; cat last_report >> max_report; fi
awk 'FNR==NR{a[FNR""]=$0; next}{if ($0 > a[FNR""]) {print $0;} else print a[FNR""] }' max_report new_report >> _max_report
mv _max_report max_report
awk 'FNR==NR{a[FNR""]=$0; next}{if ($0 > 8) {print $0-a[FNR""];} else print -1 }' max_report new_report >> .tmp_results
awk 'FNR==NR{if ($0 == 0) {a[FNR""]=1;} next}{if (a[FNR""]==1) {print $0;}}' .tmp_results raw_report > final_report
#diff new_report last_report >> /dev/null
if [[ $is_time == 0 && $(cat final_report | grep -v "N/A" | wc -l) != 0 ]]; then
    date >> wind.log;
    ./send_mail.py ariz@shaldag.biz ariz@shaldag.biz "$(cat final_report | grep -v 'N/A')" >> wind.log;
    mv new_report last_report;
fi


