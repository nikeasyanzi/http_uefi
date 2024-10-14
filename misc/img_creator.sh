#!/usr/bin/env bash
set -x
set -e
SCRIPT_PATH=$(readlink -f "$(dirname "${BASH_SOURCE[0]}")")

MOUNT_PATH=${SCRIPT_PATH}/img_mount
IMG=${SCRIPT_PATH}/myfs.img
#EDK2 build output
DATA=../output/*

if test -t 1 && test $(tput colors) -ge 8; then
	C_RED='\033[1;31m'
	C_GREEN='\033[1;32m'
	C_BLUE='\033[1;34m'
	C_YELLOW='\033[1;33m'
	C_CYAN='\033[1;36m'
	NC='\033[0;00m'
fi

arg_parse() {
	while true; do
		[[ $1 == "" ]] && break
		case $1 in
		-h | --help)
			help
			exit
			;;
		-i | --ip)
			IPADDR=$2
			;;
		*)
			echo "Invalid command, please follow instructions"
			help
			exit
			;;
		esac
		shift 2
	done
}

main() {
	#arg_parse "$@"

	#env_check

	dd if=/dev/zero of=${IMG} bs=1024 count=102400
	mkfs.vfat -F 32 -v ${IMG}

	mkdir -p ${MOUNT_PATH}
	sudo mount -o loop ${IMG} ${MOUNT_PATH}
	sudo cp -r ${DATA} ${MOUNT_PATH}
	sudo umount ${MOUNT_PATH}
	rm -rf ${MOUNT_PATH}

	return 0
}

main "$@"
