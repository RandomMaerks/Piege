<div align="center" style="display: grid; place-items: center;">
<h1>Piègeur</h1>
<h3>A Python interpreter for Piège</h3>
<p>v0.1.4 (04 January, 2026)</p><br>
</div>


## Preamble
This is the official repository of the Python interpreter and math library for the Piège programming language.

**Piège** /ˈpɪ.eʒ/ is a mathematically-focused interpreted language which is used to compute various sorts of mathematical operations.

Piège files have the `.piege` file extension. The interpreter is the `piegeur.py` file. The interpreter also uses `mathPiege.py` as a library for math operations.

For detailed information about syntaxes and sample codes of this language, [read this document](https://docs.google.com/document/d/1WAAu7p1CHTn9_E9xxxhv4B_jBKVATX67ZG5KDJ2ysMM).


## Version history

### v0.1.4 (04 January, 2026)
- Released project to GitHub
- Changed `interpreter.py` file name to `piegeur.py`

### v0.1.3 (04 January, 2026)
- Changed `moveCursor[]` of version 0.1.2 to `setCursor[]`
- Changed `deleteCode[]` of version 0.1.2 to `ignoreIndex[]`
- Added a new function concept: `moveCursor[]`
- Implemented `moveCursor[]`, `ignoreIndex[]`, `endCode[]`
- Changed `print[]` parameter separator from `,` to `;`
- Added parameter type to `moveCursor[]` and `setCursor[]`
- Removed function `loop[]` due to redundancy

### v0.1.2 (03 January, 2026)
- Added 6 new function concepts: `deleteVar[]`, `getIndex[]`, `moveCursor[]`, `loop[]`, `deleteCode[]`, `endCode[]`
- Implemented `deleteVar[]`, `getIndex[]`, `moveCursor[]`
- Changed variable name detection

### v0.1.1 (02 January, 2026)
- Added a new function: `print[]`
- Added variable name detection

### v0.1.0 (01 January, 2026)
- Created `interpreter.py`, `mathPiege.py`
- Added 7 new functions: `io{}`, `op{}`, `input[]`, `output[]`, `do[]`, `solve[]`, `return[]`
- Implemented `io{}`, `op{}`, `output[]`, `do[]`, `return[]`
