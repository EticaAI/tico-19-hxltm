#!/bin/sh
# ==============================================================================
#
#          FILE:  data-original-prepare-terminology.sh
#
#         USAGE:  ./scripts/data-original-prepare-terminology.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#                 - rsync
#                 - miller
#                   - See <https://github.com/johnkerl/miller>
#                 - ./scripts/data-original-download.sh
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

# PWD_NOW=$(pwd)
# TMP_DIR="tmp"
# DATA_DIR="data"
DATA_ORIGINAL_DIR="data/original"
DATA_ORIGINAL_GIT_DIR="tmp/original-git"

set -x
rsync --archive --verbose "${DATA_ORIGINAL_GIT_DIR}/data/" "$DATA_ORIGINAL_DIR/"
# set +x


#### terminology/facebook ______________________________________________________
### Copy file ..................................................................
find "$DATA_ORIGINAL_DIR/terminologies/" -name 'f_*' -type f -exec cp "{}" "$DATA_ORIGINAL_DIR/terminology/facebook"  \;

## ls
ls "${DATA_ORIGINAL_DIR}"/terminology/facebook/

### Rename file ................................................................
# data/original/terminology/facebook/f_en-pt_XX.csv -> data/original/terminology/facebook/f-en-pt-XX.csv
for i in "${DATA_ORIGINAL_DIR}"/terminology/facebook/f_en-*; do
  mv "$i" "$(echo "$i" | sed "s/_/-/g")";
done

ls "${DATA_ORIGINAL_DIR}"/terminology/facebook/

# data/original/terminology/facebook/f-en-pt-XX.csv -> data/original/terminology/facebook/en_pt-XX.csv
for i in "${DATA_ORIGINAL_DIR}"/terminology/facebook/f-en-*; do
  mv "$i" "$(echo "$i" | sed "s/f-en-/en_/g")";
done

