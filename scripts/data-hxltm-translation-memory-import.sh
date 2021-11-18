#!/bin/sh
# ==============================================================================
#
#          FILE:  data-hxltm-translation-memory-import.sh
#
#         USAGE:  ./scripts/data-hxltm-translation-memory-import.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#                 - hxltm
#                   - pip install hxltm-eticaai
#                 - ./scripts/data-original-download.sh
#                 - ./scripts/data-original-prepare.sh
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-18 02:51 UTC started
# ==============================================================================
set -e

# PWD_NOW=$(pwd)
# TMP_DIR="tmp"
# DATA_DIR="data"
DATA_ORIGINAL_DIR="data/original"
DATA_ORIGINAL_GIT_DIR="tmp/original-git"

TMX_OUT_ALL_DIR="${DATA_ORIGINAL_DIR}/translation-memory/translators-without-borders/all"
# data/original/translation-memory/translators-without-borders/all/en-pt-BR.tmx
# "en-pt-BR" list from scripts/data-info/tico19_tm_twb_initial-language-pairs.csv


set -x
# TODO: extract also <prop type="note">
# hxltmdexml --agendum-linguam en-Latn@en data/original/translation-memory/translators-without-borders/all/en-pt-BR.tmx

# hxltmdexml
set +x
echo "Okay!"