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
"""


# >>> Simulationem('linguacodex --de_codex pt').jq()

# >>> Simulationem('linguacodex --de_codex pt').jq('.')

>>> Simulationem('linguacodex --de_codex pt').jq('.codex')
{"_crudum": "pt", "BCP47": "pt", "HXLTMa": "@TODO", "HXLTMt": "@TODO"}

>>> Simulationem('linguacodex --de_codex pt').jq('.codex.BCP47')
"pt"


# >>> LinguaCodex(de_codex='pt').quid()
# '{"de_codex": "pt", "de_codex_norma": "BCP47"}'

TODO: - Need a word for Autonym/endonym, but does not exist in latin
        Prefix here https://www.englishhints.com/latin-prefixes.html
      - https://en.wiktionary.org/wiki/Category:Latin_words_by_prefix

# pip install pyglottolog
# - https://github.com/glottolog/pyglottolog
#   - https://github.com/cldf/cldf/tree/master/components/languages
#     - https://github.com/cldf-datasets/wals/blob/master/cldf/languages.csv
#   - https://wals.info/
# - https://github.com/w3c/i18n-discuss/issues/13
# - About criticisms on ISO 639-1 ISO 639-2
#   - https://www.eva.mpg.de/fileadmin/content_files/linguistics
#     /conferences/2015-diversity-linguistics/Drude_slides.pdf

TESTS
    python3 -m doctest ./scripts/fn/linguacodex.py
    python3 -m doctest -v ./scripts/fn/linguacodex.py
    python3 -m pylint --disable=W0511 -v ./scripts/fn/linguacodex.py
"""
import sys
import os
import argparse
from pathlib import Path
import copy
import csv
import json
from dataclasses import dataclass, InitVar
from typing import (
    Any,
    # Dict,
    # Iterable,
    # Optional,
    # List,
    # TextIO,
    Type,
    Union,
)

import langcodes


DESCRIPTION = "_[eng-Latn]Command line to process language codes[eng-Latn]_"
EPILOG = """

ABOUT LANGUAGE-TERRITORY INFORMATION
(--quod .communitas)
    The estimates for "writing population" are often overestimates,
    as described in the CLDR documentation on territory data.
    In most cases, they are derived from published data about literacy rates
    in the places where those languages are spoken.
    This doesn't take into account that many literate people around the
    world speak a language that isn't typically written,
    and write in a different language.
    See https://unicode-org.github.io/cldr-staging/charts/39/supplemental
    /territory_language_information.html

"""

parser = argparse.ArgumentParser(
    description=DESCRIPTION,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=EPILOG
)

parser.add_argument(
    '--de_codex', action='store', help="""
    The main natural language to inspect using some well know language code.
    """)
# This is just in case we start to add new code standards
parser.add_argument(
    '--de_codex_norma', action='store', default='BCP47', help="""
    When using the code, specify the coding standard used. Defaults to BCP47
    """)
parser.add_argument(
    '--de_nomen', action='store', help="""
    The main natural language to inspect using the title of the language
    in some natural language.
    """)
parser.add_argument(
    '--quod', action='store', help="""
    Dot notation to filter more exact information instead of return all
    information. Example: --quod .codex.BCP47
    """)
# Trivi: verbōsum, https://en.wiktionary.org/wiki/verbosus#Latin
parser.add_argument(
    '--verbosum', action='store_true',
    help='Verbose mode')

parser.add_argument('--version', action='version', version='0.5.0')


# DATA_EXTERNAL = __file__ .
DATA_EXTERNAL_DEFAULT = str(Path(__file__).parent.parent.resolve()) + \
    '/data-external'
DATA_EXTERNAL_CLDR_JSON = 'https://raw.githubusercontent.com/unicode-org/' + \
    'cldr-json/main/cldr-json/'

# Note: is possible to specify a different place for where store the data files
# with environment variable DATA_EXTERNAL
DATA_EXTERNAL = os.environ.get('DATA_EXTERNAL', DATA_EXTERNAL_DEFAULT)


