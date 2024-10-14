# HTTP-UEFI
This is a Python script to host an HTTP server under UEFI for remote testing purposes.
It is built against Python 3.6.8 provided on EDK II.

# Need to know before using it
* Due to the limitation of the UEFI environment,
  
  * Once the server is up and running, the UEFI shell interface is occupied and please interact with UEFI from remote instead.
  
  * The HTTP server communication is synchronous.

  * There is no I/O redirection. The EFI utilities need to output testlog on the UEFI filesystem for later read log command to access the test result.

* The communication protocol is **HTTP** not **HTTPS** and no authentication implemented. That makes it vlunerable to man-in-the-middle attacks, so PLEASE

  do shorten the server running time on a worldwide network, and shutdown the server once your task is completed or
  run the server on the local area network for better security.
  
* It only accepts operations for testing purposes and I have no plan to support UEFI shell commands embedded in HTTP requests at this point. 

# Preparation
* Python 3 enablement on UEFI

  Please refer to https://github.com/tianocore/edk2-libc/blob/master/AppPkg/Applications/Python/Python-3.6.8/Py368ReadMe.txt
        
* Copy the built Python libraries and the **http_uefi.py**  under your UEFI environment

# Files 
* http_uefi.py  
  
  socurce file to host a http server on UEFI 

* install_python_env.nsh  
  
  installation file to install Python environment on UEFI

* startup.nsh

  start up file to auto-run the HTTP server when the server boots up 

* misc  

  others....

# Operation supported and Usage
Assume we set TARGETURL=http://192.168.100.108:8080. The following commands demonstrate a simple test scenario from a test utility upload to the test result retrieval. 
    
* Upload where it creates an `uploads` folder automatically and place the uploaded files

  curl -X POST -H "Content-Type: multipart/form-data" -F "file=@my_wake_test.efi" ${TARGETURL}

* List 

  curl -H "Content-Type: application/json" -X POST --data '{"operation":"listdir","path":"FS0:\\uploads"}' ${TARGETURLi}/listdir

  curl ${TARGETURL}/getfilelist
    
* Run

  curl ${TARGETURL}/run/my_wake_test.efi

* ReadLog

  curl -H "Content-Type: application/json" -X POST --data '{path":"FS0:\\efi\\tools\\my_wake_test.LOG"}' ${TARGETURL}/readlog
    
* Exit The HTTP server

  curl ${TARGETURL}/byehttpuefi

