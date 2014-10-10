#!/bin/sh

PROJECT=YaH3C-mini-osx
TARGET=~/local/$PROJECT

cd ..
rm -Rf $TARGET
mkdir -p $TARGET/scripts
cp -R ./$PROJECT/scripts/*.py $TARGET/scripts/
cp ./$PROJECT/README.md ./$PROJECT/yah3c.py $TARGET/