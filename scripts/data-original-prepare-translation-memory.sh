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
#                 - pip install langcodes[data]
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

# set -x
rsync --archive --verbose "${DATA_ORIGINAL_GIT_DIR}/data/" "$DATA_ORIGINAL_DIR/"
# set +x

# is this empty???
# cp "${DATA_ORIGINAL_DIR}/TM/all.en_ckb.tmx" "${DATA_ORIGINAL_DIR}/translation-memory/translators-without-borders/all/"

# xmlstarlet select --template --value-of /tmx/body/tu/tuv/@xml:lang data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx

# unzip, xmllint validate, xmllint format
task_1() {
    # TODO: better naming
    # echo "$1"
    if [ ! -f "${TMX_OUT_ALL_DIR}/all.$1.tmx" ]; then
        echo "start $1"
        echo unzip "${TMX_DIR_IN}/all.$1tmx.zip" -d "${TMX_OUT_ALL_DIR}/"
        unzip "${TMX_DIR_IN}/all.$1.tmx.zip" -d "${TMX_OUT_ALL_DIR}/"

        # echo xmllint --dtdvalid scripts/dtd/tmx14.dtd "${TMX_OUT_ALL_DIR}/all.am-om.tmx" 2>/dev/null
        # xmllint --dtdvalid scripts/dtd/tmx14.dtd "${TMX_OUT_ALL_DIR}/all.am-om.tmx" 2>/dev/null
        echo xmllint --dtdvalid scripts/dtd/tmx14.dtd --noout "${TMX_OUT_ALL_DIR}/all.$1.tmx"
        xmllint --dtdvalid scripts/dtd/tmx14.dtd --noout "${TMX_OUT_ALL_DIR}/all.$1.tmx"


        echo xmllint --format "${TMX_OUT_ALL_DIR}/all.$1.tmx" > "${TMX_OUT_ALL_DIR}/all.$1_linted.tmx"
        xmllint --format "${TMX_OUT_ALL_DIR}/all.$1.tmx" > "${TMX_OUT_ALL_DIR}/all.$1_linted.tmx"

        rm "${TMX_OUT_ALL_DIR}/all.$1.tmx"
    else
        echo "noop $1"
    fi

    # Print unique languages on each file
    # xmlstarlet select --template --value-of /tmx/body/tu/tuv/@xml:lang "${TMX_OUT_ALL_DIR}/all.$1_linted.tmx" | sort | uniq
    xmlstarlet select --template --value-of /tmx/body/tu/tuv/@xml:lang "${TMX_OUT_ALL_DIR}/all.$1_linted.tmx" | sort | uniq | xargs echo
    # xmlstarlet select --template --value-of /tmx/body/tu/tuv/@xml:lang "${TMX_OUT_ALL_DIR}/all.$1_linted.tmx" | sort | uniq | python3 -c "from langcodes import *; import sys; print(Language.make(language='fr').display_name())"
}


task_1 "am-om"
task_1 "am-ti"
task_1 "ar-es-LA"
task_1 "ar-fr"
task_1 "ar-id"
task_1 "ar-pt-BR"
task_1 "ar-ru"
task_1 "ar-zh"
task_1 "en-bn"
task_1 "en-ckb"
# NOTE: is all.en_ckb.tmx empty?
# TODO: check en_ckb
task_1 "en-din"
task_1 "en-es-LA"

# TODO: check all.en-fa.old.tmx.zip

task_1 "en-fa"

