echo Welcome to HTTP over UEFI
echo Please ensure network interface is configured correctly.(Default: eth0)

echo Enabling network interface eth0
ifconfig -s eth0 dhcp
stall 5000000
FS0:
echo Initializing HTTP over UEFI
python EFI\tools\http_uefi.py

# Check if the EFI file executed successfully
#if %lasterror% == 0 then
#    echo "EFI file executed successfully."
#else
#    echo "Error occurred while running the EFI file."
#endif

