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
#                 - xmlstarlet
#                   - sudo apt  install xmlstarlet
#                 - ./scripts/data-hxltm-prepare.sh
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
DEBUG="1"
EXPLAIN="1"

TMX_DIR_IN="${DATA_ORIGINAL_DIR}/TM/"
TMX_OUT_ALL_DIR="${DATA_ORIGINAL_DIR}/translation-memory/translators-without-borders/all"

# set -x
rsync --archive --verbose "${DATA_ORIGINAL_GIT_DIR}/data/" "$DATA_ORIGINAL_DIR/"
# set +x

# TODO: is this empty??? Some data may be redundant on source material.
#       Leaving here to maybe cite later
#        cp "${DATA_ORIGINAL_DIR}/TM/all.en_ckb.tmx" "${DATA_ORIGINAL_DIR}/translation-memory/translators-without-borders/all/"

#######################################
# Extract, validate (TMX syntax only), and export formated TMX.
# Example:
#    tmx_tuv_langs_sorted path/to/file.tmx
# Requires:
#   xmlstarlet
# Globals:
#   None
# Arguments:
#   tmx_file    Path to a TMX file on the disk.
#######################################
tmx_tuv_langs_unique() {
    # xmlstarlet select --template --value-of /tmx/body/tu/tuv/@xml:lang data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx
    xmlstarlet select --template --value-of /tmx/body/tu/tuv/@xml:lang "$1" | sort | uniq | xargs echo
}

#######################################
# Extract, validate (TMX syntax only), and export formated TMX.
# Globals:
#   TMX_OUT_ALL_DIR
#   TMX_DIR_IN
#   DEBUG
#   EXPLAIN
# Arguments:
#   non-standard-lang-pair  Language pair string, _as it is_, on TICO-19
#######################################
tico19_tmx_extract() {
    tmx_source_zip="${TMX_DIR_IN}/all.$1.tmx.zip"
    tmx_source_unziped="${TMX_OUT_ALL_DIR}/all.$1.tmx"
    tmx_formated_and_linted="${TMX_OUT_ALL_DIR}/$1.tmx"

    test -n "$EXPLAIN" && echo "> tico19_tmx_extract $1"

    # echo "$1"
    if [ ! -f "$tmx_formated_and_linted" ]; then
        unzip "$tmx_source_zip" -d "${TMX_OUT_ALL_DIR}/"

        xmllint --dtdvalid scripts/dtd/tmx14.dtd --noout "$tmx_source_unziped"
        test -n "$EXPLAIN" && echo "  >> TMX source syntax valid"

        xmllint --format "$tmx_source_unziped" > "$tmx_formated_and_linted"

        rm "${TMX_OUT_ALL_DIR}/all.$1.tmx"
    else
        # Already okay, nothing to do
        test -n "$DEBUG" && echo "  >> unzip + xmllint --dtdvalid already done"
    fi


    xmllint --dtdvalid scripts/dtd/tmx14.dtd --noout "$tmx_formated_and_linted"
    test -n "$EXPLAIN" && echo "  >> TMX linted syntax valid"

    if [ -n "$EXPLAIN" ]; then
        langs_all=$(tmx_tuv_langs_unique "$tmx_formated_and_linted")
        echo "  >> TMX languages <tuv> xml:lang: $langs_all"
        # echo "  >> TMX languages <tuv> xml:lang: $langs"
    fi
}


# From The benchmark includes 30 documents  translated from English into 37 languages: 

# From https://tico-19.github.io/memories.html at 2021-11-17, 37 languages
#    document.querySelectorAll('table th').forEach(function(el){console.log(el.innerHTML)})
# Amharic, Arabic (Modern Standard), Bengali, Chinese (Simplified), Dari, Dinka, Farsi, French (European), Hausa, Hindi, Indonesian, Kanuri, Khmer (Central), Kinyarwanda, Kurdish Kurmanji, Kurdish Sorani, Lingala, Luganda, Malay, Marathi, Myanmar, Nepali, Nigerian Fulfulde, Nuer, Oromo, Pashto, Portuguese (Brazilian), Russian, Somali, Spanish (Latin American), Swahili, Tagalog, Tamil, Ethiopian Tigrinya, Eritrean Tigrinya, Urdu, Zulu.
# find data/original/TM/ -iname all.en-*.zip | grep -E '(en-...?.?.?.?).tmx' --only-matching | sed 's/.tmx//' | grep -v old | sort | xargs printf '\ntico19_tmx_extract "%s"'

