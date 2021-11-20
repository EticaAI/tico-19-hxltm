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

# TODO: move this to some file related to deploy website
VAR_Gemfile=$(cat << EOF
source 'https://rubygems.org'
gem 'asciidoctor'
gem 'asciidoctor-pdf'
gem 'asciidoctor-epub3'
# https://github.com/asciidoctor/asciidoctor-bibtex
gem 'asciidoctor-bibtex'
# https://github.com/asciidoctor/asciidoctor-chart
gem 'asciidoctor-chart'
## https://github.com/asciidoctor/asciidoctor-latex
# gem 'asciidoctor-latex'
gem 'rouge'
# https://github.com/gjtorikian/html-proofer
gem 'html-proofer'
EOF
)
echo "$VAR_Gemfile" > Gemfile
# bundle install
# bundle exec asciidoctor-pdf -v --attribute allow-uri-read=1 --attribute source-highlighter=rouge docs/eng-Latn/index.adoc --out-file docs/tico-19-hxltm_eng-Latn.pdf

./scripts/data-original-download.sh

./scripts/data-external-prepare.sh

./scripts/data-original-prepare-terminology.sh

./scripts/data-original-prepare-translation-memory.sh

./scripts/data-hxltm-prepare.sh

./scripts/data-hxltm-terminologia.sh

./scripts/data-hxltm-translation-memory-import.sh