class LinguaCodex:
    """
    _[eng-Latn]
    Command line to process language codes

    Trivia:
    - lingua cōdex
        - https://en.wiktionary.org/wiki/lingua#Latin
        - https://en.wiktionary.org/wiki/codex#Latin

    [eng-Latn]_
    """
    de_codex: str = None
    de_nomen: str = None
    de_exemplum: str = None
    de_codex_norma: str = 'BCP47'
    # nomen_lingua: str = None
    quod: str = '.'
    utilitas: Type['LinguaCodexUtilitas'] = None

    def __init__(
            self, de_codex: str = None,
            de_nomen: str = None,
            de_exemplum: str = None,
            de_codex_norma: str = 'BCP47',
            quod: str = '.'
    ):  # pylint: disable=too-many-arguments
        """LinguaCodex initiāle
        """
        if de_codex:
            self.de_codex = de_codex
        if de_nomen:
            self.de_nomen = de_nomen
        if de_exemplum:
            self.de_exemplum = de_exemplum
        if de_codex_norma:
            self.de_codex_norma = de_codex_norma
        if quod:
            self.quod = quod

        self.utilitas = LinguaCodexUtilitas()

    # def quid(self):
    #     return LinguaCodexQuid.in_textum_json(self.__dict__)

    def quid(self, info_in_lang=False):

        # TODO: try catch with errors for codes like
        result_ = langcodes.Language.get(self.de_codex)
        if info_in_lang:
            if info_in_lang == 'autonym':
                result = result_.describe(self.de_codex)
            else:
                result = result_.describe(info_in_lang)
        else:
            result = result_.describe()

        # result['bcp47'] = langcodes.standardize_tag(self.de_codex)
        # result['codex'] = {
        #     '_crudum': self.de_codex,
        #     'BCP47': langcodes.standardize_tag(self.de_codex),
        #     'HXLTMa': '',
        #     'HXLTMt': ''
        # }
        result['codex'] = {}
        if self.de_codex:
            result['codex']['_crudum'] = self.de_codex
        result['codex']['BCP47'] = langcodes.standardize_tag(self.de_codex)
        result['codex']['HXLTMa'] = '@TODO'
        result['codex']['HXLTMt'] = '@TODO'

        # https://en.wikipedia.org/wiki/Endonym_and_exonym
        # Autonym, https://en.wikipedia.org/wiki/Autonym
        # endonym, https://en.wikipedia.org/wiki/Endonym_and_exonym
        # exonym/xenonym (maybe xenomen??)
        # nōmen, https://en.wiktionary.org/wiki/nomen#Derived_terms
        # *-, https://www.englishhints.com/latin-prefixes.html
        # extra-, http://www.perseus.tufts.edu/hopper
        #         /resolveform?type=start&lookup=extra&lang=la
        result['nomen'] = {}
        if self.de_nomen:
            result['nomen']['_crudum'] = self.de_nomen
        result['nomen']['autonym'] = langcodes.Language.get(
            self.de_codex).autonym()
        result['nomen']['exonym'] = {}

        # commūnitās, https://en.wiktionary.org/wiki/communitas#Latin
        result['communitas'] = {
            # litterātum, https://en.wiktionary.org/wiki/litteratus#Latin
            'litteratum': result_.speaking_population(),
            # scrībendum, https://en.wiktionary.org/wiki/scribo#Latin
            'scrībendum': result_.writing_population()
        }
        # TODO: separate part to script
        # scrīptum, https://en.wiktionary.org/wiki/scriptum#Latin

        # 	errōrem, https://en.wiktionary.org/wiki/error#Latin
        # typum, https://en.wiktionary.org/wiki/typus#Latin
        # https://en.wiktionary.org/wiki/syntaxis#Latin
        if not langcodes.tag_is_valid(self.de_codex):
            result['errorem_syntaxin'] = True

        # result['errorem'] = not langcodes.tag_is_valid(self.de_codex)
        # result['errorem'] = not langcodes.tag_is_valid(self.de_codex)

        # print('oi', self.quod)

        return in_jq(result, self.quod)
        # print(json.dumps(result_item))
        # print('ooi', result)


