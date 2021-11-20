#!/bin/sh
# ==============================================================================
#
#          FILE:  _setup-local-machine.sh
#
#         USAGE:  ./scripts/_setup-local-machine.sh
#
#   DESCRIPTION: Script NOT related with data generation.
#                This is only relevant if you are trying to run scripts on
#                your machine (like trying to generate the preview of the
#                website)
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#                 - ruby
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
if [ ! -f 'Gemfile' ]; then
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
    bundle install
fi

set -x
bundle exec asciidoctor-pdf -v --attribute allow-uri-read=1 --attribute source-highlighter=rouge docs/eng-Latn/index.adoc --out-file docs/tico-19-hxltm_eng-Latn.pdf
bundle exec asciidoctor-epub3 -v --attribute allow-uri-read=1 --attribute source-highlighter=rouge docs/eng-Latn/index.adoc --out-file docs/tico-19-hxltm_eng-Latn.epub

set +x
echo 'Okay'