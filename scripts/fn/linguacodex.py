#!/usr/bin/python3
# ==============================================================================
#
#          FILE:  linguacodex.py
#
#         USAGE:  ./scripts/fn/linguacodex.py
#
#   DESCRIPTION: _[eng-Latn] Command line to process language codes
#                Install dependencies with
#                    pip install langcodes[data]
#                [eng-Latn]_
#                Trivia:
#                - lingua cōdex
#                  - https://en.wiktionary.org/wiki/lingua#Latin
#                  - https://en.wiktionary.org/wiki/codex#Latin
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - python3
#                   - langcodes
#                     - https://github.com/rspeer/langcodes
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v0.5
#       CREATED:  2021-11-20 10:37 UTC v0.1 name langcodescli.py
#       CHANGED:  2021-11-21 04:59 UTC v0.5 renamed as linguacodex.py
# ==============================================================================

import sys
import argparse
import json
import langcodes


description = "_[eng-Latn]Command line to process language codes[eng-Latn]_"
epilog = """

ABOUT LANGUAGE-TERRITORY INFORMATION
(--speaking-population, --writing-population)
    The estimates for "writing population" are often overestimates,
    as described in the CLDR documentation on territory data.
    In most cases, they are derived from published data about literacy rates
    in the places where those languages are spoken.
    This doesn't take into account that many literate people around the
    world speak a language that isn't typically written,
    and write in a different language.
    See https://unicode-org.github.io/cldr-staging/charts/39/supplemental
    /territory_language_information.html

""".format(sys.argv[0])

parser = argparse.ArgumentParser(
    description=description,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=epilog
)
parser.add_argument(
    'language_code',
    help='The language code. Requires at least one option, like --info')
parser.add_argument(
    '--info', action='store_true',
    help='General information (JSON output) [default]')
parser.add_argument(
    '--info-in-lang', help='Same as --help, ' +
    'but requires a language parameter to in which language return ' +
    ' the description. (JSON output)')
parser.add_argument(
    '--info-in-autonym', action='store_true',
    help='Same as --info-in-lang, but defaults language_code, e.g. autonym ' +
    '(JSON output)')
parser.add_argument(
    '--bcp47', action='store_true',
    help='Standardize the language code to BCP47 if already not is'
    '(string output) as BCP47')
parser.add_argument(
    '--is-valid-syntax', action='store_true',
    help='Check if is valid. Return 0 plus error code if so wrong ' +
    'that is not even recognizable')
parser.add_argument(
    '--speaking-population', action='store_true',
    help='Estimated speaking population. ')
parser.add_argument(
    '--writing-population', action='store_true',
    help='Estimated writing population')

parser.add_argument('--version', action='version', version='1.0.0')


def info(language_code, info_in_lang=False):
    result = langcodes.Language.get(language_code)
    if info_in_lang:
        if info_in_lang == 'autonym':
            result_item = result.describe(language_code)
        else:
            result_item = result.describe(info_in_lang)
    else:
        result_item = result.describe()

    result_item['bcp47'] = langcodes.standardize_tag(language_code)
    result_item['autonym'] = langcodes.Language.get(language_code).autonym()
    result_item['speaking_population'] = result.speaking_population()
    result_item['writing_population'] = result.writing_population()
    result_item['is_valid_syntax'] = langcodes.tag_is_valid(language_code)

    print(json.dumps(result_item))
    # print('ooi', result)


def is_valid_syntax(language_code):
    if langcodes.tag_is_valid(language_code):
        print(1)
        sys.exit(0)
    else:
        print(0)
        sys.exit(1)


def bcp47(language_code):
    print(json.dumps(langcodes.standardize_tag(language_code)))


def speaking_population(language_code):
    result = langcodes.Language.get(language_code)
    print(json.dumps(result.speaking_population()))


def writing_population(language_code):
    result = langcodes.Language.get(language_code)
    print(json.dumps(result.writing_population()))


def run_cli(args):
    if args.bcp47:
        return bcp47(args.language_code)
    if args.is_valid_syntax:
        return is_valid_syntax(args.language_code)
    if args.speaking_population:
        return speaking_population(args.language_code)
    if args.writing_population:
        return writing_population(args.language_code)
    if args.info_in_lang:
        return info(args.language_code, args.info_in_lang)
    if args.info_in_autonym:
        return info(args.language_code, 'autonym')
    if args.info:
        return info(args.language_code)

    # parser.print_help()
    # sys.exit(1)
    return info(args.language_code)


if __name__ == '__main__':

    args = parser.parse_args()

    if len(sys.argv) > 1:
        run_cli(args)
    else:
        parser.print_help()
        sys.exit(1)
