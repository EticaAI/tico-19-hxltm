#!/bin/sh
# ==============================================================================
#
#          FILE:  data-original-prepare.sh
#
#         USAGE:  ./scripts/data-original-prepare.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - rename
#                 - rsync
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-11 16:63 UTC started
# ==============================================================================
set -e

PWD_NOW=$(pwd)
TMP_DIR="tmp"
DATA_DIR="data"
DATA_ORIGINAL_DIR="data/original"
DATA_ORIGINAL_GIT_DIR="tmp/original-git"

set -x
rsync --archive --verbose "${DATA_ORIGINAL_GIT_DIR}/data/" "$DATA_ORIGINAL_DIR/"
# set +x


# cd "$DATA_ORIGINAL_DIR/terminologies"
# pwd

# Copy
find "$DATA_ORIGINAL_DIR/terminologies/" -name 'f_*' -type f -exec cp "{}" "$DATA_ORIGINAL_DIR/terminology/facebook"  \;

# Rename
# find "$DATA_ORIGINAL_DIR/terminology/facebook/" -name 'f_*' -type f -exec ls "{}"  \;

# rename 's/f_//' "$DATA_ORIGINAL_DIR/terminology/facebook/*.csv"

# find "$DATA_ORIGINAL_DIR/terminology/facebook/" -name 'f_*' -type f -exec rename 's/f_//_' "{}"  \;


# echo 'oi'
# find f_* -type f | sed -n "s/f_//" | xargs print
# echo 'bye'
# echo 'oi2'
# find f_* -type f -exec sed -n "s/f_//" {} \;
# echo 'bye2'
# echo 'oi2'
# find ./ -type f -exec sed -i -e 's/f_//g' {} \;
# echo 'bye2'
# find f_* -type f  -print0
# # ecfind f_* -type f  -print0 | xargs --null -I{} mv {} {}_renamed
# echo 'bye3'



# find . -type f |
# sed -n "s/\(.*\)factory\.py$/& \1service\.py/p" |
# xargs -p -n 2 mv

# for


# if [ ! -d "${DATA_ORIGINAL_DIR}/terminology" ]; then
#     mkdir "${DATA_ORIGINAL_DIR}/terminology"
#     # echo "todo"
# fi

# # if [ ! -d "${DATA_ORIGINAL_DIR}/terminology/google" ]; then
#     mkdir "${DATA_ORIGINAL_DIR}/terminology/google"
#     tmpdir1=$(mktemp -d --tmpdir -t "tmp.XXXXXXXXXX" )
#     echo "$tmpdir1"
#     ls -l "$tmpdir1"
#     # rsync -a "${DATA_ORIGINAL_DIR}/terminologies/" --include='g_*' --exclude='*' "$tmpdir1"
#     # cp -r "${DATA_ORIGINAL_DIR}/data/terminologies/g_*" "$tmpdir1"
#     ls -l "$tmpdir1"
#     pwd "$tmpdir1"

#     echo "todo"
# # fi

# if [ ! -d "${DATA_ORIGINAL_DIR}/terminology/facebook" ]; then
#     mkdir "${DATA_ORIGINAL_DIR}/terminology/facebook"
#     echo "todo"
# fi

