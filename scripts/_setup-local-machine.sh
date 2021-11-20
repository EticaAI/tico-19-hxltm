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

PWD_NOW=$(pwd)

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
else
    echo 'OK: Gemfile exists'
fi

# TODO:
# .vscode/settings.json
# # {
# #     "xml.fileAssociations": [
# #         {
# #             "pattern": "**/*.tmx",
# #             "systemId": "scripts/dtd/tmx14.dtd"
# #         }
# #     ]
# # }


if [ ! -L './docs/scripts' ]; then
    cd './docs/'
    echo "Create link on /docs/scripts to top folder, since the docs simulate "
    echo "GitHub pages deployment"
    ln -s ../scripts/ ./
    cd "$PWD_NOW"
else
    echo 'OK: ./docs/scripts symlink exists'
fi

if [ ! -L './docs/data' ]; then
    cd './docs/'
    echo "Create link on /docs/scripts to top folder, since the docs simulate "
    echo "GitHub pages deployment"
    ln -s ../data/ ./
    cd "$PWD_NOW"
else
    echo 'OK: ./docs/data symlink exists'
fi

printf "\nTesting if some required software are already installed. "
printf "If something fails, you may not run all software or need some changes\n"


set -x
git --version

rsync --version

## @see https://hxltm.etica.ai
hxltmcli --version

## @seehttps://github.com/johnkerl/miller
mlr --version

## @see http://xmlsoft.org/; example: sudo apt  install libxml2-utils
xmllint --version

## Example: sudo apt  install xmlstarlet
xmlstarlet --version
set +x

# bundle exec asciidoctor-pdf -v --attribute allow-uri-read=1 --attribute source-highlighter=rouge docs/eng-Latn/index.adoc --out-file docs/tico-19-hxltm_eng-Latn.pdf
# bundle exec asciidoctor-epub3 -v --attribute allow-uri-read=1 --attribute source-highlighter=rouge docs/eng-Latn/index.adoc --out-file docs/tico-19-hxltm_eng-Latn.epub

echo 'OKAY. All working'