# HTTP-UEFI
This is a Python script to host an HTTP server under UEFI for remote testing purposes.

It is built against Python 3.6.8 provided on EDK II.

It supports operations such as file upload, test utility run, and log read to facilitate the testing process.

![Pasted Image 20250430133431_772](https://github.com/user-attachments/assets/58de799a-e0aa-4f22-a917-d70ed9d609fc)


# Need to know before using it
## Manual run
* Due to the limitation of the UEFI environment,
  
  * Once the server is up and running, the user can only interact with UEFI from HTTP, and UEFI shell interface is override.
  
  * The HTTP server communication is synchronous.

  * There is no I/O redirection. The EFI utilities must output test logs on the UEFI filesystem for later read commands to access the test result.

* Security
  The communication protocol is **HTTP** not **HTTPS** and no authentication is implemented. That makes it vulnerable to man-in-the-middle attacks,
  so PLEASE stop the service once your task is completed
    
* It only accepts operations for testing purposes and I have no plan to support UEFI shell commands embedded in HTTP requests at this point.
  
## Auto run the HTTP server when enter UEFI
* Work with the `startup.nsh`, we can make UEFI to execute the HTTP binary once it enters the shell envoriment.
* If you want to stop the HTTP server and return the shell environment, please emit exit command to the HTTP server

# How to use
* Copy the built Python libraries which are folders Tools and StdLib and the **http_uefi.py** in this repo  under your UEFI environment
  
  For Python 3 enablement on UEFI, please refer to https://github.com/tianocore/edk2-libc/releases/tag/v3.6.8.1 provided by [Jayaprakash Nevara](https://github.com/jpshivakavi)

  If you want to build by yourself, please refer to https://github.com/tianocore/edk2-libc/blob/master/AppPkg/Applications/Python/Python-3.6.8/Py368ReadMe.txt
  
  ![image](https://github.com/user-attachments/assets/fc159642-bf84-459d-9dc5-f14ddd33a695)

* Run the HTTP server
  
  ![image](https://github.com/user-attachments/assets/7804dceb-4bbc-45eb-bb9f-10cc0191c11f)

# Files 
* http_uefi.py  
  
  socurce file to host a http server on UEFI
  
* install_python_env.nsh  
  
  installation file to install Python environment on UEFI

* startup.nsh

  start up file to auto-run the HTTP server when the server boots up 

* curl_test.sh
  
  A simple example demonstrating how to write up your test suit logic 

* misc  

  others....

# Operation supported and Usage
Assume we set TARGETURL=http://192.168.100.108:8080. The following commands demonstrate a simple test scenario from a test utility upload to the test result retrieval. 
    
* Upload where it creates an `uploads` folder automatically and place the uploaded files

  curl -X POST -H "Content-Type: multipart/form-data" -F "file=@my_wake_test.efi" ${TARGETURL}

* List dir with the custom path 

  curl -H "Content-Type: application/json" -X POST --data '{"operation":"listdir","path":"FS0:\\uploads"}' ${TARGETURLi}/listdir

  curl ${TARGETURL}/getfilelist
    
* Run the efi test utility

  curl ${TARGETURL}/run/my_wake_test.efi

* Read log with the customized path

  curl -H "Content-Type: application/json" -X POST --data '{path":"FS0:\\efi\\tools\\my_wake_test.LOG"}' ${TARGETURL}/readlog
    
* Exit the HTTP server and return ownership to UEFI Shell 

  curl ${TARGETURL}/byehttpuefi