class LinguaCodexUtilitas:
    """LinguaCodexUtilitas
    _[eng-Latn]
    Quick and hacky bunch of staticmethod functions that could be decoupled
    [eng-Latn]_
    Trivia:
    - lingua cōdex
        - https://en.wiktionary.org/wiki/lingua#Latin
        - https://en.wiktionary.org/wiki/codex#Latin
    - ūtilitās
        - https://en.wiktionary.org/wiki/utilitas#Latin
    """

    # DATA_EXTERNAL can be defined as environment variable
    data_external: str = DATA_EXTERNAL
    likelySubtags: dict = {}
    bcp47langToIso15924: dict = {}
    iso6393ToGlottocode: dict = {}

    def __init__(
            self
            # self, de_codex: str = None,
            # de_nomen: str = None,
            # de_exemplum: str = None,
            # de_codex_norma: str = 'BCP47',
            # quod: str = '.'
    ):  # pylint: disable=too-many-arguments
        """LinguaCodex initiāle
        """
        self._init_data_cldf()
        self._init_data_cldr()

    def _init_data_cldf(self):
        """_init_data_cldf
        """
        cldfLanguages_path = DATA_EXTERNAL + '/cldf/languages.csv'

        with open(cldfLanguages_path, 'r') as file_:
            csv_reader = csv.DictReader(file_)
            line_count = 0
            for row in csv_reader:
                if row["ISO639P3code"]:
                    self.iso6393ToGlottocode[row["ISO639P3code"]] = \
                        row["Glottocode"]
                    # self.cldfLanguages[row["ISO639P3code"]] = {
                    #     'ISO639P3code': row["ISO639P3code"],
                    #     'Glottocode': row["Glottocode"],
                    #     'Name': row["Name"]
                    # }

        # print(self.iso6393ToGlottocode)
        # pass

    def _init_data_cldr(self):
        """_init_data_cldr
        """
        likelySubtags = DATA_EXTERNAL + '/cldr/likelySubtags.json'

        with open(likelySubtags, 'r') as file_:
            data = json.loads(file_.read())
            self.likelySubtags = data['supplemental']['likelySubtags']

            # for item in data['supplemental']['likelySubtags']:
            #     print(item)

        self._init_data_cldf()

    @staticmethod
    def in_exemplum_funcion(rem: Union[int, str]) -> int:
        """Rem in numerum simplex?

        _[eng-Latn]
        explanation here
        [eng-Latn]_

        Trivia:
          - rem, https://en.wiktionary.org/wiki/res#Latin
          - in, https://en.wiktionary.org/wiki/in#Latin
          - numerum, https://en.wiktionary.org/wiki/numerus#Latin
          - simplex, https://en.wiktionary.org/wiki/simplex#Latin
          - disciplīnam manuāle
            - https://en.wikipedia.org/wiki/IEEE_754

        Args:
            rem ([Any]): Rem

        Returns:
            [Union[int, float]]: Rem in numerum IEEE integer aut IEEE 754

        Exemplōrum gratiā (et Python doctest, id est, testum automata):

            # >>> HXLTMTypum.in_numerum_simplex('1234')
            # 1234
            # >>> HXLTMTypum.in_numerum_simplex('1234.0')
            # 1234
        """
        # pylint: disable=invalid-name,no-else-return
        pass
        # try:
        #     n = float(rem)
        #     if n == int(n):
        #         return int(n)
        #     else:
        #         return n
        # except Exception as expt:
        #     raise ValueError(
        #         "Non numerum trānslātiōnem: {}".format(rem)) from expt

    def quod_iso15924_de_bcp47(
            rem: str,
            formosum: Union[bool, int] = None,
            clavem_sortem: bool = False,
            imponendum_praejudicium: bool = False
    ) -> str:
        """Trānslātiōnem: rem in textum JSON

        Trivia:
            - quod, https://en.wiktionary.org/wiki/quod#Latin
            - rem, https://en.wiktionary.org/wiki/res#Latin
            - in, https://en.wiktionary.org/wiki/in#Latin
            - json, https://www.json.org/
            - fōrmōsum, https://en.wiktionary.org/wiki/formosus
            - impōnendum, https://en.wiktionary.org/wiki/enforcier#Old_French
            - praejūdicium, https://en.wiktionary.org/wiki/praejudicium#Latin
            - sortem, https://en.wiktionary.org/wiki/sors#Latin
            - clāvem, https://en.wiktionary.org/wiki/clavis#Latin

        Args:
            rem ([Any]): Rem

        Returns:
            [str]: Rem in JSON textum

        Exemplōrum gratiā (et Python doctest, id est, testum automata):

    >>> rem = {"b": 2, "a": ['ت', 'ツ', '😊']}

    >>> in_textum_json(rem)
    '{"b": 2, "a": ["ت", "ツ", "😊"]}'

    # >>> in_textum_json(rem, clavem_sortem=True)
    # '{"a": ["ت", "ツ", "😊"], "b": 2}'
    #
    # >>> in_textum_json(rem, imponendum_praejudicium=True)
    # '{"b": 2, "a": ["\\\u062a", "\\\u30c4", "\\\ud83d\\\ude0a"]}'
    #
    # >>> in_textum_json(rem, formosum=True)
    # '{\\n    "b": 2,\\n    \
    # "a": [\\n        "ت",\\n        "ツ",\\n        "😊"\\n    ]\\n}'

    """

        # print = json.dumps()

        if formosum is True:
            formosum = 4

        json_textum = json.dumps(
            rem,
            indent=formosum,
            sort_keys=clavem_sortem,
            ensure_ascii=imponendum_praejudicium
        )

        return json_textum


