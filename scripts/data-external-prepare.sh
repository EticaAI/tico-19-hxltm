#!/bin/sh
# ==============================================================================
#
#          FILE:  data-external-prepare.sh
#
#         USAGE:  ./scripts/data-external-prepare.sh
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - POSIX Shell or better
#
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v1.0
#       CREATED:  2021-11-18 06:59 UTC started
# ==============================================================================
set -e

PWD_NOW=$(pwd)


# https://iso639-3.sil.org/code_tables/download_tables
if [ ! -f scripts/data-external/iso-639-3.tab ]; then
    curl https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab --output scripts/data-external/iso-639-3.tab
    mlr --itsv --ocsv cat scripts/data-external/iso-639-3.tab > scripts/data-external/iso-639-3.csv
    head scripts/data-external/iso-639-3.csv > scripts/data-external/iso-639-3.sample.csv
    head scripts/data-external/iso-639-3.tab > scripts/data-external/iso-639-3.sample.tab
fi
if [ ! -f scripts/data-external/iso15924.txt ]; then
    curl https://www.unicode.org/iso15924/iso15924.txt --output scripts/data-external/iso15924.txt
    tail -n +8 scripts/data-external/iso15924.txt > scripts/data-external/iso15924_no-comments.txt
    # sed 's/;/|/g' < scripts/data-external/iso15924_no-comments.txt > scripts/data-external/iso15924_no-comments-pipe.txt
    sed 's/;/\t/g' < scripts/data-external/iso15924_no-comments.txt > scripts/data-external/iso15924_no-comments.tsv
    mlr --itsv --ocsv \
      --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date \
      scripts/data-external/iso15924_no-comments.tsv \
      > scripts/data-external/iso15924.csv

    head scripts/data-external/iso15924.csv > scripts/data-external/iso15924.sample.csv
    head scripts/data-external/iso15924.txt > scripts/data-external/iso15924.sample.txt
fi

if [ ! -f scripts/data-external/cldr/likelySubtags.json ]; then
    curl https://raw.githubusercontent.com/unicode-org/cldr-json/main/cldr-json/cldr-core/supplemental/likelySubtags.json --output scripts/data-external/cldr/likelySubtags.json
    head -n 15 scripts/data-external/cldr/likelySubtags.json > scripts/data-external/cldr/likelySubtags.sample.json
fi

if [ ! -f scripts/data-external/cldr/aliases.json ]; then
    curl https://raw.githubusercontent.com/unicode-org/cldr-json/main/cldr-json/cldr-core/supplemental/aliases.json --output scripts/data-external/cldr/aliases.json
    head -n 15 scripts/data-external/cldr/likelySubtags.json > scripts/data-external/cldr/aliases.sample.json
fi

# https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-core/scriptMetadata.json

# mlr --irs '|' --implicit-csv-header cat scripts/data-external/iso15924_no-comments-pipe.txt

# mlr --itsv --ocsv cat scripts/data-external/iso15924_no-comments.tsv
# mlr --itsv --ocsv \
#   --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date \
#   scripts/data-external/iso15924_no-comments.tsv \
#   > scripts/data-external/iso15924.csv

# mlr --itsv --ocsv cat scripts/data-external/iso-639-3.tab > scripts/data-external/iso-639-3.csv


# mlr --irs ';' cat scripts/data-external/iso15924_no-comments.txt
# mlr --irs ';' --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924_no-comments.txt
# mlr --opprint  --irs ';' --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924_no-comments.txt
# mlr --opprint  --irs ";" --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924_no-comments.txt


# mlr --icsv --ocsv --irs ';' cat scripts/data-external/iso15924_no-comments.txt
# mlr --irs ';' cat scripts/data-external/iso15924_no-comments.txt



# mlr --irs ';' --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924_no-comments.txt
# mlr --csv  --irs ';' --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924_no-comments.txt

# mlr --irs ';' --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924_no-comments.txt
# https://www.unicode.org/iso15924/iso15924.txt



# # mlr --csv skip-trivial-records --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date cat scripts/data-external/iso15924.txt
# # mlr --csv skip-trivial-records --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924.txt

# tail -n +6 scripts/data-external/iso15924.txt


# mlr --csv --irs ';' --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924.txt
# mlr --csv --irs ';' --implicit-csv-header scripts/data-external/iso15924.txt
# mlr --csv --ocsv --irs ';' --skip-comments --implicit-csv-header cat scripts/data-external/iso15924.txt

# mlr --tsv --irs ';' --skip-comments --implicit-csv-header cat scripts/data-external/iso15924.txt
# mlr --csv --irs ';' --skip-comments --implicit-csv-header cat scripts/data-external/iso15924.txt

# mlr --csv --irs ';' skip-trivial-records --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924.txt
# mlr --irs ';' --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924.txt
# mlr --icsv --irs ';' --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924.txt
# mlr --icsv --opprint --irs ';' --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924.txt
# mlr --icsv --ojson --irs ';' --pass-comments --implicit-csv-header label code_alpha,code_num,name_en,name_fr,pva,unicode_version,date scripts/data-external/iso15924.txt

# NOTE: the https://github.com/datasets/language-codes needs update.

# https://github.com/datasets/language-code
# if [ ! -d "scripts/language-codes-git" ]; then
#     git clone https://github.com/datasets/language-codes.git scripts/language-codes-git
# fi

# cd scripts/language-codes-git

# ./scripts/language-codes-git/language-codes.sh

# wget http://www.unicode.org/Public/cldr/latest/core.zip

# cd "$PWD_NOW"

echo "Okay!"