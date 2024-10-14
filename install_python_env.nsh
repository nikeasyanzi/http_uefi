map -r 

rm -q FS1:\efi\Tools
rm -q FS1:\efi\StdLib
cp -r FS0:\efi\Tools FS1:\efi
cp -r FS0:\efi\StdLib FS1:\efi
