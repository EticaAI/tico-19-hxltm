#!/bin/sh
# ==============================================================================
#
#          FILE:  _run-all-data-scripts.sh
#
#         USAGE:  ./scripts/_run-all-data-scripts.sh
#
#   DESCRIPTION:  Run all scripts, in order
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#                 - git
#                 - rsync
#                 - hxltm
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

./scripts/data-original-prepare-terminology.sh

./scripts/data-original-prepare-translation-memory.sh

./scripts/data-hxltm-prepare.sh

./scripts/data-hxltm-terminologia.sh

./scripts/data-hxltm-translation-memory-import.sh

# https://github.com/datasets/language-codes

# @TODO maybe convert docs/eng-Latn/index.adoc
#       to markdown before setup an ascidoctor pipeline here
#       to generate the site. See
#       https://github.com/asciidoctor/asciidoctor/issues/1907
