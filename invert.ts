import fs from 'node:fs'

type Vec = [number, number]

type Eigen = {
    S1: Vec,
    S3: Vec
}

interface IData {
    get normal(): Vec
    cost(eigen: Eigen): number
    predict(eigen: Eigen): Vec
    name(): string
}

interface ISolver {
    addData(filename: string, dataType: string): void
    run(n: number): void
}

const solverMap_: Map<string, any> = new Map()
class SolverFactory {
    static bind(name: string = '', obj: any): void {
        name.length === 0 ? solverMap_.set(obj.name, obj) : solverMap_.set(name, obj)
    }

    static create(name: string, params: any = undefined): ISolver {
        const M = solverMap_.get(name)
        if (M) {
            return new M(params)
        }
        return undefined
    }

    static has(name: string): boolean {
        return solverMap_.has(name)
    }
}

const dataMap_: Map<string, any> = new Map()
class DataFactory {
    static bind(name: string = '', obj: any): void {
        name.length === 0 ? dataMap_.set(obj.name, obj) : dataMap_.set(name, obj)
    }

    static create(name: string, params: any = undefined): IData {
        const M = dataMap_.get(name)
        if (M) {
            return new M(params)
        }
        return undefined
    }

    static has(name: string): boolean {
        return dataMap_.has(name)
    }
}

// ----------------------------------------------------------

function normalize(n: Vec): Vec {
    const l = Math.sqrt(n[0] ** 2 + n[1] ** 2)
    return [n[0] / l, n[1] / l]
}

const dot = (n1: Vec, n2: Vec): number => n1[0] * n2[0] + n1[1] * n2[1]

const lerp = (v0: number, v1: number, t: number): number => (1 - t) * v0 + t * v1

function remoteStress(theta: number, k: number): Eigen {
    const a = theta * Math.PI / 180.0
    const c = Math.cos(a)
    const s = Math.sin(a)
    const xx = k * c * c + s * s
    const xy = (k - 1) * c * s
    const yy = k * s * s + c * c
    const trace = xx + yy
    const discri = Math.sqrt(trace * trace - 4 * (xx * yy - xy * xy))
    // Decreasing order according to the eigen values
    return {
        S1: normalize([xy, (trace + discri) / 2 - xx]),
        S3: normalize([xy, (trace - discri) / 2 - xx])
    }
}

// ----------------------------------------------------------

class Joint implements IData {
    constructor(private n_: Vec) {
    }
    get normal(): Vec {
        return this.n_
    }
    cost(eigen: Eigen): number {
        return 1.0 - Math.abs(dot(this.n_, eigen.S1))
    }
    predict(eigen: Eigen): Vec {
        return eigen.S1
    }
    name(): string {
        return 'joint'
    }
}
DataFactory.bind('joint', Joint )

class Stylolite implements IData {
    constructor(private n_: Vec) {
    }
    get normal(): Vec {
        return this.n_
    }
    cost(eigen: Eigen): number {
        return 1.0 - Math.abs(dot(this.n_, eigen.S3))
    }
    predict(eigen: Eigen): Vec {
        return eigen.S3
    }
    name(): string {
        return 'stylolite'
    }
}
DataFactory.bind('stylo', Stylolite )

// ----------------------------------------------------------

abstract class Solver implements ISolver {
    protected data: Data[] = []

    abstract run(n: number): void

    addData(filename: string, dataType: string): void {
        if ( DataFactory.has(dataType)) {
            fs.readFileSync(filename, 'utf8').split('\n').forEach((line: string) => {
                const n = line.split(' ').map(v => parseFloat(v))
                this.data.push(DataFactory.create(dataType, n))
            })
        }
        else {
            throw `No Data type named ${dataType}!`
        }
    }
}

class MonteCarlo extends Solver {
    run(n = 5000): void {
        let theta = 0
        let k = 0
        let cost = Number.POSITIVE_INFINITY
        for (let i = 0; i < n; ++i) {
            const THETA = lerp(0, 180, Math.random())
            const K = lerp(0, 1, Math.random())
            const remote = remoteStress(THETA, K)
            const c = this.data.reduce((c, d) => c + d.cost(remote), 0) / this.data.length
            if (c < cost) {
                cost = c
                theta = THETA
                k = K
                console.log(i, theta, k, c)
            }
        }
    }
}
SolverFactory.bind('mc', MonteCarlo)

class Regular extends Solver {
    run(n = 50): void {
        let theta = 0
        let k = 0
        let cost = Number.POSITIVE_INFINITY
        for (let i = 0; i < n; ++i) {
            const K = lerp(0, 1, i/(n-1))
            for (let j = 0; j < n; ++j) {
                const THETA = lerp(0, 180, j/(n-1))
                const remote = remoteStress(THETA, K)
                const c = this.data.reduce((c, d) => c + d.cost(d.n, remote), 0) / this.data.length
                if (c < cost) {
                    cost = c
                    theta = THETA
                    k = K
                    console.log(i*n+j, theta, k, c)
                }
            }
        }
    }
}
SolverFactory.bind('regular', Regular)

function generateDomain(data: Data[], n: number): number[] {
    const z = new Array(n*n).fill(0)
    let l = 0
    for (let i = 0; i < n; ++i) {
        const k = lerp(0, 1, i/(n-1))
        for (let j = 0; j < n; ++j) {
            const theta = lerp(0, 180, j/(n-1))
            const remote = remoteStress(theta, k)
            z[l++] = data.reduce((c, d) => c + d.cost(remote), 0) / data.length
        }
    }

    return z
}

// ----------------------------------------------------------
//                          R U N
// ----------------------------------------------------------

const solver = SolverFactory.create('mc')
if (solver) {
    solver.addData("matelles-joints.txt", "joint")
    solver.addData("matelles-stylolites.txt", "stylo")
    solver.run()
}

// const domain = generateDomain(solver.data, 50)