task_1 "en-fr" # NOTE: both .tmx and .tmx.zip present. Likely to be the same (just unziped)
task_1 "en-fuv" # NOTE: both .tmx and .tmx.zip present
task_1 "en-hi" # NOTE: both .tmx and .tmx.zip present
task_1 "en-id" # NOTE: both .tmx and .tmx.zip present
task_1 "en-km"
task_1 "en-kr"
task_1 "en-ku" # NOTE: both .tmx and .tmx.zip present
task_1 "en-lg" # NOTE: both .tmx and .tmx.zip present
task_1 "en-ln" # NOTE: both .tmx and .tmx.zip present
task_1 "en-mr"
task_1 "en-ms" # NOTE: both .tmx and .tmx.zip present
task_1 "en-my"
task_1 "en-ne"
task_1 "en-nus"
task_1 "en-om"
task_1 "en-prs"
task_1 "en-ps"  # NOTE: both .tmx and .tmx.zip present
task_1 "en-pt-BR"  # NOTE: both .tmx and .tmx.zip present
task_1 "en-ru"  # NOTE: both .tmx and .tmx.zip present
task_1 "en-rw"  # NOTE: both .tmx and .tmx.zip present
task_1 "en-so"
task_1 "en-sw"
task_1 "en-ta"
task_1 "en-ti"
task_1 "en-ti_ER"
task_1 "en-ti_ET"
task_1 "en-tl"
task_1 "en-ur" # NOTE: both .tmx and .tmx.zip present
task_1 "en-zh" # NOTE: both .tmx and .tmx.zip present
task_1 "en-zu"
task_1 "es-LA-ar"
task_1 "es-LA-hi"
task_1 "es-LA-id"
task_1 "es-LA-pt-BR"
task_1 "es-LA-ru"
task_1 "es-LA-zh"
task_1 "fa-prs"
task_1 "fr-ar"
task_1 "fr-es-LA"
task_1 "fr-fuv"
task_1 "fr-hi"
task_1 "fr-id"
task_1 "fr-lg"
task_1 "fr-ln"
task_1 "fr-pt-BR"
task_1 "fr-ru"
task_1 "fr-rw"
task_1 "fr-sw"
task_1 "fr-zh"
task_1 "fr-zu"
task_1 "hi-ar"
task_1 "hi-bn"
task_1 "hi-es-LA"
task_1 "hi-fr"
task_1 "hi-id"
task_1 "hi-mr"
task_1 "hi-pt-BR"
task_1 "hi-ru"
task_1 "hi-ur"
task_1 "hi-zh"
task_1 "id-ar"
task_1 "id-es-LA"
task_1 "id-fr"
task_1 "id-hi"
task_1 "id-pt-BR"
task_1 "id-ru"
task_1 "id-zh"
task_1 "ku-ckb"
task_1 "pt-BR-ar"
task_1 "pt-BR-es-LA"
task_1 "pt-BR-hi"
task_1 "pt-BR-id"
task_1 "pt-BR-ru"
task_1 "pt-BR-zh"
task_1 "ru-ar"
task_1 "ru-es-LA"

# ru-fr. (...)


# https://github.com/datasets/language-codes/blob/master/language-codes.sh
# xmllint --xpath 'text()' --dtdvalid scripts/dtd/tmx14.dtd data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx
# xmlstarlet select --value-of tmx data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx
# xmlstarlet select --template --value-of /tmx data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx

# xmlstarlet select --template --value-of /tmx/body/tu/@lang data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx
# xmlstarlet select --template --value-of /tmx/body/tu/tuv[@xml:lang] data/original/translation-memory/translators-without-borders/all/all.en-fr.tm
# https://pypi.org/project/langcodes/
# python3 -c "from langcodes import *; import sys; print('rob')"
# python3 -c "from langcodes import *; import sys; print(Language.make(language='fr').display_name())"

# TODO: implement this type of help
# xmlstarlet select --help

# yq '.[0]' data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx
# yq '.[0]' data/original/translation-memory/translators-without-borders/all/all.ar-pt-BR_linted.tmx

# xmllint --format data/original/translation-memory/translators-without-borders/all/all.am-om.tmx
# if [ ! -f "${TMX_OUT_ALL_DIR}/all.am-om.tmx" ]; then
#     unzip "${TMX_DIR_IN}/all.am-om.tmx.zip" -d "${TMX_OUT_ALL_DIR}/"
#     xmllint --format "${TMX_OUT_ALL_DIR}/all.am-om.tmx" > "${TMX_OUT_ALL_DIR}/all.am-om_linted.tmx"
# fi