# data/original/terminology/facebook/en_pt-XX.csv-> data/original/terminology/facebook/en_pt.csv
for i in "${DATA_ORIGINAL_DIR}"/terminology/facebook/*-XX.csv; do
#   echo "$i" "$(echo "$i" | sed "s/-XX.csv/.csv/")";
  mv "$i" "$(echo "$i" | sed "s/-XX.csv/.csv/")";
done

### scripts/patch/data-terminology-facebook.diff: Patch missing DQUOTES ........
# patch --dry-run --verbose --unified -p1 --input=scripts/patch/data-terminology-facebook.diff
patch --verbose --unified -p1 --input=scripts/patch/data-terminology-facebook.diff
# exit 1

## ls
ls "${DATA_ORIGINAL_DIR}"/terminology/facebook/


### Replace content targetLang _ by - ..........................................
# Restrict - language tags delimiter, as per IETF Best Current Practice 47
# and common usage in industry.
# example: 
# '1,en,pt_XX,1918 flu,gripe de 1918' -> '1,en,pt-XX,1918 flu,gripe de 1918'
for i in "${DATA_ORIGINAL_DIR}"/terminology/facebook/*.csv; do
  # shellcheck disable=SC2016
  mlr --csv -I put '$targetLang = gsub($targetLang, "_", "-")' "$i"
done

### Replace content targetLang _ by - ..........................................
# Restrict - language tags delimiter, as per IETF Best Current Practice 47
# and common usage in industry.
# example: 
# '1,en,pt-XX,1918 flu,gripe de 1918' -> '1,en,pt,1918 flu,gripe de 1918'
for i in "${DATA_ORIGINAL_DIR}"/terminology/facebook/*.csv; do
  # shellcheck disable=SC2016
  mlr --csv -I put '$targetLang = gsub($targetLang, "-XX", "")' "$i"
done

### Concatenate Facebook terminology ...........................................
mlr --csv cat "${DATA_ORIGINAL_DIR}"/terminology/facebook/*.csv > "${DATA_ORIGINAL_DIR}"/tico-19-terminology-facebook.csv

# mlr --csv put '$targetLang2 = $targetLang' data/original/terminology/facebook/en_zh-TW.csv
# mlr --csv put '$targetLang = gsub($targetLang, "_", "-")' data/original/terminology/facebook/en_zh-TW.csv
# original/terminology

echo "TODO data/original/terminologies/f_en-es_XX.csv missing data"

#### terminology/google ________________________________________________________

### Copy files .................................................................
find "$DATA_ORIGINAL_DIR/terminologies/" -name 'g_*' -type f -exec cp "{}" "$DATA_ORIGINAL_DIR/terminology/google"  \;

## ls
ls "${DATA_ORIGINAL_DIR}"/terminology/google/

### Rename files ...............................................................

for i in "${DATA_ORIGINAL_DIR}"/terminology/google/g_*; do
#   echo "$i" "$(echo "$i" | sed "s/f_//")";
  mv "$i" "$(echo "$i" | sed "s/g_//")";
done

## ls
ls "${DATA_ORIGINAL_DIR}"/terminology/google/

### Concatenate Facebook terminology
mlr --csv cat "${DATA_ORIGINAL_DIR}"/terminology/google/*.csv > "${DATA_ORIGINAL_DIR}"/tico-19-terminology-google.csv

#### validate __________________________________________________________________

mlr --icsv check data/original/terminology/google/*.csv
mlr --icsv check data/original/terminology/facebook/*.csv

#### Extract unique languages __________________________________________________

### The ones from Google already were good .....................................
mlr --csv --headerless-csv-output cut -f sourceLang data/original/tico-19-terminology-google.csv | sort | uniq > scripts/data-info/tico19_t_google_initial-language-source.csv
mlr --csv --headerless-csv-output cut -f targetLang data/original/tico-19-terminology-google.csv | sort | uniq > scripts/data-info/tico19_t_google_initial-language-target.csv
cat scripts/data-info/tico19_t_google_initial-language-source.csv scripts/data-info/tico19_t_google_initial-language-target.csv | sort | uniq > scripts/data-info/tico19_t_google_initial-languages.csv

# mlr --csv --headerless-csv-output cut -f sourceLang data/original/tico-19-terminology-google.csv | uniq
# mlr --csv --headerless-csv-output cut -f targetLang data/original/tico-19-terminology-google.csv | uniq

### The ones from facebook are poorly labeled ..................................
mlr --csv --headerless-csv-output cut -f sourceLang data/original/tico-19-terminology-facebook.csv | sort | uniq | grep . > scripts/data-info/tico19_t_facebook_initial+hotfixes-language-source.csv
mlr --csv --headerless-csv-output cut -f targetLang data/original/tico-19-terminology-facebook.csv | sort | uniq | grep . > scripts/data-info/tico19_t_facebook_initial+hotfixes-language-target.csv
cat scripts/data-info/tico19_t_facebook_initial+hotfixes-language-source.csv scripts/data-info/tico19_t_facebook_initial+hotfixes-language-target.csv | sort | uniq > scripts/data-info/tico19_t_facebook_initial+hotfixes-languages.csv

# print csvs
# mlr --csv cat data/tico-19-terminology-google.tm2.hxl.csv
# mlr --csv cut -f sourceLang,targetLang data/original/tico-19-terminology-google.csv
### With HXL
# hxlcut --include '#item+rem+linguam_fontem_est,#item+rem+linguam_objectivum_est' data/tico-19-terminology-google.tm2.hxl.csv
#     mlr --csv cut -f sourceLang,targetLang data/tico-19-terminology-google.tm2.hxl.csv

# #### scripts/data-info/tico19_tm_twb_initial-language-pairs.csv ________________
# # Save the languages to CSV file to reuse later
# find data/original/TM/ -iname "all.en-*.zip" \
#   | grep -E '(en-...?.?.?.?).tmx' --only-matching \
#   | sed 's/.tmx//' | grep -v old | sort > scripts/data-info/tico19_tm_twb_initial-language-pairs.csv

# #### scripts/data-info/tico19_tm_twb_initial-languages.csv _____________________

# # cat scripts/data-info/tico19_tm_twb_initial-language-pairs.csv | sed 's/en-//'
# sed 's/en-//' scripts/data-info/tico19_tm_twb_initial-language-pairs.csv > scripts/data-info/tico19_tm_twb_initial-languages-temp.csv
# echo "en" >> scripts/data-info/tico19_tm_twb_initial-languages-temp.csv
set +x
echo "Okay!"