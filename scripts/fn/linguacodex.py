#!/usr/bin/python3
# ==============================================================================
#
#          FILE:  linguacodex.py
#
#         USAGE:  ./scripts/fn/linguacodex.py
#
#   DESCRIPTION: _[eng-Latn]
#                Expert system command line tool to aid misuse of language codes
#                [eng-Latn]_
#                Trivia:
#                - lingua cōdex
#                  - https://en.wiktionary.org/wiki/lingua#Latin
#                  - https://en.wiktionary.org/wiki/codex#Latin
#
#       OPTIONS:  See linguacodex.py --help
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
#       VERSION:  v0.6
#       CREATED:  2021-11-20 10:37 UTC v0.1 name langcodescli.py
#       CHANGED:  2021-11-21 04:59 UTC v0.5 renamed as linguacodex.py
#                 2021-11-23 09:20 UTC v0.6 --in_bcp47_simplex implemented
# ==============================================================================
"""linguacodex: expert system command line tool to aid misuse of language codes

>>> Simulationem('linguacodex --de_codex pt').jq('.codex')
{"BCP47": "pt", "ISO639P3": "por", "ISO639P2B": "por", \
"ISO639P2T": "por", "ISO639P1": "pt", "Glotto": "port1283"}

>>> Simulationem(
...   'linguacodex --de_codex pt --imponendum_praejudicium').jq('.codex')
{"BCP47": "pt", "ISO639P3": "por", "ISO639P2B": "por", \
"ISO639P2T": "por", "ISO639P1": "pt", "Glotto": "port1283", "ISO15924A": "Latn"}

>>> Simulationem('linguacodex --de_codex pt').jq('.codex.BCP47')
"pt"

>>> Simulationem(
... 'linguacodex --de_codex en-b-ccc-bbb-a-aaa-X-xyz --in_bcp47_simplex')\
    .jq('.Language-Tag_normalized')
"en-a-aaa-b-bbb-ccc-x-xyz"


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

TESTS:
    python3 -m doctest ./scripts/fn/linguacodex.py
    python3 -m doctest -v ./scripts/fn/linguacodex.py
    python3 -m pylint --disable=C0302,W0511 -v ./scripts/fn/linguacodex.py
Manual tests (eventually remove it):
    ./scripts/fn/linguacodex.py --de_codex pt
    ./scripts/fn/linguacodex.py --de_codex pt --in_bcp47_simplex

    # This is well formed, but langcodes 3.3.0 think it is invalid
    ./scripts/fn/linguacodex.py --de_codex en-GB-oxedict | jq

./scripts/fn/linguacodex.py --de_nomen pt --imponendum_praejudicium | jq
./scripts/fn/linguacodex.py --de_nomen Português --imponendum_praejudicium | jq
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
    (from python langcodes documentation)
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
    in some natural language. Requires --imponendum_praejudicium.
    """)
parser.add_argument(
    '--quod', action='store', default=".", help="""
    Dot notation to filter more exact information instead of return all
    information. Example: --quod .codex.BCP47
    """)
parser.add_argument(
    '--in_bcp47_simplex', action='store_true', help="""
    Define output as simple syntax parsing of input code as BCP47, without any
    advanced processing and/or conversion. Works even without download external
    data. Result use same key names as BCP47, except by
    'Language-Tag_normalized', '_unknown' and '_error' (JSON output)
    """)
