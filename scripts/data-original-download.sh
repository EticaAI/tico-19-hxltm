#!/bin/sh
# ==============================================================================
#
#          FILE:  data-original-download.sh
#
#         USAGE:  ./scripts/data-original-download.sh
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
#       CREATED:  2021-11-11 15:25 UTC started
# ==============================================================================

TMP_DIR="./tmp"
DATA_DIR="./data"
DATA_ORIGINAL_DIR="./data-original"

# wget https://github.com/tico-19/tico-19.github.io/archive/refs/heads/master.zip

if [ ! -f ${TMP_DIR}/tico-19.github.io.zip ]; then
  curl -L "https://github.com/tico-19/tico-19.github.io/archive/refs/heads/master.zip" \
    --output "${TMP_DIR}/tico-19.github.io.zip"
fi

unzip "${TMP_DIR}/tico-19.github.io.zip" -d "$TMP_DIR"
# unzip "${TMP_DIR}/tico-19.github.io.zip" -d "$DATA_ORIGINAL_DIR"
# unzip "${TMP_DIR}/tico-19.github.io.zip" "tico-19.github.io-master/data/*" -d "$DATA_ORIGINAL_DIR"
# unzip myfile.zip -d "some directory"
# rm -f myfile.zip