#!/bin/sh -l
# ==============================================================================
#
#          FILE:  download-source.sh
#
#         USAGE:  ./download-source.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-11 15:25 UTC started (on hxltm-action)
# ==============================================================================

pwd_now=$(pwd)
data_original_dir=$(dirname "$0")

cd "$data_original_dir" || exit

# wget https://github.com/tico-19/tico-19.github.io/archive/refs/heads/master.zip

curl -L "https://github.com/tico-19/tico-19.github.io/archive/refs/heads/master.zip" \
  --output "tico-19.github.io.zip"

unzip "tico-19.github.io.zip" "tico-19.github.io-master/data/*" -d "$data_original_dir"
# unzip myfile.zip -d "some directory"
# rm -f myfile.zip


cd "$pwd_now" || exit