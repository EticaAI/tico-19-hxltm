#!/bin/sh
# ==============================================================================
#
#          FILE:  data-hxltm-prepare.sh
#
#         USAGE:  ./scripts/data-hxltm-prepare.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-18 05:19 UTC started
# ==============================================================================
set -e

PWD_NOW=$(pwd)

cat scripts/data-info/tico19_t_facebook_initial+hotfixes-languages.csv \
  scripts/data-info/tico19_t_google_initial-languages.csv \
  scripts/data-info/tico19_tm_twb_initial-languages.csv \
  | sort | uniq > scripts/data-info/tico19_tm+t_twb+google+facebook_initial-languages.csv


# NOTE: the https://github.com/datasets/language-codes, not used here, is a bit outdated

# https://github.com/datasets/language-code
# if [ ! -d "scripts/language-codes-git" ]; then
#     git clone https://github.com/datasets/language-codes.git scripts/language-codes-git
# fi

# cd scripts/language-codes-git

# ./scripts/language-codes-git/language-codes.sh

# wget http://www.unicode.org/Public/cldr/latest/core.zip

# cd "$PWD_NOW"

echo "Okay!"