# Trivia:
# - impōnendum, https://en.wiktionary.org/wiki/enforcier#Old_French
# - praejūdicium, https://en.wiktionary.org/wiki/praejudicium#Latin
parser.add_argument(
    '--imponendum_praejudicium', action='store_true', default=False,
    help="""
    Enforce linguistic prejudgment. Default: disabled.
    """
)
# Trivia: verbōsum, https://en.wiktionary.org/wiki/verbosus#Latin
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
    # pylint: disable=too-few-public-methods,too-many-instance-attributes
    de_codex: str = None
    de_nomen: str = None
    de_exemplum: str = None
    de_codex_norma: str = 'BCP47'
    # nomen_lingua: str = None
    quod: str = '.'
    # in_bcp47_simplex: bool = False
    imponendum_praejudicium: bool = False

    # TODO: maybe take the systema_locale from the current terminal.
    #       (example from env vars: LANGUAGE=pt_BR:pt:en). For now
    #       we're defaulting to most common scripts
    # @see - https://www.worldatlas.com/articles
    #        /the-world-s-most-popular-writing-scripts.html
    #      - https://github.com/unicode-org/cldr-json/blob/main/cldr-json
    #        /cldr-core/supplemental/likelySubtags.json
    #      - https://unicode.org/iso15924/iso15924-codes.html
    systema_locale: list = [
        # Sorted by script ISO 15924 (latin) letter code
        'ar-Arab',
        'hy-Armn',
        'ru-Cyrl',
        'hi-Deva',
        'gu-Gujr',
        'el-Grek',
        'ka-Geor',
        'pa-Guru',
        'zh-Hans',
        'zh-Hant',
        'he-Hebr',
        'ko-Jamo',
        'jv-Java',
        'ja-Kana',
        'km-Khmr',
        'kn-Knda',
        'lo-Laoo',
        'la-Latn',
        'my-Mymr',
        'su-Sund',
        'ta-Taml',
        'te-Telu',
        'th-Thai',
        'bo-Tibt',
        'ii-Yiii',
    ]

    utilitas: Type['LinguaCodexUtilitas'] = None

    def __init__(
            self, de_codex: str = None,
            de_nomen: str = None,
            de_exemplum: str = None,
            de_codex_norma: str = 'BCP47',
            quod: str = '.',
            systama_locale: list = None,
            imponendum_praejudicium: bool = False
            # in_bcp47_simplex: bool = False
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

        if imponendum_praejudicium is not False:
            self.imponendum_praejudicium = imponendum_praejudicium

        if systama_locale is not None:
            self.systama_locale = systama_locale
        # if in_bcp47_simplex:
        #     self.in_bcp47_simplex = in_bcp47_simplex

        self.utilitas = LinguaCodexUtilitas()

    # def quid(self):
    #     return LinguaCodexQuid.in_textum_json(self.__dict__)

    def quid(self, info_in_lang=False):
        """quid [TODO documen]

        [extended_summary]

        Args:
            info_in_lang (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """
        # pylint: disable=too-many-branches,too-many-statements

        # TODO: implement try catch with errors for langcodes
        # TODO: eventually refactor this entire method. Doing too much here

        # imponendum_praejudicium_rem
        ipr = []

        if self.de_codex:
            de_codex = self.de_codex
        elif self.de_nomen:
            de_codex = langcodes.find(self.de_nomen).to_tag()
            ipr.append('de_codex')
            #  = self.de_codex

        result_ = langcodes.Language.get(de_codex)
        if info_in_lang:
            if info_in_lang == 'autonym':
                result = result_.describe(de_codex)
            else:
                result = result_.describe(info_in_lang)
        else:
            result = result_.describe()

        # result['bcp47'] = langcodes.standardize_tag(de_codex)
        # result['codex'] = {
        #     '_crudum': de_codex,
        #     'BCP47': langcodes.standardize_tag(de_codex),
        #     'HXLTMa': '',
        #     'HXLTMt': ''
        # }
        # Trivia:
        # - macro_linguae de
        #   https://books.google.com.br
        #   /books?id=D-5GAAAAcAAJ&pg=PA400&lpg=PA400&dq=%22macro+linguae%22
        result['macro_linguae'] = None
        result['codex'] = {}

        result['codex']['BCP47'] = langcodes.standardize_tag(de_codex)
        if 'de_codex' in ipr and result['codex']['BCP47']:
            ipr.append('codex.BCP47')

        codex_language = bcp47_langtag(de_codex, 'language')
        # print('codex_language', codex_language)

        iso639 = iso639_type(self.utilitas.iso6393, codex_language)

        if iso639 and 'ISO639P3code' in iso639:
            ipr_b = []
            result['codex']['ISO639P3'] = iso639['ISO639P3code']  # type: ignore

            ipr_b.append('codex.ISO639P3')

            if iso639['ISO639P2Bcode']:  # type: ignore
                result['codex']['ISO639P2B'] = \
                    iso639['ISO639P2Bcode']  # type: ignore
                ipr_b.append('codex.ISO639P2B')

            if iso639['ISO639P2Tcode']:  # type: ignore
                result['codex']['ISO639P2T'] = \
                    iso639['ISO639P2Tcode']  # type: ignore
                ipr_b.append('codex.ISO639P2T')

            if iso639['ISO639P1code']:  # type: ignore
                result['codex']['ISO639P1'] = \
                    iso639['ISO639P1code']  # type: ignore
                ipr_b.append('codex.ISO639P1')

            scope = iso639['ISO639P3scope']  # type: ignore
            if scope:
                if scope == 'I':
                    result['macro_linguae'] = False
                elif scope == 'M':
                    result['macro_linguae'] = True

            if result['codex']['ISO639P3'] in self.utilitas.iso6393ToGlottocode:
                result['codex']['Glotto'] = \
                    self.utilitas.iso6393ToGlottocode[
                        result['codex']['ISO639P3']]
                ipr_b.append('codex.Glotto')

            if 'de_codex' in ipr:
                ipr.extend(ipr_b)

        # glottocode

        iso15924a = cldr_likely_iso15924(
            self.utilitas.likely_subtags,
            de_codex,
        )
        if iso15924a['script']:  # type: ignore
            if iso15924a['imponendum_praejudicium'] is False:  # type: ignore
                # cldr_likely_iso15924 found exact match, great
                result['codex']['ISO15924A'] = \
                    iso15924a['script']  # type: ignore
                # pass
            elif self.imponendum_praejudicium is True:

                # cldr_likely_iso15924 not found exact match, inference allowed
                result['codex']['ISO15924A'] = \
                    iso15924a['script']  # type: ignore
                ipr.append('codex.ISO15924A')
                # pass
            # pass

        # result['codex']['ISO15924A'] = iso15924a
        # result['codex']['HXLTMa'] = '@TODO'
        # result['codex']['HXLTMt'] = '@TODO'

        # commūnitās, https://en.wiktionary.org/wiki/communitas#Latin
        result['communitas'] = {
            # litterātum, https://en.wiktionary.org/wiki/litteratus#Latin
            'litteratum': result_.speaking_population(),
            # scrībendum, https://en.wiktionary.org/wiki/scribo#Latin
            'scribendum': result_.writing_population()
        }

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
            de_codex).autonym()
        result['nomen']['exonym'] = {}

        if self.systema_locale is not None and len(self.systema_locale) > 0:
            for lang in self.systema_locale:
                result['nomen']['exonym'][lang] = langcodes.Language.get(
                    de_codex).display_name(lang)

        # TODO: separate part to script
        # scrīptum, https://en.wiktionary.org/wiki/scriptum#Latin

        # 	errōrem, https://en.wiktionary.org/wiki/error#Latin
        # typum, https://en.wiktionary.org/wiki/typus#Latin
        # https://en.wiktionary.org/wiki/syntaxis#Latin
        if not langcodes.tag_is_valid(de_codex):
            result['errorem_syntaxin'] = True

        # result['errorem'] = not langcodes.tag_is_valid(de_codex)
        # result['errorem'] = not langcodes.tag_is_valid(de_codex)

        # print('oi', self.quod)

        result['praejudicium'] = ipr

        result['__meta'] = {}
        if self.de_codex:
            result['__meta']['de_codex'] = self.de_codex
        if self.de_nomen:
            result['__meta']['de_nomen'] = self.de_nomen
        if self.imponendum_praejudicium:
            result['__meta']['imponendum_praejudicium'] = \
                self.imponendum_praejudicium
            # result['__meta']['praejudicium'] = ipr

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
    # pylint: disable=too-few-public-methods

    # DATA_EXTERNAL can be defined as environment variable
    data_external: str = DATA_EXTERNAL
    likely_subtags: dict = {}
    # bcp47langToIso15924: dict = {}
    iso6393ToGlottocode: dict = {}
    iso6393: list = []

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
        self._init_data_iso639_3()

    def _init_data_cldf(self):
        """_init_data_cldf
        """
        cldf_language_path = DATA_EXTERNAL + '/cldf/languages.csv'

        with open(cldf_language_path, 'r') as file_:
            csv_reader = csv.DictReader(file_)
            # line_count = 0
            # print('oi')
            for row in csv_reader:
                if row["ISO639P3code"] and row["Glottocode"]:
                    key = row["ISO639P3code"]

                    # Uncomment the next block to find imperfect ISO6393 to
                    # Glottocode. As 2021-11-23, this happens with
                    # [eus][basq1248][basq1250]
                    # if key in self.iso6393ToGlottocode:
                    #     if self.iso6393ToGlottocode[key] != row["Glottocode"]:
                    #         print('mismatch [' + row["ISO639P3code"] + '][' +
                    #               self.iso6393ToGlottocode[key] +
                    #               '][' + row["Glottocode"] + ']')
                    self.iso6393ToGlottocode[key] = \
                        row["Glottocode"]

    def _init_data_cldr(self):
        """_init_data_cldr
        """
        likely_subtags = DATA_EXTERNAL + '/cldr/likelySubtags.json'

        with open(likely_subtags, 'r') as file_:
            data = json.loads(file_.read())
            self.likely_subtags = data['supplemental']['likelySubtags']

            # for item in data['supplemental']['likelySubtags']:
            #     print(item)

        self._init_data_cldf()

    def _init_data_iso639_3(self):
        """_init_data_iso639_3
        """
        iso639_3_path = DATA_EXTERNAL + '/iso-639-3.csv'

        with open(iso639_3_path, 'r') as file_:
            csv_reader = csv.DictReader(file_)
            # line_count = 0
            for row in csv_reader:
                self.iso6393.append({
                    'ISO639P3code': row['Id'],
                    'ISO639P2Bcode': row['Part2B'],
                    'ISO639P2Tcode': row['Part2T'],
                    'ISO639P1code': row['Part1'],
                    'ISO639P3scope': row['Scope'],
                    'ISO639P3languagetype': row['Language_Type'],
                    'ISO639P3refname': row['Ref_Name'],
                })
                # if row["ISO639P3code"]:
                #     self.iso6393[row["ISO639P3code"]] = \
                #         row["Glottocode"]


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


