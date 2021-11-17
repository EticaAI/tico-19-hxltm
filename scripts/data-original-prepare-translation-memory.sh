#!/bin/sh
# ==============================================================================
#
#          FILE:  data-original-prepare-translation-memory.sh
#
#         USAGE:  ./scripts/data-original-prepare-translation-memory.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#                 - rsync
#                 - xmllint
#                   - See <http://xmlsoft.org/>
#                   - sudo apt  install libxml2-utils
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-17 05:46 UTC started
# ==============================================================================
set -e

# PWD_NOW=$(pwd)
# TMP_DIR="tmp"
# DATA_DIR="data"
DATA_ORIGINAL_DIR="data/original"
DATA_ORIGINAL_GIT_DIR="tmp/original-git"

TMX_DIR_IN="${DATA_ORIGINAL_DIR}/TM/"
TMX_OUT_ALL_DIR="${DATA_ORIGINAL_DIR}/translation-memory/translators-without-borders/all"

set -x
rsync --archive --verbose "${DATA_ORIGINAL_GIT_DIR}/data/" "$DATA_ORIGINAL_DIR/"
# set +x

# is this empty???
# cp "${DATA_ORIGINAL_DIR}/TM/all.en_ckb.tmx" "${DATA_ORIGINAL_DIR}/translation-memory/translators-without-borders/all/"


unzip "${TMX_DIR_IN}/all.am-om.tmx.zip" -d "${TMX_OUT_ALL_DIR}/"

xmllint --format data/original/translation-memory/translators-without-borders/all/all.am-om.tmx

echo "Okay!"