#!/bin/sh
# ==============================================================================
#
#          FILE:  build-ebooks.sh
#
#         USAGE:  ./scripts/build-ebooks.sh
#
#   DESCRIPTION:  Script NOT related with data generation.
#                 Create ebooks.
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#                 - scripts/_setup-local-machine.sh
#                 - asciidoctor-pdf
#                 - asciidoctor-epub3
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-20 09:12 UTC
# ==============================================================================

set -e
set -x

bundle exec asciidoctor-pdf -v --attribute allow-uri-read=1 --attribute source-highlighter=rouge docs/eng-Latn/index.adoc --out-file docs/tico-19-hxltm_eng-Latn.pdf
bundle exec asciidoctor-epub3 -v --attribute allow-uri-read=1 --attribute source-highlighter=rouge docs/eng-Latn/index.adoc --out-file docs/tico-19-hxltm_eng-Latn.epub

set +x