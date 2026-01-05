<div align="center" style="display: grid; place-items: center;">
<h1>Piège</h1>
<h3>Repo for the Documentation and the official Python interpreter, Piègeur</h3>
<p>Piègeur v0.1.4, Piège v1.0</p><br>
</div>


## Preamble
This is the official repository for the Documentation of the Piège programming language, as well as the Python interpreter Piègeur and math library.

**Piège** /ˈpɪ.eʒ/ is a mathematically-focused interpreted language which is used to compute various sorts of mathematical operations. Piège files have the `.piege` file extension. Check the wiki for more details.

**Piègeur** /pɪ.ˈe.ʒœ/ is the official Python interpreter for Piège, which is the `piegeur.py` file. The interpreter also uses `mathPiege.py` as a custom-made library for math operations. Note that all input values will be converted to float.

**Small warning**: The interpreter and the language itself are made by me, an extremely nooby programmer. Tinker around, have fun, and please don't use these things in actual projects. You're also welcome to give feedback and make changes if necessary.


## Version history (Piège)

### v1.0 (05 January, 2026)
- Released documentation to GitHub

### pre-1.0 (04 Janurary, 2026)
- Added functions: `io{}`, `op{}`, `input[]`, `output[]`, `do[]`, `solve[]`, `return[]`, `deleteVar[]`, `getIndex[]`, `setCursor[]`, `moveCursor[]`, `loop[]`, `ignoreIndex[]`, `endCode[]`


## Version history (Piègeur)

### v0.1.4 (04 January, 2026)
- Released project to GitHub
- Changed `interpreter.py` file name to `piegeur.py`

### v0.1.3 (04 January, 2026)
- Changed `moveCursor[]` of version 0.1.2 to `setCursor[]`
- Changed `deleteCode[]` of version 0.1.2 to `ignoreIndex[]`
- Added a new function concept: `moveCursor[]`
- Implemented `moveCursor[]`, `ignoreIndex[]`, `endCode[]`
- Changed `print[]` parameter separator from `,` to `;`
- Added parameter `type` to `moveCursor[]` and `setCursor[]`
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
