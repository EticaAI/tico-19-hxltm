#!/bin/sh
# ==============================================================================
#
#          FILE:  build-badges.sh
#
#         USAGE:  ./scripts/build-badges.sh
#
#   DESCRIPTION:  Script NOT related with data generation.
#                 Just create/update the visual badges used on documentation.
#                 Script used to generate img/badges/*.svg used to serve
#                 the README.md files and on the website.
#                 This is not related to data manipulation.
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#                 - pybadges
#                   - See <https://github.com/google/pybadges>
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-12 16:59 UTC started, based on EticaAI
#                                      /inclusao-digital/imagens/badges
#                                      /build-badges.sh
# ==============================================================================

# Requeriment: pybadges (see https://github.com/google/pybadges)
# `pip install pybadges`

python3 -m pybadges --left-text='Downloads' --right-text='Releases' --right-color='#1E90FF' > docs/img/badges/download-releases.svg

python3 -m pybadges --left-text='GitHub' --right-text='EticaAI/tico-19-hxltm' --right-color='#237c02' > docs/img/badges/github.svg
python3 -m pybadges --left-text='Website' --right-text='tico-19-hxltm.etica.ai' --right-color='#237c02' > docs/img/badges/website.svg
