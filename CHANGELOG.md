## Piègeur & mathPiège library changelog

### v0.1.5 (07 January, 2026)
- Added `NullValue = 0`, `ComplexInfinity = inf`, `pi = 3.1415926535897932` in `tempVariable` and `tempValue` lists
- Added 3 custom errors: `NoVariable`, `InvalidCommand`, `InvalidVariable`
- Slightly changed `do[]` function to avoid potential duplicate operators during reading (e.g. `arcsin(` read as `arcsin(` and `sin(`)
- Added 24 trigonometric and hyperbolic operators, `exp()`, `ln()` operators for `do[]` function

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