tico19_tmx_extract "en-ar"
tico19_tmx_extract "en-bn"
tico19_tmx_extract "en-ckb"
tico19_tmx_extract "en-din"
tico19_tmx_extract "en-es-LA"
tico19_tmx_extract "en-fa"
tico19_tmx_extract "en-fr"
tico19_tmx_extract "en-fuv"
tico19_tmx_extract "en-ha"
tico19_tmx_extract "en-hi"
tico19_tmx_extract "en-id"
tico19_tmx_extract "en-km"
tico19_tmx_extract "en-kr"
tico19_tmx_extract "en-ku"
tico19_tmx_extract "en-lg"
tico19_tmx_extract "en-ln"
tico19_tmx_extract "en-mr"
tico19_tmx_extract "en-ms"
tico19_tmx_extract "en-my"
tico19_tmx_extract "en-ne"
tico19_tmx_extract "en-nus"
tico19_tmx_extract "en-om"
tico19_tmx_extract "en-prs"
tico19_tmx_extract "en-ps"
tico19_tmx_extract "en-pt-BR"
tico19_tmx_extract "en-ru"
tico19_tmx_extract "en-rw"
tico19_tmx_extract "en-so"
tico19_tmx_extract "en-sw"
tico19_tmx_extract "en-ta"
tico19_tmx_extract "en-ti"
tico19_tmx_extract "en-ti_ER"
tico19_tmx_extract "en-ti_ET"
tico19_tmx_extract "en-tl"
tico19_tmx_extract "en-ur"
tico19_tmx_extract "en-zh"
tico19_tmx_extract "en-zu"


./scripts/fn_tico19_datainfo_tmx.py "csv-header" > scripts/data-info/tico19_tm.csv

# find data/original/TM/ -iname all.en-*.zip | grep -E '(en-...?.?.?.?).tmx' --only-matching | sed 's/.tmx//' | grep -v old | sort | xargs printf '\n./scripts/fn_tico19_datainfo_tmx.py "%s" >> scripts/data-info/tico19_tm.csv'

./scripts/fn_tico19_datainfo_tmx.py "en-ar" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-bn" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ckb" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-din" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-es-LA" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-fa" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-fr" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-fuv" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ha" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-hi" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-id" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-km" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-kr" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ku" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-lg" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ln" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-mr" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ms" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-my" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ne" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-nus" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-om" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-prs" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ps" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-pt-BR" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ru" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-rw" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-so" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-sw" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ta" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ti" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ti_ER" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ti_ET" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-tl" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-ur" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-zh" >> scripts/data-info/tico19_tm.csv
./scripts/fn_tico19_datainfo_tmx.py "en-zu" >> scripts/data-info/tico19_tm.csv

#### scripts/data-info/tico19_tm_twb_initial-language-pairs_source-lang-en.csv ________________
# Save the languages to CSV file to reuse later
find data/original/TM/ -iname "all.en-*.zip" \
  | grep -E '(en-...?.?.?.?).tmx' --only-matching \
  | sed 's/.tmx//' | grep -v old | sort > scripts/data-info/tico19_tm_twb_initial-language-pairs_source-lang-en.csv

#### scripts/data-info/tico19_tm_twb_initial-languages.csv _____________________

# cat scripts/data-info/tico19_tm_twb_initial-language-pairs_source-lang-en.csv | sed 's/en-//'
sed 's/en-//' scripts/data-info/tico19_tm_twb_initial-language-pairs_source-lang-en.csv > scripts/data-info/tico19_tm_twb_initial-languages-temp.csv
echo "en" >> scripts/data-info/tico19_tm_twb_initial-languages-temp.csv

sort < scripts/data-info/tico19_tm_twb_initial-languages-temp.csv > scripts/data-info/tico19_tm_twb_initial-languages.csv

rm scripts/data-info/tico19_tm_twb_initial-languages-temp.csv

echo "Okay!"

exit 0

