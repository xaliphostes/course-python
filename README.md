# Courses on stress inversion

Provide 4 ways of programming stress inversion:
- using JavaScript and procedural programming (~80 lines of code)
- using Python, procedural programming and object oriented programming (150-200 lines of code)
- using TypeScript, object oriented and procedural programming (~330 lines of code)
- in the browser using `index.html`

Folder `inversion` contains the same classes as in `invert-class.py`, but split the code into multiple files, and introduces the notion of data factory.

## Installation
- [PyCharm IDE, Community Edition](https://www.jetbrains.com/pycharm/download/) for python
- [node](https://nodejs.org/en) for JavaScript
- [deno](https://deno.com/) for TypeScript
- [Visual Studio Code](https://code.visualstudio.com/) (for JavaScript and TypeScript)


## Running
### In Python
Directly from PyCharm by selecting either `invert-function.py` or `invert-class.py`.

### In JavaScript (using node)
```sh
node invert.js
```

### In TypeScript (using deno).
```sh
deno run invert.ts
```
Deno will ask you the permission to read the two files from your folder, and will display:
```
⚠️  Deno requests read access to "matelles-joints.txt".
├ Requested by `Deno.readFileSync()` API.
├ Run again with --allow-read to bypass this prompt.
└ Allow? [y/n/A] (y = yes, allow; n = no, deny; A = allow all read permissions) >
```
To bypass this prompt, prefer to use `--allow-read`:
```sh
deno run --allow-read invert.ts 
```

## Running in the browser
The index.html file embeds JavaScript code to represent the cost domain,
including both the code and data from Les Matelles.

---
<center>
Simply <a href="https://xaliphostes.github.io/course-stress-inv-3/"><b><b>click here</b></a></b> to display the cost domain.
</center>

---
