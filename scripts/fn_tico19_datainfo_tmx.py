#!/usr/bin/python3
# ==============================================================================
#
#          FILE:  scripts/fn_tico19_datainfo_tmx.py
#
#         USAGE:  ./scripts/fn_tico19_datainfo_tmx.py
#
#   DESCRIPTION: Hardcoded function to generate data about what should be
#                converted based on the whatever whas the file naming
#                on the original.
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - python3
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-20 03:26 UTC
# ==============================================================================

import sys

if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print('usage: ' + sys.argv[0] + 'xx-yy')
    print('example: ')
    print('example: ')
    print('         ' + sys.argv[0] + ' csv-header')
    print('         ' + sys.argv[0] + ' en-pt-BR')
    print('         ' + sys.argv[0] + ' en-ti_ER')

    sys.exit()

# print(sys.argv[1].find('en-'))

if sys.argv[1] == 'csv-header':
    line_items = []
    line_items.append('tmx_filename_original_lang')
    line_items.append('source_lang_original')
    line_items.append('source_lang_bcp47')
    line_items.append('target_lang_original')
    line_items.append('target_lang_bcp47')
    print(','.join(line_items))
    sys.exit()

if sys.argv[1].find('en-') != -1:

    line_items = []
    lang_part_original = sys.argv[1]
    lang_part_source_original = 'en'
    lang_part_source_bc47 = 'en'
    lang_part_target_original = lang_part_original.replace('en-', '')
    lang_part_target_bc47 = lang_part_target_original.replace('_', '-')

    line_items.append(lang_part_original)
    line_items.append(lang_part_source_original)
    line_items.append(lang_part_source_bc47)
    line_items.append(lang_part_target_original)
    line_items.append(lang_part_target_bc47)
    print(','.join(line_items))
    sys.exit()


# The way the filenames was so poor that we will not implement en
# all options for a funcion just to allow a quick metadata info.
# We also will generate full dataset later, so no problem
raise Exception('Not implemented')
