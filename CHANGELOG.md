# Changelog

## [Unreleased]
### Added
- TODO: Fix Facebook terminology usage of "_XX" as suffix

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
      an common usage in industry.
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