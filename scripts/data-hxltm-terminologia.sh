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
#                 - libhxl
#                 - ./scripts/data-original-download.sh
#                 - ./scripts/data-original-prepare-terminology.sh
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
  --map='sourceLang #item+rem+linguam_fontem_est+v_bcp47' \
  --map='targetLang #item+rem+linguam_objectivum_est+v_bcp47' \
  --map='pos #item+rem+linguam_fontem+partem_orationis' \
  --map='description #item+rem+definitionem+i_mul+ii_zyyy' \
  --map='sourceString #item+rem+linguam_fontem+terminum' \
  --map='targetString #item+rem+linguam_objectivum+terminum' \
  data/original/tico-19-terminology-google.csv \
  data/tico-19-terminology-google.tm2.hxl.csv

# id,sourceLang,targetLang,sourceString,targetString
# TODO: decide better tagging conventions
hxltag --default-tag='#meta' \
  --map='id #item+conceptum+codicem' \
  --map='sourceLang #item+rem+linguam_fontem_est+v_bcp47' \
  --map='targetLang #item+rem+linguam_objectivum_est+v_bcp47' \
  --map='sourceString #item+rem+linguam_fontem+terminum' \
  --map='targetString #item+rem+linguam_objectivum+terminum' \
  data/original/tico-19-terminology-facebook.csv \
  data/tico-19-terminology-facebook.tm2.hxl.csv

set +x
echo "Okay!"