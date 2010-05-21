#!/bin/bash
cd `dirname $0`
export SB_DIR=`pwd`

cd $SB_DIR
echo "Adding sb paths to python path in site packages"
python_packages=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`

echo "${SB_DIR}/scripts" > external/.conf.d/sb_path.pth
echo "${SB_DIR}/plugins" >> external/.conf.d/sb_path.pth
cp external/.conf.d/sb_path.pth "$python_packages"/sb_path.pth

echo "Running dbs/initDBS.sh with no options"
echo
dbifile=external/dbs/initDBS.sh
echo ${dbifile}:
$dbifile
exit