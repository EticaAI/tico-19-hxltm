#!/bin/sh
# ==============================================================================
#
#          FILE:  _run-all-data-scripts.sh
#
#         USAGE:  ./scripts/_run-all-data-scripts.sh
#
#   DESCRIPTION:  Run all data manipulation scripts in order.
#                 In short, it will download the lastest version at
#                 https://github.com/tico-19/tico-19.github.io/ and
#                 rebuild ALL the data transformations, including part of the
#                 documentation used here.
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#                 - git
#                 - rsync
#                 - hxltm, libhxl
#                   - pip install hxltm-eticaai
#                 - miller
#                   - See <https://github.com/johnkerl/miller>
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
#       CREATED:  2021-11-18 04:43 UTC started
# ==============================================================================
set -e

./scripts/data-original-download.sh

./scripts/data-external-prepare.sh

./scripts/data-original-prepare-terminology.sh

./scripts/data-original-prepare-translation-memory.sh

./scripts/data-hxltm-prepare.sh

./scripts/data-hxltm-terminologia.sh

./scripts/data-hxltm-translation-memory-import.sh
