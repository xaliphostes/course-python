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

---
<center>
Simply <a href="https://xaliphostes.github.io/course-stress-inv-3/"><b><b>click here</b></a></b> to display the cost domain.
</center>

---     

<br><br><br><br><br>

## Testing a GUI using deno
```sh
deno run --allow-all --unstable test-gui.ts  
```
