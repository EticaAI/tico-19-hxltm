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

# unzip, xmllint validate, xmllint format
task_1() {
    # TODO: better naming
    # echo "$1"
    if [ ! -f "${TMX_OUT_ALL_DIR}/all.$1.tmx" ]; then
        echo unzip "${TMX_DIR_IN}/all.$1tmx.zip" -d "${TMX_OUT_ALL_DIR}/"
        unzip "${TMX_DIR_IN}/all.$1.tmx.zip" -d "${TMX_OUT_ALL_DIR}/"

        # echo xmllint --dtdvalid scripts/dtd/tmx14.dtd "${TMX_OUT_ALL_DIR}/all.am-om.tmx" 2>/dev/null
        # xmllint --dtdvalid scripts/dtd/tmx14.dtd "${TMX_OUT_ALL_DIR}/all.am-om.tmx" 2>/dev/null
        echo xmllint --dtdvalid scripts/dtd/tmx14.dtd --noout "${TMX_OUT_ALL_DIR}/all.$1.tmx"
        xmllint --dtdvalid scripts/dtd/tmx14.dtd --noout "${TMX_OUT_ALL_DIR}/all.$1.tmx"

        echo xmllint --format "${TMX_OUT_ALL_DIR}/all.$1.tmx" > "${TMX_OUT_ALL_DIR}/all.$1_linted.tmx"
        xmllint --format "${TMX_OUT_ALL_DIR}/all.$1.tmx" > "${TMX_OUT_ALL_DIR}/all.$1_linted.tmx"
    else
        echo "noop $1"
    fi
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

# es-LA-fr (...)

# xmllint --xpath 'text()' --dtdvalid scripts/dtd/tmx14.dtd data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx
# xmlstarlet select --value-of tmx data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx
# xmlstarlet select --template --value-of /tmx data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx

# TODO: implement this type of help
# xmlstarlet select --help

# yq '.[0]' data/original/translation-memory/translators-without-borders/all/all.en-fr.tmx
# yq '.[0]' data/original/translation-memory/translators-without-borders/all/all.ar-pt-BR_linted.tmx

# xmllint --format data/original/translation-memory/translators-without-borders/all/all.am-om.tmx
# if [ ! -f "${TMX_OUT_ALL_DIR}/all.am-om.tmx" ]; then
#     unzip "${TMX_DIR_IN}/all.am-om.tmx.zip" -d "${TMX_OUT_ALL_DIR}/"
#     xmllint --format "${TMX_OUT_ALL_DIR}/all.am-om.tmx" > "${TMX_OUT_ALL_DIR}/all.am-om_linted.tmx"
# fi



# xmllint --dtdvalid scripts/dtd/tmx14.dtd data/original/translation-memory/translators-without-borders/all/all.am-om.tmx

echo "Okay!"