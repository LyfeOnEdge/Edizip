# Edizip
Python3 module / script for generating .edz style archives.

```
usage: edizip.py [-h] [-o OUTPUT] [-d] [-c] [-m MAGIC] target

positional arguments:
  target                Target dir to archive

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        edizip output location, defaults to
                        `target/target.edz` if not set
  -d, --decompress      decompress file, target becomes archive and output
                        becomes the target output directory. Will decompress
                        in parent dir of archive if output dir not specified.
  -c, --check           Verifies file header is accurate, pass an integer
                        representation of to --magic if checking for a file
                        with non-standard magic
  -m MAGIC, --magic MAGIC
                        Magic to use in header.
```