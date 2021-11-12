#!/bin/sh
# ==============================================================================
#
#          FILE:  data-hxltm-terminologia.sh
#
#         USAGE:  ./scripts/data-hxltm-terminologia.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#                 - rsync
#                 - miller
#                   - See <https://github.com/johnkerl/miller>
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-12 01:22 UTC started
# ==============================================================================
set -e

# PWD_NOW=$(pwd)
# TMP_DIR="tmp"
# DATA_DIR="data"
DATA_ORIGINAL_DIR="data/original"
DATA_ORIGINAL_GIT_DIR="tmp/original-git"

set -x

# hxltag --default-tag=#meta --map 'stringID' '#item+conceptum+codicem' data/original/tico-19-terminology-google.csv
# hxltag --default-tag=#meta --map='stringID #item+conceptum+codicem' data/original/terminology/google/en_es-419.csv
# stringID,sourceLang,targetLang,pos,description,sourceString,targetString

# TODO: decide better tagging conventions
hxltag --default-tag='#meta' \
  --map='stringID #item+conceptum+codicem' \
  --map='sourceLang #item+rem2+fontem+linguam+v_bcp47' \
  --map='targetLang #item+rem2+objectivum+linguam+v_bcp47' \
  --map='pos #item+rem2+fontem+partem_orationis' \
  --map='description #item+rem2+definitionem+i_mul+ii_zyyy' \
  --map='sourceString #item+rem2+fontem+terminum' \
  --map='targetString #item+rem2+objectivum+terminum' \
  data/original/tico-19-terminology-google.csv \
  data/tico-19-terminology-google.tm2.hxl.csv

# id,sourceLang,targetLang,sourceString,targetString
# TODO: decide better tagging conventions
hxltag --default-tag='#meta' \
  --map='id #item+conceptum+codicem' \
  --map='sourceLang #item+rem2+fontem+linguam+v_bcp47' \
  --map='targetLang #item+rem2+objectivum+linguam+v_bcp47' \
  --map='sourceString #item+rem2+fontem+terminum' \
  --map='targetString #item+rem2+objectivum+terminum' \
  data/original/tico-19-terminology-facebook.csv \
  data/tico-19-terminology-facebook.tm2.hxl.csv

echo "Okay!"