def cldr_likely_iso15924(
        dictionarium: dict,
        langtag: str,
        clavem: Type[Union[str, list]] = None,
        strictum_certum: bool = False,
) -> Type[Union[dict, str]]:
    """cldr_likely_iso15924 Likely ISO 15924 (script) from BCP47 tag

    Trivia:
    - CLDR, https://cldr.unicode.org/
    - langtag, https://tools.ietf.org/search/bcp47
    - dictiōnārium, https://en.wiktionary.org/wiki/dictionarium#Latin
    - resultātum, https://en.wiktionary.org/wiki/resultatum#Latin
    - certum, https://en.wiktionary.org/wiki/certus#Latin
    - strictum, https://en.wiktionary.org/wiki/strictus#Latin

    Args:
        dictionarium (dict): Python dictionary keys + values like the
                             CLDR supplemental.likelySubtags
        bcp47_langtag (str): [description]
        clavem (Type[Union[str, list]], optional): Key to return.
                                                   Defaults to None.
        strictum_certum (bool, optional): If only accept exact match.
                                          Defaults to False.

    Returns:
        Type[Union[dict, str]]: Either dict or exact result key

    Tests:
    >>> dictionarium = {'pt': 'pt-Latn-BR', 'und-BR': 'pt-Latn-BR', \
'und-419': 'es-Latn-419', 'zh': 'zh-Hans-CN'}

    >>> cldr_likely_iso15924(dictionarium, 'pt-Latn')
    {'Language-Tag': 'pt-Latn', 'script': 'Latn', \
'imponendum_praejudicium': False}

    >>> cldr_likely_iso15924(dictionarium, 'pt')
    {'Language-Tag': 'pt', 'script': 'Latn', 'imponendum_praejudicium': True}

    >>> cldr_likely_iso15924(dictionarium, 'und-BR', 'script')
    'Latn'
    >>> cldr_likely_iso15924(dictionarium, 'und-BR', 'script', True)

    >>> cldr_likely_iso15924(dictionarium, 'und-Latn-BR', 'script', True)
    'Latn'
    """
    resultatum = {
        'Language-Tag': langtag,
        'script': None,
        'imponendum_praejudicium': None
    }
    # exact_scriptum = bcp47_langtag(langtag, 'script')
    langtag_certum = bcp47_langtag(langtag)
    if langtag_certum['script']:
        resultatum['script'] = langtag_certum['script']
        resultatum['imponendum_praejudicium'] = False
    elif not strictum_certum:
        if langtag_certum['region']:
            lpr = langtag_certum['language'] + '-' + langtag_certum['region']
            if lpr in dictionarium:
                langtag_non_certum = bcp47_langtag(dictionarium[lpr])
                resultatum['script'] = langtag_non_certum['script']
                resultatum['imponendum_praejudicium'] = True
        # TODO: try by ISO3 too, or inverse by ISO2
        if not resultatum['script']:
            lll = langtag_certum['language']
            if lll in dictionarium:
                langtag_non_certum = bcp47_langtag(dictionarium[lll])
                resultatum['script'] = langtag_non_certum['script']
                resultatum['imponendum_praejudicium'] = True
            # pass

    # resultatum['__dictionarium'] = dictionarium
    # resultatum['__langtag_certum'] = langtag_certum

    if clavem is not None:
        if isinstance(clavem, str):
            return resultatum[clavem]
        if isinstance(clavem, list):
            rresultatum_partial = {}
            for item in clavem:
                rresultatum_partial[item] = resultatum[item]
            return rresultatum_partial
        raise TypeError(
            'clavem [' + str(type(clavem)) + '] != [str, list]')

    return resultatum


