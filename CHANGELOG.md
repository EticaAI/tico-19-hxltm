# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- TODO: this is a placeholder
- `scripts/dtd/tmx14.dtd` from <https://www.gala-global.org/sites/default/files/migrated-pages/docs/tmx14%20%281%29.dtd>

## [1.5.0] - 2021-11-12
### Added
- <https://tico-19-hxltm.etica.ai/> is now the public website.

### Changed
- <https://github.com/EticaAI/tico-19-hxltm> is the (likely) definitive
  repository for this project, as part of the
  [Etica.AI GitHub organization](https://github.com/EticaAI).
  The early draft was bootstrapped on
  <https://github.com/fititnt/tico-19-hxltm> (personal account).

### Fixed
- `data/original/terminology/facebook/{.*-XX.csv -> .*.csv}`: Removed unknown
  language suffix `_XX` / `-XX` used on filenames for Facebook terminology.
  _If this is to mean "no specific region" can be simply omitted when
  exchanging data._:
  - `en_es-XX`, `en_fr-XX`, `en_ja-XX`, `en_nl-XX`, `en_no-XX`, `en_pt-XX`,
    `en_tl-XX`
- `scripts/patch/data-terminology-facebook.diff` for
  `data/original/terminology/facebook/`. As per
  [RFC 4180 -  Common Format and MIME Type for Comma-Separated Values (CSV) Files](https://datatracker.ietf.org/doc/html/rfc4180)
  the manually applied DQUOTE `"` to non-optional fields with data containing
  `,` as text.
- `data/original/terminology/facebook/`: field targetLang data content
  replaced `_` with `-`:
  - Restrict `-` language tags delimiter, as per
    [IETF Best Current Practice 47](https://tools.ietf.org/rfc/bcp/bcp47.txt)
     and common usage in industry.
- `data/original/terminology/facebook/`: field targetLang data content
  removed unknown language suffix `_XX` / `-XX`

## [1.0.0] - 2021-11-11
### Added
- **Fiat lux!**
- Draft of scripts to download data from TICO-19 original sources
- `data/original/terminology/facebook`: TICO-19 terminology from Facebook
  - Uses data from `tico-19/tico-19.github.io/data/terminologies/f_*`, with
    following data normalizations, using as example `f_en-pt_XX.csv` to
    `en_pt-XX.csv`:
    - Restrict `-` language tags delimiter, as per
      [IETF Best Current Practice 47](https://tools.ietf.org/rfc/bcp/bcp47.txt)
      and common usage in industry.
    - Use single `_` for other types of delimiter when necessary. No known
      industry convention on this decision.
      - In the case of language pair on  file names  this means unambiguously
        separating one language code from another.
    - Remove prefix `f_`, since now is inferred from folder path.
- `data/original/terminology/google`: TICO-19 terminology from Google
  - Uses data from `tico-19/tico-19.github.io/data/terminologies/g_*`, with
    following data normalizations, using as example `g_en_pt-BR.csv` to
    `en_pt-BR.csv`:
    - Remove prefix `g_`, since now is inferred from folder path.
