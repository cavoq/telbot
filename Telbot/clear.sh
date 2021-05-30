#!/bin/sh

if [ -e log.txt ]
then
  rm -f log.txt
  echo 'Successfully cleared'
fi