def bcp47_langtag(
        rem: str,
        clavem: Type[Union[str, list]] = None,
        strictum: bool = True
) -> dict:
    """Public domain python function to process BCP47 langtag

    Created at 2021-11-22. Partial implementation of BCP47 (RFC 5646).
    See https://tools.ietf.org/search/bcp47.

    Args:
        rem (str):                       The BCP47 langtag
        clavem (Type[Union[str, list]]): Key (string) for specific value or keys
                                         (list) to return a dict (optional)
        strictum (bool):                 Throw exceptions. False replace values
                                        with False (optional)

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

    Most tests use examples from https://tools.ietf.org/search/bcp47 and
    https://github.com/unicode-org/cldr/blob/main/tools/cldr-code
    /src/main/resources/org/unicode/cldr/util/data/langtagTest.txt

    TESTS (run with python3 -m doctest myscript.py):

    >>> bcp47_langtag('pt-Latn-BR', 'language')
    'pt'

    >>> bcp47_langtag('pt-Latn-BR', 'script')
    'Latn'

    >>> bcp47_langtag('pt-Latn-BR', 'region')
    'BR'

    >>> bcp47_langtag('de-CH-1996', 'variant')
    ['1996']

    >>> bcp47_langtag('x-fr-CH', ['language', 'region', 'privateuse'])
    {'language': None, 'region': None, 'privateuse': ['fr', 'CH']}

    >>> bcp47_langtag('i-klingon', 'grandfathered')
    'i-klingon'

    >>> bcp47_langtag('zh-min-nan', 'language')
    'zh'

    >>> bcp47_langtag('zh-min-nan', 'variant')
    ['min-nan']

    >>> bcp47_langtag('es-419', 'region')
    '419'

    >>> bcp47_langtag('en-oxendict', 'variant') # Oxford English Dictionary
    ['oxendict']

    >>> bcp47_langtag('zh-pinyin', 'variant') # Pinyin romanization
    ['pinyin']

    >>> bcp47_langtag('zh-pinyin', 'script') # Limitation: cannot infer Latn

    >>> bcp47_langtag('en-a-bbb-x-a-ccc', 'privateuse')
    ['a', 'ccc']

    >>> bcp47_langtag('en-a-bbb-x-a-ccc', 'extension')
    {'a': ['bbb']}

    >>> bcp47_langtag('tlh-a-b-foo', '_error')
    Traceback (most recent call last):
    ...
    ValueError: Errors for [tlh-a-b-foo]: extension [a] empty

    >>> bcp47_langtag('tlh-a-b-foo', '_error', False)
    ['extension [a] empty']

    >>> bcp47_langtag(
    ... 'zh-Latn-CN-variant1-a-extend1-x-wadegile-private1',
    ... ['variant', 'extension', 'privateuse'])
    {'variant': ['variant1'], 'extension': {'a': ['extend1']}, \
'privateuse': ['wadegile', 'private1']}

    >>> bcp47_langtag(
    ... 'en-Latn-US-lojban-gaulish-a-12345678-ABCD-b-ABCDEFGH-x-a-b-c-12345678')
    {'Language-Tag': \
'en-Latn-US-lojban-gaulish-a-12345678-ABCD-b-ABCDEFGH-x-a-b-c-12345678', \
'Language-Tag_normalized': \
'en-Latn-US-lojban-gaulish-a-12345678-abcd-b-abcdefgh-x-a-b-c-12345678', \
'language': 'en', 'script': 'Latn', 'region': 'US', \
'variant': ['lojban', 'gaulish'], \
'extension': {'a': ['12345678', 'abcd'], 'b': ['abcdefgh']}, \
'privateuse': ['a', 'b', 'c', '12345678'], \
'grandfathered': None, '_unknown': [], '_error': []}

    # BCP47: "Example: The language tag "en-a-aaa-b-ccc-bbb-x-xyz" is in
    # canonical form, while "en-b-ccc-bbb-a-aaa-X-xyz" is well-formed (...)
    >>> bcp47_langtag(
    ... 'en-b-ccc-bbb-a-aaa-X-xyz')
    {'Language-Tag': 'en-b-ccc-bbb-a-aaa-X-xyz', \
'Language-Tag_normalized': 'en-a-aaa-b-bbb-ccc-x-xyz', \
'language': 'en', 'script': None, 'region': None, 'variant': [], \
'extension': {'a': ['aaa'], 'b': ['bbb', 'ccc']}, 'privateuse': ['xyz'], \
'grandfathered': None, '_unknown': [], '_error': []}
    """
    # For sake of copy-and-paste portability, we ignore a few pylints:
    # pylint: disable=too-many-branches,too-many-statements,too-many-locals
    result = {
        # The input Language-Tag, _as it is_
        'Language-Tag': rem,
        # The Language-Tag normalized syntax, if no errors
        'Language-Tag_normalized': None,
        'language': None,
        'script': None,
        'region': None,
        'variant': [],
        'extension': {},   # Example {'a': ['bbb', 'ccc'], 'd': True}
        'privateuse': [],  # Example: ['wadegile', 'private1']
        'grandfathered': None,
        '_unknown': [],
        '_error': [],
    }

    skip = 0

    if not isinstance(rem, str) or len(rem) == 0:
        result['_error'].append('Empty/wrong type')
        skip = 1
    else:
        rem = rem.replace('_', '-').strip()

    # The weird tags first: grandfathered/irregular
    if rem in [
        'en-GB-oed', 'i-ami', 'i-bnn', 'i-default', 'i-enochian',
        'i-hak', 'i-klingon', 'i-lux', 'i-ming', 'i-navajo', 'i-pwn',
            'i-tao', 'i-tay', 'i-tsu', 'sgn-BE-FR', 'sgn-BE-NL', 'sgn-CH-DE']:
        # result['langtag'] = None
        result['language'] = rem.lower()
        result['grandfathered'] = rem
        skip = 1
    # The weird tags first: grandfathered/regular
    if rem in [
            'art-lojban', 'cel-gaulish', 'no-bok', 'no-nyn', 'zh-guoyu',
            'zh-hakka', 'zh-min', 'zh-min-nan', 'zh-xiang']:

        parts_r = rem.split('-')
        # result['langtag'] = None
        result['language'] = parts_r.pop(0).lower()
        result['variant'].append('-'.join(parts_r).lower())
        result['grandfathered'] = rem
        skip = 1

    parts = rem.split('-')
    leftover = []

    deep = 0
    while len(parts) > 0 and skip == 0 and deep < 100:
        deep = deep + 1

        # BCP47 can start with private tag, without language at all
        if parts[0].lower() == 'x':
            parts.pop(0)
            while len(parts) > 0:
                result['privateuse'].append(parts.pop(0))
            break

        # BCP47 extensions start with one letter.
        if len(parts[0]) == 1 and parts[0].isalpha():
            if parts[0].isalpha() == 'i':
                result['_error'].append('Only grandfathered can use i-')

            extension_key = parts.pop(0).lower()
            if len(parts) == 0 or len(parts[0]) == 1:
                # BCP47 2.2.6. : "Each singleton MUST be followed by at least
                # one extension subtag (...)
                result['extension'][extension_key] = [None]
                result['_error'].append(
                    'extension [' + extension_key + '] empty')
                continue

            result['extension'][extension_key] = []
            while len(parts) > 0 and len(parts[0]) != 1:
                result['extension'][extension_key].append(
                    parts.pop(0).lower())
            continue

        # for part in parts:
        if result['language'] is None:
            if parts[0].isalnum() and len(parts[0]) == 2 or len(parts[0]) == 3:
                result['language'] = parts[0].lower()
            else:
                result['language'] = False
                result['_error'].append('language?')
            parts.pop(0)
            continue

        # Edge case to test for numeric in 4 (not 3): 'de-CH-1996'
        if len(parts[0]) == 4 and parts[0].isalpha() \
                and result['script'] is None:
            # if parts[0].isalpha() and result['script'] is None:
            if parts[0].isalpha():
                if result['region'] is None and len(result['privateuse']) == 0:
                    result['script'] = parts[0].capitalize()
                else:
                    result['script'] = False
                    result['_error'].append('script after region/privateuse')
            else:
                result['script'] = False
                result['_error'].append('script?')
            parts.pop(0)
            continue

        if len(parts[0]) == 2 and result['region'] is None:
            if parts[0].isalpha():
                result['region'] = parts[0].upper()
            else:
                result['region'] = False
                result['_error'].append('region?')
            parts.pop(0)
            continue

        if len(parts[0]) == 3 and result['region'] is None:
            if parts[0].isnumeric():
                result['region'] = parts.pop(0)
            else:
                result['region'] = False
                result['_error'].append('region?')
                parts.pop(0)
            continue

        if len(result['extension']) == 0 and len(result['privateuse']) == 0:
            # "Variant subtags that begin with a letter (a-z, A-Z) MUST be
            # at least five characters long."
            if parts[0][0].isalpha() and len(parts[0]) >= 5:
                result['variant'].append(parts.pop(0))
                continue
            if parts[0][0].isnumeric() and len(parts[0]) >= 4:
                result['variant'].append(parts.pop(0))
                continue

        leftover.append(parts.pop(0))

    result['_unknown'] = leftover

    if len(result['extension']) > 0:
        extension_norm = {}
        # keys
        keys_sorted = sorted(result['extension'])
        # values
        for key in keys_sorted:
            extension_norm[key] = sorted(result['extension'][key])

        result['extension'] = extension_norm

    if len(result['_error']) == 0:

        if result['grandfathered']:
            result['Language-Tag_normalized'] = result['grandfathered']
        else:
            norm = []
            if result['language']:
                norm.append(result['language'])
            if result['script']:
                norm.append(result['script'])
            if result['region']:
                norm.append(result['region'])
            if len(result['variant']) > 0:
                norm.append('-'.join(result['variant']))

            if len(result['extension']) > 0:
                for key in result['extension']:
                    if result['extension'][key][0] is None:
                        norm.append(key)
                    else:
                        norm.append(key)
                        norm.extend(result['extension'][key])

            if len(result['privateuse']) > 0:
                norm.append('x-' + '-'.join(result['privateuse']))

            result['Language-Tag_normalized'] = '-'.join(norm)

    if strictum and len(result['_error']) > 0:
        raise ValueError(
            'Errors for [' + rem + ']: ' + ', '.join(result['_error']))

    if clavem is not None:
        if isinstance(clavem, str):
            return result[clavem]
        if isinstance(clavem, list):
            result_partial = {}
            for item in clavem:
                result_partial[item] = result[item]
            return result_partial
        raise TypeError(
            'clavem [' + str(type(clavem)) + '] != [str, list]')

    return result


