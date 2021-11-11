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
#  REQUIREMENTS:  ---
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

TMP_DIR="tmp"
DATA_DIR="data"
DATA_ORIGINAL_DIR="data-original"

rsync -a "${TMP_DIR}/tico-19.github.io-master/data/" "$DATA_ORIGINAL_DIR/"

if [ ! -d "${DATA_ORIGINAL_DIR}/terminology" ]; then
    mkdir "${DATA_ORIGINAL_DIR}/terminology"
    # echo "todo"
fi

# if [ ! -d "${DATA_ORIGINAL_DIR}/terminology/google" ]; then
    mkdir "${DATA_ORIGINAL_DIR}/terminology/google"
    tmpdir1=$(mktemp --directory tmp.XXXXXXXXXX )
    echo "$tmpdir1"
    ls -l "$tmpdir1"
    rsync -a "${DATA_ORIGINAL_DIR}/terminologies/" --include='g_*' --exclude='*' "$tmpdir1"
    # cp -r "${DATA_ORIGINAL_DIR}/data/terminologies/g_*" "$tmpdir1"
    ls -l "$tmpdir1"

    echo "todo"
# fi

if [ ! -d "${DATA_ORIGINAL_DIR}/terminology/facebook" ]; then
    mkdir "${DATA_ORIGINAL_DIR}/terminology/facebook"
    echo "todo"
fi

