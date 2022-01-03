#!/usr/bin/python3
# ==============================================================================
#
#          FILE:  datainfo_tmx.py
#
#         USAGE:  ./scripts/fn/datainfo_tmx.py
#
#   DESCRIPTION: Quick and hackish way to generate a CSV formated of what
#                first version of released TMXs from TICO-19 means
#                by the language pair.
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
    print('usage: ' + sys.argv[0] + 'xx-yy xx-YY_ZZ xx-JJ-LL')
    print('example: ')
    print('         ' + sys.argv[0] + ' en-pt-BR en-ti_ER en-es-LA')

    sys.exit()

line_items = []
line_items.append('TICO-19 language pair')
line_items.append('Source Language')
line_items.append('Source language BCP47')
line_items.append('Target language')
line_items.append('Target language BCP47')
line_items.append('Deterministic language pair')
print(','.join(line_items))


def fubar(lang):
    if lang == 'es-LA':
        return 'es-419'
    return lang


def tico19_language_row(tico19_lang_convention):
    if tico19_lang_convention.find('en-') != -1:
        line_items = []
        lang_part_original = tico19_lang_convention
        lang_part_source_original = 'en'
        lang_part_source_bc47 = 'en'
        lang_part_target_original = lang_part_original.replace('en-', '')
        lang_part_target_bc47 = fubar(
            lang_part_target_original.replace('_', '-'))

        lang_pair_deterministic = lang_part_source_bc47 + '_' + \
            lang_part_target_bc47

        line_items.append(lang_part_original)
        line_items.append(lang_part_source_original)
        line_items.append(lang_part_source_bc47)
        line_items.append(lang_part_target_original)
        line_items.append(lang_part_target_bc47)
        line_items.append(lang_pair_deterministic)
        print(','.join(line_items))
        return True

    raise Exception('Not implemented + [' + tico19_lang_convention + ']')


for i in sys.argv[1:]:
    tico19_language_row(i)


sys.exit()
