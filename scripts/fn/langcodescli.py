#!/usr/bin/python3
# ==============================================================================
#
#          FILE:  langcodescli.py
#
#         USAGE:  ./scripts/fn/langcodescli.py
#
#   DESCRIPTION: A command line wrapper to https://github.com/rspeer/langcodes.
#                Install dependencies with
#                    pip install langcodes[data]
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - python3
#                   - langcodes
#                     - https://github.com/rspeer/langcodes
#                   - click
#                     - https://click.palletsprojects.com/
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
import argparse
import langcodes
# https://realpython.com/comparing-python-command-line-parsing-libraries-argparse-docopt-click/

description = "A command line wrapper to python langcodes"
epilog = """
EXAMPLES:
> Get BCP47 minimum tag
    {0} standardize_tag por-Latn-BR

> Check if language tag is valid.
    These ones have syntax errors (no language with these country codes)
        {0} is_valid jp-JP
        {0} is_valid us

    These are syntax valid (but likely user error)
        {0} is_valid ar-AR
        {0} is_valid en-UK

""".format(sys.argv[0])


def info(args):
    result = langcodes.Language.get(args.tag)
    print(result.describe())
    # print('ooi', result)


def is_valid(args):
    if langcodes.tag_is_valid(args.tag):
        print(1)
        sys.exit(0)
    else:
        print(0)
        sys.exit(1)


def standardize_tag(args):
    print(langcodes.standardize_tag(args.tag))


def speaking_population(args):
    result = langcodes.Language.get(args.tag)
    print(result.speaking_population())

# def noargs():
#     print(sys.argv[0] + ' --help')
#     sys.exit(1)


# parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(
    description=description,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=epilog
)
parser.add_argument('--version', action='version', version='1.0.0')
subparsers = parser.add_subparsers()

standardize_tag_parser = subparsers.add_parser('standardize_tag')
standardize_tag_parser.add_argument(
    'tag', help='Tag value to normalize tags the minimum BCP 47')
standardize_tag_parser.set_defaults(func=standardize_tag)

info_parser = subparsers.add_parser('info')
info_parser.add_argument(
    'tag', help='Tag value to return information')
info_parser.set_defaults(func=info)

speaking_population_parser = subparsers.add_parser('speaking_population')
speaking_population_parser.add_argument(
    'tag', help='Tag value to return information')
speaking_population_parser.set_defaults(func=speaking_population)

is_valid_parser = subparsers.add_parser('is_valid')
is_valid_parser.add_argument(
    'tag', help='Tag value to return information')
is_valid_parser.set_defaults(func=is_valid)

# goodbye_parser = subparsers.add_parser('goodbye')
# goodbye_parser.add_argument('name', help='name of the person to greet')
# goodbye_parser.add_argument('--greeting', default='Hello', help='word to use for the greeting')
# goodbye_parser.add_argument('--caps', action='store_true', help='uppercase the output')
# goodbye_parser.set_defaults(func=greet)

if __name__ == '__main__':
    # return 'oi'
    if len(sys.argv) > 1:
        args = parser.parse_args()
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)
    # try:
    #     args = parser.parse_args()
    #     args.func(args)
    # except:
    #     print('deu erro')
    #     # parser.print_help()
