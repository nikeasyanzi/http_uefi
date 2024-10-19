#!/usr/bin/env bash

set -x
echo "Run this script to test the http server over UEFI"
echo "Currenly, HTTPS is not supported!!"
TARGETURL=http://192.168.100.108:8080

#Test file upload
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@my_wake.efi" ${TARGETURL}

#Test list dir with the custom path 
curl -H "Content-Type: application/json" -X POST --data '{"path":"FS0:\\efi\\tools\\uploads"}' ${TARGETURL}/listdir

#Test run the efi test utility
curl ${TARGETURL}/run/my_wake.efi

#Test log read with the customized path
curl -H "Content-Type: application/json" -X POST --data '{"path":"FS0:\\syslinux.cfg"}' ${TARGETURL}/readlog

#Exit the server and return ownership to UEFI Shell 
curl ${TARGETURL}/byehttpuefi

