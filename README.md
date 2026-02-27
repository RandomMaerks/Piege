<div align="center" style="display: grid; place-items: center;">
  <img src="https://github.com/RandomMaerks/Piege/blob/main/documentation/piege.png" width=13% height=13%>
  <h1>Piège</h1>
  <h3>Repo for the <a href="https://github.com/RandomMaerks/Piege/wiki">Documentation</a> and the Python interpreter</h3>
  <p>Piège v2.1<br>Piègeur v0.3.1 (compatible with Piège v2.1)</p><br>
  <img width="964" height="672" alt="image" src="https://github.com/user-attachments/assets/03300284-7232-48fd-b005-ee81b82c9c80" />
</div>


## Preamble

This is the official repository for the Documentation of the Piège programming language, as well as the Python interpreter Piègeur and math library.

**Piège** /ˈpɪ.eʒ/ is a mathematically-focused interpreted language which is used to compute various sorts of mathematical operations. Piège files have the `.piege` file extension. Check [the wiki](https://github.com/RandomMaerks/Piege/wiki) for more details.

**Piègeur** /pɪ.ˈe.ʒœ/ is the official interpreter for Piège as well as the integrated development environment (IDE) for the language. The interpreter includes by default `mathPiege.py`, a math library, and `visualiser.py`, a library for drawing graphs and visualising numbers.

## Small warning

Firstly, the build of Piègeur IDE is only available for Windows as I only have a Windows machine. If you want to use it on Linux or MacOS, please build it yourself.

Secondly, the interpreter and the language itself are not meant for serious business. Tinker around, write some stuff, and have fun. You're also welcome to give feedback and make changes if necessary.

## Use Piègeur & code with Piège

Versions of Piègeur after v0.3.0 now have an IDE as a portable .exe application.

To use the interpreter, you can either download the binary from the release page or build it yourself. Make sure you have all the required dependencies (see `requirements`).

Upon opening the app, you can immediately start writing your code in the code editor and run it without needing to save. Though, when you do need to save, your program will be saved as a `.piege` file which you can reopen anytime later. Any output from the interpreter will either go to the specified output file or the interpreter itself, depending on how you set up the I/O functions.

## Build Piègeur

First, install all the dependencies in `requirements`.

Next, use PyInstaller to compile the program:
```
py -m PyInstaller --onefile --noconsole --i=resources/piege.ico --version-file=version.txt Piegeur.py
``` 
Instead of using the `--onefile` flag, you can also use the `--onedir` flag to compile into a folder instead:
```
py -m PyInstaller --onedir --noconsole --i=resources/piege.ico --version-file=version.txt Piegeur.py
``` 
Make sure the current directory is `../source/`.

There should be a `build` and a `dist` folder. The executable/binary file will be placed in the `dist` folder, and the file type will depend on your operating system (on Windows, it's an `.exe` file).
