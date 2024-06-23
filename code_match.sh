#!/bin/sh

awk -F'\t' -v pattern=$1 '$2 ~ pattern {print $1"\t"$2}' $2