# tico19_tmx_extract "am-om"
# tico19_tmx_extract "am-ti"
# tico19_tmx_extract "ar-es-LA"

# # exit 0

# tico19_tmx_extract "ar-fr"
# tico19_tmx_extract "ar-id"
# tico19_tmx_extract "ar-pt-BR"
# tico19_tmx_extract "ar-ru"
# tico19_tmx_extract "ar-zh"
# tico19_tmx_extract "en-bn"
# tico19_tmx_extract "en-ckb"
# # NOTE: is all.en_ckb.tmx empty?
# # TODO: check en_ckb
# tico19_tmx_extract "en-din"
# tico19_tmx_extract "en-es-LA"

# # TODO: check all.en-fa.old.tmx.zip

# tico19_tmx_extract "en-fa"

# tico19_tmx_extract "en-fr" # NOTE: both .tmx and .tmx.zip present. Likely to be the same (just unziped)
# tico19_tmx_extract "en-fuv" # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-hi" # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-id" # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-km"
# tico19_tmx_extract "en-kr"
# tico19_tmx_extract "en-ku" # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-lg" # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-ln" # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-mr"
# tico19_tmx_extract "en-ms" # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-my"
# tico19_tmx_extract "en-ne"
# tico19_tmx_extract "en-nus"
# tico19_tmx_extract "en-om"
# tico19_tmx_extract "en-prs"
# tico19_tmx_extract "en-ps"  # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-pt-BR"  # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-ru"  # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-rw"  # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-so"
# tico19_tmx_extract "en-sw"
# tico19_tmx_extract "en-ta"
# tico19_tmx_extract "en-ti"
# tico19_tmx_extract "en-ti_ER"
# tico19_tmx_extract "en-ti_ET"
# tico19_tmx_extract "en-tl"
# tico19_tmx_extract "en-ur" # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-zh" # NOTE: both .tmx and .tmx.zip present
# tico19_tmx_extract "en-zu"
# tico19_tmx_extract "es-LA-ar"
# tico19_tmx_extract "es-LA-hi"
# tico19_tmx_extract "es-LA-id"
# tico19_tmx_extract "es-LA-pt-BR"
# tico19_tmx_extract "es-LA-ru"
# tico19_tmx_extract "es-LA-zh"
# tico19_tmx_extract "fa-prs"
# tico19_tmx_extract "fr-ar"
# tico19_tmx_extract "fr-es-LA"
# tico19_tmx_extract "fr-fuv"
# tico19_tmx_extract "fr-hi"
# tico19_tmx_extract "fr-id"
# tico19_tmx_extract "fr-lg"
# tico19_tmx_extract "fr-ln"
# tico19_tmx_extract "fr-pt-BR"
# tico19_tmx_extract "fr-ru"
# tico19_tmx_extract "fr-rw"
# tico19_tmx_extract "fr-sw"
# tico19_tmx_extract "fr-zh"
# tico19_tmx_extract "fr-zu"
# tico19_tmx_extract "hi-ar"
# tico19_tmx_extract "hi-bn"
# tico19_tmx_extract "hi-es-LA"
# tico19_tmx_extract "hi-fr"
# tico19_tmx_extract "hi-id"
# tico19_tmx_extract "hi-mr"
# tico19_tmx_extract "hi-pt-BR"
# tico19_tmx_extract "hi-ru"
# tico19_tmx_extract "hi-ur"
# tico19_tmx_extract "hi-zh"
# tico19_tmx_extract "id-ar"
# tico19_tmx_extract "id-es-LA"
# tico19_tmx_extract "id-fr"
# tico19_tmx_extract "id-hi"
# tico19_tmx_extract "id-pt-BR"
# tico19_tmx_extract "id-ru"
# tico19_tmx_extract "id-zh"
# tico19_tmx_extract "ku-ckb"
# tico19_tmx_extract "pt-BR-ar"
# tico19_tmx_extract "pt-BR-es-LA"
# tico19_tmx_extract "pt-BR-hi"
# tico19_tmx_extract "pt-BR-id"
# tico19_tmx_extract "pt-BR-ru"
# tico19_tmx_extract "pt-BR-zh"
# tico19_tmx_extract "ru-ar"
# tico19_tmx_extract "ru-es-LA"