@dataclass
class LinguaCodexQuid:
    """LinguaCodexQuid

    Trivia:
        - fōrmātum, https://en.wiktionary.org/wiki/formatus#Latin
    [extended_summary]
    """
    lingua_codex: InitVar[Type['LinguaCodex']] = None

    def __init__(self, lingua_codex: Type['LinguaCodex']):
        """LinguaCodexQuid initiāle
        """
        self.lingua_codex = lingua_codex


def in_jq(rem, quod: str = '.', incognitum: Any = '?!?'):
    """in_jq TODO document
    >>> in_jq({'a': {'aa1': 1, "aa2": 2}, 'b': 10}, '.b')
    10
    >>> in_jq({'a': {'aa1': 1, "aa2": 2}, 'b': 10}, '.a')
    {'aa1': 1, 'aa2': 2}
    >>> in_jq({'a': {'aa1': 1, "aa2": 2}, 'b': 10}, '.a.aa1')
    1
    """
    neo_rem = rem
    if len(quod.strip('.')) > 0:
        parts = quod.strip('.').split('.')
        # print('parts', parts)
        for item in parts:
            # print('item', item, result)
            if neo_rem is not None and item in neo_rem:
                neo_rem = neo_rem[item]
            else:
                neo_rem = incognitum
                break

    return neo_rem


