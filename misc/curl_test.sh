#!/usr/bin/env bash

set -x
echo "Run this script to test the http server over UEFI"
echo "Currenly, HTTPS is not supported!!"
TARGETURL=http://192.168.100.108:8080
#TARGETURL=http://localhost:8080
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@rtc_wake.efi" ${TARGETURL}
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@http_uefi.py" ${TARGETURL}
curl -H "Content-Type: application/json" -X POST --data '{"operation":"listdir","path":"FS0:"}' ${TARGETURL}
curl -H "Content-Type: application/json" -X POST --data '{"operation":"listdir","path":"FS0:\\uploads"}' ${TARGETURL}
curl ${TARGETURL}/run/rtc_wake.efi
sleep 300
curl ${TARGETURL}/byehttpuefi
exit
curl -H "Content-Type: application/json" -X POST --data '{"operation":"readlog","path":"FS0:\\efi\\tools\\RTC_WAKE.LOG"}' ${TARGETURL}

exit

curl ${TARGETURL}/getfilelist
echo
curl ${TARGETURL}/getloglist
echo
#curl -X POST -H "Content-Type: multipart/form-data" -F "file=@test_helloworld.py" ${TARGETURL}
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@Hello.efi" ${TARGETURL}
echo
curl ${TARGETURL}/getfilelist
echo
#curl ${TARGETURL}/run/test_helloworld.py
curl ${TARGETURL}/run/Hello.efi
echo
curl ${TARGETURL}/getloglist
echo
curl ${TARGETURL}/readlog/helloworld_log
exit
echo "Test not exist case"
curl ${TARGETURL}/run/test_helloworld_not_exist.py
curl ${TARGETURL}/readlog/helloworld_log_not_exist

