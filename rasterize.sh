#!/bin/bash

if [ -z "$1" ]
    then
        input_file='out.svg'
    else
        input_file=$1
fi

if [ -z "$2" ]
    then
        output_file='out.png'
    else
        output_file=$2
fi

inkscape -z -f $input_file -j -e $output_file