def bcp47_langtag(rem: str, item: str = None) -> dict:
    """Public domain python function to process BCP47 langtag

    Created at 2021-11-22. Partial implementation of BCP47 (RFC 5646).
    See https://tools.ietf.org/search/bcp47.

    Args:
        rem (str): The BCP47 langtag

    Returns:
        dict: Python dictionary. None means not found. False means the feature
                                 is not implemented

    Author:
        Emerson Rocha <rocha(at)ieee.org>

    License:
        SPDX-License-Identifier: Unlicense OR 0BSD

    -------------
    The syntax of the language tag in ABNF [RFC5234] is:

    Language-Tag  = langtag             ; normal language tags
                / privateuse          ; private use tag
                / grandfathered       ; grandfathered tags
    langtag       = language
                    ["-" script]
                    ["-" region]
                    *("-" variant)
                    *("-" extension)
                    ["-" privateuse]

    language      = 2*3ALPHA            ; shortest ISO 639 code
                    ["-" extlang]       ; sometimes followed by
                                        ; extended language subtags
                / 4ALPHA              ; or reserved for future use
                / 5*8ALPHA            ; or registered language subtag

    extlang       = 3ALPHA              ; selected ISO 639 codes
                    *2("-" 3ALPHA)      ; permanently reserved

    script        = 4ALPHA              ; ISO 15924 code

    region        = 2ALPHA              ; ISO 3166-1 code
                / 3DIGIT              ; UN M.49 code

    variant       = 5*8alphanum         ; registered variants
                / (DIGIT 3alphanum)

    extension     = singleton 1*("-" (2*8alphanum))

                                        ; Single alphanumerics
                                        ; "x" reserved for private use
    singleton     = DIGIT               ; 0 - 9
                / %x41-57             ; A - W
                / %x59-5A             ; Y - Z
                / %x61-77             ; a - w
                / %x79-7A             ; y - z

    privateuse    = "x" 1*("-" (1*8alphanum))

    grandfathered = irregular           ; non-redundant tags registered
                / regular             ; during the RFC 3066 era

    irregular     = "en-GB-oed"         ; irregular tags do not match
                / "i-ami"             ; the 'langtag' production and
                / "i-bnn"             ; would not otherwise be
                / "i-default"         ; considered 'well-formed'
                / "i-enochian"        ; These tags are all valid,
                / "i-hak"             ; but most are deprecated
                / "i-klingon"         ; in favor of more modern
                / "i-lux"             ; subtags or subtag
                / "i-mingo"           ; combination
                / "i-navajo"
                / "i-pwn"
                / "i-tao"
                / "i-tay"
                / "i-tsu"
                / "sgn-BE-FR"
                / "sgn-BE-NL"
                / "sgn-CH-DE"

    regular       = "art-lojban"        ; these tags match the 'langtag'
                / "cel-gaulish"       ; production, but their subtags
                / "no-bok"            ; are not extended language
                / "no-nyn"            ; or variant subtags: their meaning
                / "zh-guoyu"          ; is defined by their registration
                / "zh-hakka"          ; and all of these are deprecated
                / "zh-min"            ; in favor of a more modern
                / "zh-min-nan"        ; subtag or sequence of subtags
                / "zh-xiang"

    alphanum      = (ALPHA / DIGIT)     ; letters and numbers
    -------------

    Tests (run with python3 -m doctest myscript.py):

        >>> bcp47_langtag('pt-Latn-BR', 'language')
        'pt'
    """
    result = {
        'langtag': rem,
        'language': None,
        'script': None,
        'region': None,
        'privateuse': [],
        'extension': False,  # This will not be implemented
        'variant': False,  # This will not be implemented
        'grandfathered': False,  # This will not be implemented
    }

    parts = rem.replace('_', '-').strip().split('-')

    # for part in parts:
    #     if result['language'] is None:
            
    result['language'] = parts[0]

    # Stritly speaking, we shoudl check if is alpha2 or alpha3
    

    if item != None:
        return result[item]

    return result


