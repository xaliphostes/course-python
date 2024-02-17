# Courses on stress inversion version 3

## Installation
- Python 3.11 min
- node
- deno


## Running
- In Python
```sh
python3 invert.py
```
- In JavaScript (using node)
```sh
node invert.js
```
- In TypeScript (using deno)
Info: Deno will ask you the permission to read the two files from your folder.
```sh
deno run invert.ts
```

## Running in the browser
The JavaScript code is embedded into a index.html file allowing the representation of the cost domain.
This file includes not only the code, but also the data form Les Matelles.

Simply double-click on `index.html` to display the cost domain.

<br><br><br><br><br>

## Testing a GUI using deno
```sh
deno run --allow-all --unstable test-gui.ts  
```
