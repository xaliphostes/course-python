# Courses on stress inversion

Provide 3 ways of programming stress inversion using Python
- [invert-1.py](invert-1.py): Beurk programming for small project
- [invert-2.py](invert-2.py): Procedural programming
- [invert-3.py](invert-3.py): Object oriented programming (150-200 lines of code). Folder [inversion](inversion) contains the same classes, but split the code into multiple files, and introduces the notion of data factory.

## Installation
- [Spyder](https://www.spyder-ide.org)
- [PyCharm IDE, Community Edition](https://www.jetbrains.com/pycharm/download/)
- [Visual Studio Code](https://code.visualstudio.com/)

## Running
Directly from PyCharm/Spyder by selecting either [invert-1.py](invert-1.py), [invert-2.py](invert-2.py) or [invert-3.py](invert-3.py).

## Others folders
1. In folder [others](./others/), you will find several scripts such as:
   - [normal-shear-stress](others/normal-shear-stress.py)
   - [plot-costs](others/plot-costs.py)
   - [plot-fct](others/plot-fct.py)
   - [principal-directions](others/principal-directions.py)

2. In folder [data](./data/), you will find the Matelles data (joints and stylolites). Each line represents the 2D normal to a fracture (joint or stylolite)

3. Folder [inversion](inversion) contains the same classes as in [invert-3.py](invert-3.py), but the code is splitted into multiple files, and we introduces the notion of data factory.

4. Folder [js](./js/) provide three JavaScript version of the inversion procedure: on running with [node](https://nodejs.org/en) ([invert.js](./js/invert.js)), one with [deno](https://deno.com) ([invert.ts](./js/invert.ts)) and one that is running online ([index.html](./js/index.html))