def in_textum_json(
        rem: Any,
        formosum: Union[bool, int] = None,
        clavem_sortem: bool = False,
        imponendum_praejudicium: bool = False
) -> str:
    """Trānslātiōnem: rem in textum JSON

    Trivia:
        - rem, https://en.wiktionary.org/wiki/res#Latin
        - in, https://en.wiktionary.org/wiki/in#Latin
        - json, https://www.json.org/
        - fōrmōsum, https://en.wiktionary.org/wiki/formosus
        - impōnendum, https://en.wiktionary.org/wiki/enforcier#Old_French
        - praejūdicium, https://en.wiktionary.org/wiki/praejudicium#Latin
        - sortem, https://en.wiktionary.org/wiki/sors#Latin
        - clāvem, https://en.wiktionary.org/wiki/clavis#Latin

    Args:
        rem ([Any]): Rem

    Returns:
        [str]: Rem in JSON textum

    Exemplōrum gratiā (et Python doctest, id est, testum automata):

>>> rem = {"b": 2, "a": ['ت', 'ツ', '😊']}

>>> in_textum_json(rem)
'{"b": 2, "a": ["ت", "ツ", "😊"]}'

# >>> in_textum_json(rem, clavem_sortem=True)
# '{"a": ["ت", "ツ", "😊"], "b": 2}'
#
# >>> in_textum_json(rem, imponendum_praejudicium=True)
# '{"b": 2, "a": ["\\\u062a", "\\\u30c4", "\\\ud83d\\\ude0a"]}'
#
# >>> in_textum_json(rem, formosum=True)
# '{\\n    "b": 2,\\n    \
# "a": [\\n        "ت",\\n        "ツ",\\n        "😊"\\n    ]\\n}'

"""

    # print = json.dumps()

    if formosum is True:
        formosum = 4

    json_textum = json.dumps(
        rem,
        indent=formosum,
        sort_keys=clavem_sortem,
        ensure_ascii=imponendum_praejudicium
    )

    return json_textum

# def linguacodex_cli(args):
# https://en.wiktionary.org/wiki/simulatio#Latin

# https://stackoverflow.com/questions/50886471
# /simulating-argparse-command-line-arguments-input-while-debugging
# /50886791#50886791


class LinguaCodexCli:
    argparse_args = None
    linguacodex: Type['LinguaCodex'] = None

    def __init__(self, argparse_args):
        """Simulationem initiāle
        """
        self.argparse_args = argparse_args

        self.linguacodex = LinguaCodex(
            de_codex=argparse_args.de_codex,
            de_codex_norma=argparse_args.de_codex_norma,
            de_nomen=argparse_args.de_nomen,
            quod=argparse_args.quod
        )

    def resultatum(self):
        # print('oooi', self.linguacodex)
        # print('oooi5', self.linguacodex.__dict__)
        # print('oooi6', self.linguacodex.quid())
        return self.linguacodex.quid()

    def resultatum_in_textum(self):
        return in_textum_json(self.resultatum())


class Simulationem:
    argumenta: str = None

    def __init__(self, argumenta):
        """Simulationem initiāle
        """
        self.argumenta = argumenta

    def jq(self, jq_argumenta='.'):  # pylint: disable=invalid-name
        sys.argv = self.argumenta.split(' ')
        args = parser.parse_args()
        # result_original = run_cli(args)
        result_original = LinguaCodexCli(args).resultatum()
        # print('ooi7', result_original, type(result_original))
        # TODO: implement jq_argumenta
        result = copy.copy(result_original)
        # result = []
        if len(jq_argumenta.strip('.')) > 0:
            parts = jq_argumenta.strip('.').split('.')
            # print('parts', parts)
            for item in parts:
                # print('item', item, result)
                if result is not None and item in result:
                    result = result[item]
                else:
                    result = '?!?'
                    break

        print(in_textum_json(result))


def simulationem(argumenta: str):
    """simulationem
    Trivia:
    - simulātiōnem, https://en.wiktionary.org/wiki/simulatio#Latin

    Args:
        argumenta (str): Command line arguments
    """
    # parts = 'linguacodex.py' + ' '.split(argumenta)
    sys.argv = argumenta.split(' ')
    # print(sys.argv, argumenta, ' '.split(argumenta))
    args = parser.parse_args()
    # print(run_cli(args))
    print(LinguaCodexCli(args).resultatum_in_textum())


if __name__ == '__main__':

    args_ = parser.parse_args()

    if len(sys.argv) > 1:
        # run_cli(args)
        print(LinguaCodexCli(args_).resultatum_in_textum())
    else:
        parser.print_help()
        sys.exit(1)
