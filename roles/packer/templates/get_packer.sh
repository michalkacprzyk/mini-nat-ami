#!/bin/bash
# mk (c) 2018
# Downloads (and checks) the latest version of packer
set -x -e -o pipefail

TARGET="{{ packer_dir }}"

LATEST=$( curl --silent "{{ download_url }}" | grep --only-matching "https.*linux_amd64\.zip" )
SHASUMS=$( curl --silent "{{ download_url }}" | grep --only-matching "https.*SHA256SUMS\"" )
SHASUMS=${SHASUMS:0:-1}
SHASIG=$( curl --silent "{{ download_url }}" | grep --only-matching "https.*SHA256SUMS\.sig" )

mkdir -p ${TARGET}
#rm ${TARGET}/*
cd ${TARGET}
wget ${LATEST}
wget ${SHASUMS}
wget ${SHASIG}

gpg --keyserver "{{ keyserver_hkp }}" --recv-keys "{{ pgp_key_id }}"
gpg --verify *_SHA256SUMS.sig *_SHA256SUMS 2>&1 | grep "{{ pgp_fingerprint }}"

cat *_SHA256SUMS | grep linux_amd64.zip > linux_SHA256SUM
shasum -a 256 -c linux_SHA256SUM

unzip -o *.zip
