# ipynb_output_filter
Script for stripping output from ipython/jupyter scripts.

Originally from http://stackoverflow.com/questions/18734739/using-ipython-notebooks-under-version-control/20844506

## Usage

Let us assume that the script is saved to ```~/bin/ipynb_output_filter.py```, and that it is executable (otherwise: ```chmod +x ~/bin/ipynb_output_filter.py```).

Then, create the file ```~/.gitattributes``` with the following content

```file
*.ipynb    filter=dropoutput_ipynb
```

and run the following commands:

```sh
git config --global core.attributesfile ~/.gitattributes
git config --global filter.dropoutput_ipynb.clean ~/bin/ipynb_output_filter.py
git config --global filter.dropoutput_ipynb.smudge cat
```

### Disable/enable on specific repo(s)

To disable the output filtering for a specific git repository, simply create inside it a file ```.git/info/attributes```, with

```file
**.ipynb filter=
```

as content. Clearly, in the same way it is possible to apply filtering //only// on specific repo(s).
