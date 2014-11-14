#!/bin/sh

PROJECT=YaH3C-mini-osx
TARGET=~/local/$PROJECT

rm -Rf $TARGET
mkdir -p $TARGET/scripts
cp -R ./scripts/*.py $TARGET/scripts/
cp ./README.md ./yah3c.py $TARGET/