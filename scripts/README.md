# tico-19-hxltm scripts

All scripts on this directory can run on any POSIX shell (so somewhat
can be ported to pretty much everywhere). Some require extra additional
command line tools, as per their documentation.

## Run all
- [_run-all-data-scripts.sh](_run-all-data-scripts.sh)

This is the script which runs all data commands in order to rebuild the datasets
from the source TICO-19 order. An fork is also available at
https://github.com/fititnt/tico-19.github.io, which can be used if the
tico-19.github.io gets updated while this one does not.

## data-info
- [scripts/data-info](scripts/data-info)

This directory has extra intermediate files used to prepare the end result.
They are built with the scripts. While not formally documented, they can be
used for a quick look.