def iso639_type(
        dictionarium: Type['list[dict]'],
        language: str,
        clavem: Type[Union[str, list]] = None,
        # strictum_certum: bool = False,
) -> Type[Union[dict, str]]:
    """iso639_type Inferecen about ISO 639 type (using ISO 639-3 reference)

    Trivia:
    - ISO 639-3, https://iso639-3.sil.org/
    - langtag, https://tools.ietf.org/search/bcp47
    - dictiōnārium, https://en.wiktionary.org/wiki/dictionarium#Latin
    - resultātum, https://en.wiktionary.org/wiki/resultatum#Latin
    - certum, https://en.wiktionary.org/wiki/certus#Latin
    - strictum, https://en.wiktionary.org/wiki/strictus#Latin

    Args:
        dictionarium (dict): Python dictionary keys + values like the
                             CLDR supplemental.likelySubtags
        bcp47_langtag (str): [description]
        clavem (Type[Union[str, list]], optional): Key to return.
                                                   Defaults to None.
        strictum_certum (bool, optional): If only accept exact match.
                                          Defaults to False.

    Returns:
        Type[Union[dict, str]]: Either dict or exact result key

    Tests:
    >>> dictionarium = [{'ISO639P3code':'por', 'ISO639P2Bcode': 'por', \
'ISO639P2Tcode': 'por', 'ISO639P1code': 'pt', 'ISO639P3scope': 'I', \
'ISO639P3languagetype': 'L', 'ISO639P3refname': 'Portuguese'}]

    >>> iso639_type(dictionarium, 'pt', '_type')
    'ISO639P1code'

    >>> iso639_type(dictionarium, 'por', '_type')
    'ISO639P3code'

    >>> iso639_type(dictionarium, 'zzz', '_type')

    """
    resultatum = {}
    for item in dictionarium:
        if language == item['ISO639P3code']:  # type: ignore
            resultatum = item
            resultatum['_type'] = 'ISO639P3code'
            break
        if language == item['ISO639P2Bcode']:  # type: ignore
            resultatum = item
            resultatum['_type'] = 'ISO639P2Bcode'
        if language == item['ISO639P2Tcode']:  # type: ignore
            resultatum = item
            resultatum['_type'] = 'ISO639P2Tcode'
        if language == item['ISO639P1code']:  # type: ignore
            resultatum = item
            resultatum['_type'] = 'ISO639P1code'
            break

    if clavem and resultatum:
        return resultatum[clavem]

    return resultatum if resultatum else None


