# Courses on stress inversion version 3

## Installation
- Python 3.11 min
- node
- deno


## Running
### In Python
```sh
python3 invert.py
```
or if you only have python 3 installed:
```sh
python invert.py
```

### In JavaScript (using node)
```sh
node invert.js
```

### In TypeScript (using deno). Deno will ask you the permission to read the two files from your folder.
```sh
deno run invert.ts
```
This will prompt you:
```
⚠️  Deno requests read access to "matelles-joints.txt".
├ Requested by `Deno.readFileSync()` API.
├ Run again with --allow-read to bypass this prompt.
└ Allow? [y/n/A] (y = yes, allow; n = no, deny; A = allow all read permissions) >
```
To bypass this prompt, prefer to use:
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

<br><br><br><br><br>

## Testing a GUI using deno
```sh
deno run --allow-all --unstable test-gui.ts  
```
