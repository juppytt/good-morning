#!/bin/bash -e
cp *.csv backup/
pushd backup
    git add *.csv
    git commit -m "[BACKUP]"
    git push
popd