def in_obiectum_planum(rem: dict):
    """in_obiectum_1_level [summary]

    [extended_summary]

    Args:
        rem (dict): [description]

    Returns:
        [type]: [description]

    >>> in_obiectum_planum({'a': {'a1': {'a2': 'va'}}, 'b': 'vb'})
    """
    # obiectum, https://en.wiktionary.org/wiki/obiectum#Latin
    # recursiōnem, https://en.wiktionary.org/wiki/recursio#Latin
    # praefīxum, https://en.wiktionary.org/wiki/praefixus#Latin
    # plānum, https://en.wiktionary.org/wiki/planus

    def recursionem(rrem, praefixum: str = ''):
        pass

    return rem


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
    """LinguaCodexCli
    """
    argparse_args = None
    linguacodex: Type['LinguaCodex'] = None
    in_bcp47_simplex: bool = False
    error: list = []

    def __init__(self, argparse_args):
        """Simulationem initiāle
        """
        self.argparse_args = argparse_args

        if argparse_args.in_bcp47_simplex:
            self.in_bcp47_simplex = True
            # pass
        else:
            self.linguacodex = LinguaCodex(
                de_codex=argparse_args.de_codex,
                de_codex_norma=argparse_args.de_codex_norma,
                de_nomen=argparse_args.de_nomen,
                quod=argparse_args.quod,
                imponendum_praejudicium=argparse_args.imponendum_praejudicium
                # in_bcp47_simplex=argparse_args.in_bcp47_simplex
            )

    def resultatum(self):
        """resultatum [summary]

        [extended_summary]

        Returns:
            [type]: [description]
        """
        # print('oooi', self.linguacodex)
        # print('oooi5', self.linguacodex.__dict__)
        # print('oooi6', self.linguacodex.quid())

        # print(self)
        # print(self.argparse_args)
        # sys.exit()

        if not self.argparse_args.de_codex:
            if not self.argparse_args.de_nomen:
                # raise ValueError('--de_codex? --de_nomen?')
                self.error.append('--de_codex? --de_nomen?')
                return None
            if not self.argparse_args.imponendum_praejudicium:
                self.error.append('--imponendum_praejudicium?')
                return None
                # raise ValueError('--imponendum_praejudicium?')

        if self.in_bcp47_simplex:
            return in_jq(
                bcp47_langtag(
                    self.argparse_args.de_codex,
                ),
                self.argparse_args.quod
            )

        return self.linguacodex.quid()

    def resultatum_in_textum(self):
        """resultatum_in_textum [summary]

        [extended_summary]

        Returns:
            [type]: [description]
        """
        resultatum = self.resultatum()
        if self.error:
            resultatum_error = {
                'error': self.error
            }
            print(in_textum_json(resultatum_error))
            sys.exit(1)

        return in_textum_json(resultatum)


class Simulationem:
    """ [summary]

    [extended_summary]
    """
    # pylint: disable=too-few-public-methods
    argumenta: str = None

    def __init__(self, argumenta):
        """Simulationem initiāle
        """
        self.argumenta = argumenta

    def jq(self, jq_argumenta='.'):  # pylint: disable=invalid-name
        """jq [summary]

        [extended_summary]

        Args:
            jq_argumenta (str, optional): [description]. Defaults to '.'.
        """
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