# find data/original/TM/ -iname all.en-*.zip | wc -l
#     38
# find data/original/TM/ -iname all.en-*.zip
#     data/original/TM/all.en-fr.tmx.zip
#     data/original/TM/all.en-lg.tmx.zip
#     data/original/TM/all.en-so.tmx.zip
#     data/original/TM/all.en-hi.tmx.zip
#     data/original/TM/all.en-es-LA.tmx.zip
#     data/original/TM/all.en-ar.tmx.zip
#     data/original/TM/all.en-ti_ET.tmx.zip
#     data/original/TM/all.en-ru.tmx.zip
#     data/original/TM/all.en-zh.tmx.zip
#     data/original/TM/all.en-prs.tmx.zip
#     data/original/TM/all.en-pt-BR.tmx.zip
#     data/original/TM/all.en-zu.tmx.zip
#     data/original/TM/all.en-bn.tmx.zip
#     data/original/TM/all.en-ne.tmx.zip
#     data/original/TM/all.en-km.tmx.zip
#     data/original/TM/all.en-ta.tmx.zip
#     data/original/TM/all.en-ckb.tmx.zip
#     data/original/TM/all.en-kr.tmx.zip
#     data/original/TM/all.en-sw.tmx.zip
#     data/original/TM/all.en-ti.tmx.zip
#     data/original/TM/all.en-ha.tmx.zip
#     data/original/TM/all.en-ku.tmx.zip
#     data/original/TM/all.en-ln.tmx.zip
#     data/original/TM/all.en-fuv.tmx.zip
#     data/original/TM/all.en-ms.tmx.zip
#     data/original/TM/all.en-id.tmx.zip
#     data/original/TM/all.en-din.tmx.zip
#     data/original/TM/all.en-ur.tmx.zip
#     data/original/TM/all.en-fa.tmx.zip
#     data/original/TM/all.en-rw.tmx.zip
#     data/original/TM/all.en-ps.tmx.zip
#     data/original/TM/all.en-fa.old.tmx.zip
#     data/original/TM/all.en-mr.tmx.zip
#     data/original/TM/all.en-ti_ER.tmx.zip
#     data/original/TM/all.en-om.tmx.zip
#     data/original/TM/all.en-my.tmx.zip
#     data/original/TM/all.en-tl.tmx.zip
#     data/original/TM/all.en-nus.tmx.zip

# find data/original/TM/ -iname all.en-*.zip | grep -E en-..?.?\.
# find data/original/TM/ -iname all.en-*.zip | grep -E en-..?.?\. --only-matching

# find data/original/TM/ -iname all.en-*.zip | grep -E '(en-...?.?.?.?).tmx' --only-matching | wc -l
#     38


# find data/original/TM/ -iname all.en-*.zip | grep -E '(en-...?.?.?.?).tmx' --only-matching | sed 's/.tmx//'
#     en-fr
#     en-lg
#     en-so
#     en-hi
#     en-es-LA
#     en-ar
#     en-ti_ET
#     en-ru
#     en-zh
#     en-prs
#     en-pt-BR
#     en-zu
#     en-bn
#     en-ne
#     en-km
#     en-ta
#     en-ckb
#     en-kr
#     en-sw
#     en-ti
#     en-ha
#     en-ku
#     en-ln
#     en-fuv
#     en-ms
#     en-id
#     en-din
#     en-ur
#     en-fa
#     en-rw
#     en-ps
#     en-fa.old
#     en-mr
#     en-ti_ER
#     en-om
#     en-my
#     en-tl
#     en-nus


# xmllint --dtdvalid scripts/dtd/tmx14.dtd data/original/translation-memory/translators-without-borders/all/all.am-om.tmx

echo "Okay!"