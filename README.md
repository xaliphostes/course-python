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
The index.html file embeds JavaScript code to represent the cost domain,
including both the code and data from Les Matelles.

Simply double-click on `index.html` to display the cost domain, or <a href="https://xaliphostes.github.io/course-stress-inv-3/"><b>click here</b></a> to directly run the code.

<button name="button" onclick="https://xaliphostes.github.io/course-stress-inv-3/">Run me</button>
        

<br><br><br><br><br>

## Testing a GUI using deno
```sh
deno run --allow-all --unstable test-gui.ts  
```
