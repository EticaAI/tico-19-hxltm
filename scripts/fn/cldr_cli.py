#!/usr/bin/python3
# ==============================================================================
#
#          FILE:  cldr_cli.py
#
#         USAGE:  ./scripts/fn/scripts/fn/cldr_cli.py
#
#   DESCRIPTION: CLDR aliases via command line. It will return the JSON part
#                of each file if exists.
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
#       CREATED:  2021-11-20 10:37 UTC
# ==============================================================================

import sys
import os
import json


# /workspace/git/EticaAI/tico-19-hxltm/scripts/data-external/cldr
# CLDR_BASE="scripts/data-external/cldr" CLDR_CLI_DEBUG=1 ./scripts/fn/cldr_cli.py languageAlias por
# CLDR_BASE="scripts/data-external/cldr" CLDR_CLI_DEBUG=1 ./scripts/fn/cldr_cli.py territoryAlias 076
# CLDR_BASE="scripts/data-external/cldr" CLDR_CLI_DEBUG=1 ./scripts/fn/cldr_cli.py likelySubtags por

if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print('usage: ' + sys.argv[0] + ' [command] [parameters]')
    print('example: ')
    print('         ' + sys.argv[0] + ' languageAlias zzz')
    print('             ' + sys.argv[0] + ' languageAlias por')
    print('')
    print('         ' + sys.argv[0] + ' territoryAlias zzz')
    print('             ' + sys.argv[0] + ' territoryAlias 076')
    print('')
    print('         ' + sys.argv[0] + ' likelySubtags zz')
    print('             ' + sys.argv[0] + ' likelySubtags pt')
    print('')
    print('      CLDR_CLI_DEBUG=1 ' + sys.argv[0] + ' [command] [parameters]')
    print('')
    print('NOTE: ')
    print('  CLDR_BASE, environment variable with path to the ' +
          'CLDR JSON files,\n' +
          '  must be already defined to run this script. For example: \n')
    print('  CLDR_BASE="~/Downloads/cldr/" ' +
          sys.argv[0] + ' languageAlias por')

    sys.exit()

if 'CLDR_BASE' not in os.environ:
    sys.exit('ERROR! CLDR_BASE undefined. See ' + sys.argv[0] + ' --help')

is_debug = bool(os.environ.get('CLDR_CLI_DEBUG', '0'))
cldr_alias_path = os.environ['CLDR_BASE'] + '/aliases.json'
cldr_likelySubtags_path = os.environ['CLDR_BASE'] + '/likelySubtags.json'
repo_cldr_json_base = 'https://raw.githubusercontent.com/unicode-org/' + \
    'cldr-json/main/cldr-json/'

if not os.path.exists(cldr_alias_path):
    sys.exit('ERROR! No [' + cldr_alias_path +
             ']. Try ' + repo_cldr_json_base +
             '/main/cldr-json/cldr-core/supplemental/aliases.json')
if not os.path.exists(cldr_likelySubtags_path):
    sys.exit('ERROR! No [' + cldr_likelySubtags_path +
             ']. Try ' + repo_cldr_json_base +
             '/main/cldr-json/cldr-core/supplemental/likelySubtags.json')

if sys.argv[1] == 'languageAlias':
    with open(cldr_alias_path, 'r') as _file:
        data = json.loads(_file.read())

        if sys.argv[2] in data['supplemental']['metadata']['alias']['languageAlias']:
            print(str(data['supplemental']['metadata']
                      ['alias']['languageAlias'][sys.argv[2]]))
        else:
            if is_debug:
                print('{"msg": "Not found [' + sys.argv[2] + '] on [' +
                      cldr_alias_path + ']"}')
    sys.exit()

if sys.argv[1] == 'territoryAlias':
    with open(cldr_alias_path, 'r') as _file:
        data = json.loads(_file.read())

        if sys.argv[2] in data['supplemental']['metadata']['alias']['territoryAlias']:
            print(str(data['supplemental']['metadata']
                      ['alias']['territoryAlias'][sys.argv[2]]))
        else:
            if is_debug:
                print('{"msg": "Not found [' + sys.argv[2] + '] on [' +
                      cldr_alias_path + ']"}')
    sys.exit()

if sys.argv[1] == 'likelySubtags':
    with open(cldr_likelySubtags_path, 'r') as _file:
        data = json.loads(_file.read())

        # print(data['supplemental']['likelySubtags'].keys())

        if sys.argv[2] in data['supplemental']['likelySubtags']:
            print(str(data['supplemental']['likelySubtags'][sys.argv[2]]))
        else:
            if is_debug:
                print('{"msg": "Not found [' + sys.argv[2] + '] on [' +
                      cldr_likelySubtags_path + ']"}')
    sys.exit()


sys.exit('unknow command [' + sys.argv[1] +
         '] . See ' + sys.argv[0] + ' --help')
