# Third-party code

`antlr3/` is the ANTLR 3 runtime for Python 3 (version 3.4, `antlr3.__version__`), which the
generated protocol parser (`Parser/ProtoCCLexer.py`, `Parser/ProtoCCParser.py`) needs. It is
included unmodified because the package on PyPI (`antlr3-python-runtime`) is the Python 2
runtime. It is distributed under the BSD licence of ANTLR 3 (Copyright (c) 2005-2012 Terence
Parr), reproduced at the top of each of its files.
