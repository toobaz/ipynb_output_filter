#!/usr/bin/env python

import sys

try:
    runarg_idx = sys.argv.index('--rundir')
    rundir = sys.argv[runarg_idx+1]
    import os
    os.chdir(os.path.expanduser(rundir))
except ValueError:
    pass

version = None

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding('utf8')

try:
    # Jupyter
    from jupyter_nbformat import reads, write
except ImportError:
    try:
        # New IPython
        from nbformat import reads, write
    except ImportError:
        # Old IPython
        from IPython.nbformat.current import reads, write
        version = 'json'

to_parse = sys.stdin.read()

if not version:
    import json
    json_in = json.loads(to_parse)
    version = json_in['nbformat']

json_in = reads(to_parse, version)

if hasattr(json_in, 'worksheets'):
    # IPython
    sheets = json_in.worksheets
else:
    # Jupyter
    sheets = [json_in]

for sheet in sheets:
    for cell in sheet.cells:
        if "outputs" in cell:
            cell.outputs = []
        for field in ("prompt_number", "execution_number"):
            if field in cell:
                del cell[field]
        for field in ("execution_count",):
            if field in cell:
                cell[field] = None

        if "metadata" in cell:
            for field in ("collapsed", "scrolled"):
                if field in cell.metadata:
                    del cell.metadata[field]

    if hasattr(sheet.metadata, "widgets"):
        del sheet.metadata["widgets"]

    if hasattr(sheet.metadata, "language_info"):
        if hasattr(sheet.metadata.language_info, "version"):
            del sheet.metadata.language_info["version"]

if 'signature' in json_in.metadata:
    json_in.metadata['signature'] = ""

write(json_in, sys.stdout, version)
