# Courses on stress inversion version 3

Provide three ways of programming stress inversion:
- using JavaScript and procedural programming (~80 lines of code)
- using Python, procedural programming and functional programming (~110 lines of code)
- using TypeScript, object oriented and procedural programming (~330 lines of code)

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

# Programming tips

## Thinking without genericity
Using factory (one of the design pattern) wthout "genericity" leads to the following two classes which are equivalent:

```ts
class SolverFactory {
    static solverMap_: Map<string, any> = new Map()

    static register(name: string = '', obj: any): void {
        name.length === 0 ? SolverFactory.solverMap_.set(obj.name, obj) : SolverFactory.solverMap_.set(name, obj)
    }

    static create(name: string, params: any = undefined): ISolver {
        const M = SolverFactory.solverMap_.get(name)
        if (M) {
            return new M(params)
        }
        return undefined
    }

    static has(name: string): boolean {
        return SolverFactory.solverMap_.has(name)
    }
}

class DataFactory {
    static dataMap_: Map<string, any> = new Map()

    static register(name: string = '', obj: any): void {
        name.length === 0 ? DataFactory.dataMap_.set(obj.name, obj) : DataFactory.dataMap_.set(name, obj)
    }

    static create(name: string, params: any = undefined): IData {
        const M = DataFactory.dataMap_.get(name)
        if (M) {
            return new M(params)
        }
        return undefined
    }

    static has(name: string): boolean {
        return DataFactory.dataMap_.has(name)
    }
}
```

## Now, thinking with genericity
Write once, use many times to define several classes
```ts
// The skeleton
class GenericFactory<T> {
    static map_: Map<string, any> = new Map()

    static register(name: string = '', obj: any): void {
        name.length === 0 ? GenericFactory.map_.set(obj.name, obj) : GenericFactory.map_.set(name, obj)
    }

    static create(name: string, params: any = undefined): T {
        const M = GenericFactory.map_.get(name)
        if (M) return new M(params)
        return undefined
    }

    static has(name: string): boolean {
        return GenericFactory.map_.has(name)
    }

    static names() {
        return Array.from(GenericFactory.map_)
    }
}
```
Use it. Create two factories, one for the solvers and one for the datas
```ts
const SolverFactory = GenericFactory<ISolver>

const DataFactory = GenericFactory<IData>
```