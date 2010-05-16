#/bin/bash

cd config
python initConfig.py 
cd ../music
echo 'Initializing music db with reset-all'
python initMusic.py --reset-all

exit 1