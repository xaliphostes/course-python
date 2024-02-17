// const fs = require('fs')
import fs from 'node:fs'

// ----------------------------------------------------------

type Vec = [number, number]

type Eigen = {
    S1: Vec,
    S3: Vec
}

type CostFunction = (n: Vec, eigen: Eigen) => number

type Data = {
    n: Vec,
    cost: CostFunction
}

interface ISolver {
    addData(filename: string, costFunction: string): void
    run(n: number): void
}

class SolverFactory {
    static bind(name: string = '', obj: any): void {
        name.length === 0 ? map_.set(obj.name, obj) : map_.set(name, obj)
    }

    static create(name: string, params: any = undefined): ISolver {
        const M = map_.get(name)
        if (M) {
            return new M(params)
        }
        return undefined
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

const dataMap: Map<string, CostFunction> = new Map()
class DataFactory {
    static bind(name: string, cost: CostFunction) {
        dataMap.set(name, cost)
    }

    static resolve(name: string): CostFunction | undefined {
        if (dataMap.has(name)) {
            return dataMap.get(name)
        }
        return undefined
    }
}

DataFactory.bind('joint', (n: Vec, eigen: Eigen) => 1.0 - Math.abs(dot(n, eigen.S1)) )
DataFactory.bind('stylo', (n: Vec, eigen: Eigen) => 1.0 - Math.abs(dot(n, eigen.S3)) )

const map_: Map<string, any> = new Map()

abstract class Solver implements ISolver {
    protected data: Data[] = []

    abstract run(n: number): void

    addData(filename: string, costFunction: string): void {
        const costFct = DataFactory.resolve(costFunction)
        if (costFct !== undefined) {
            fs.readFileSync(filename, 'utf8').split('\n').forEach((line: string) => this.data.push({
                n: line.split(' ').map(v => parseFloat(v)) as Vec,
                cost: costFct
            }))
        }
        else {
            throw `Cost function named ${costFunction} does not exist`
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
            const c = this.data.reduce((c, d) => c + d.cost(d.n, remote), 0) / this.data.length
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

// -------------------------------------------

const solver = SolverFactory.create('regular')
if (solver) {
    solver.addData("matelles-joints.txt", "joint")
    solver.addData("matelles-stylolites.txt", "stylo")
    solver.run()
}