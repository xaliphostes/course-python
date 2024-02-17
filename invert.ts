import fs from 'node:fs'

/**
 * Define a vector in 2D (seems useless but very usefull for reading the code)
 */
type Vector = [number, number]

/**
 * The two eigen vectors from a 2-dimensional stress state
 */
type EigenVectors = {
    S1: Vector,
    S3: Vector
}

/**
 * The prefix 'I' stands for Interface.
 */
interface IData {
    /**
     * The normal that characterize the data geometry
     */
    get normal(): Vector

    /**
     * Given a stress state, tells if this data is more or less well oriented
     */
    cost(eigen: EigenVectors): number

    /**
     * Given a stress state, gives the best oriention (for this data) that fit this stress state
     */
    predict(eigen: EigenVectors): Vector

    /**
     * The name of this data (e.g., 'joint', 'stylolite', 'conjugate')
     */
    name(): string
}

/**
 * The interface that must follow a solver for performing stress inversion
 */
interface ISolver {
    addData(filename: string, dataType: string): void
    run(n: number): void
}

/**
 * A design pattern...
 */
class SolverFactory {
    static solverMap_: Map<string, any> = new Map()

    static bind(name: string = '', obj: any): void {
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

    static bind(name: string = '', obj: any): void {
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

// ----------------------------------------------------------

/**
 * Normamlize a 2-dimensional (2D) vector
 */
function normalize(n: Vector): Vector {
    const l = Math.sqrt(n[0] ** 2 + n[1] ** 2)
    return [n[0] / l, n[1] / l]
}

/**
 * Perform the dot product in 2D
 */
const dot = (n1: Vector, n2: Vector): number => n1[0] * n2[0] + n1[1] * n2[1]

/**
 * Perform a linear interpolation between v0 and v1 using t∊[0,1].
 * For t=0, the returned value is v0, and for t=1 the returned value is v1.
 */
const lerp = (v0: number, v1: number, t: number): number => (1 - t) * v0 + t * v1

/**
 * Given (Θ, k), return the two principal directions, σ1 and σ3.
 */
function remoteStress(theta: number, k: number): EigenVectors {
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
    constructor(private n_: Vector) {
    }
    get normal(): Vector {
        return this.n_
    }
    cost(eigen: EigenVectors): number {
        return 1.0 - Math.abs(dot(this.n_, eigen.S1))
    }
    predict(eigen: EigenVectors): Vector {
        return eigen.S1
    }
    name(): string {
        return 'joint'
    }
}
DataFactory.bind('joint', Joint )

class Stylolite implements IData {
    constructor(private n_: Vector) {
    }
    get normal(): Vector {
        return this.n_
    }
    cost(eigen: EigenVectors): number {
        return 1.0 - Math.abs(dot(this.n_, eigen.S3))
    }
    predict(eigen: EigenVectors): Vector {
        return eigen.S3
    }
    name(): string {
        return 'stylolite'
    }
}
DataFactory.bind('stylo', Stylolite )

// ----------------------------------------------------------

/**
 * First implementation of the ISolver interface. This class
 * is still abstract meaning that some (or all) of the methods
 * are not implemented, meaning that we cannot instanciate this class.
 */
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

/**
 * This is a concrete implementation of Solver class. This class implements ALL
 * of the methods, meaning that we can use it (YES!, finally).
 */
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

/**
 * Same as for the MonteCarlo class, we can use it :-)
 */
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

// ----------------------------------------------------------
//                          R U N
// ----------------------------------------------------------

const solver = SolverFactory.create('mc')
if (solver) {
    solver.addData("matelles-joints.txt", "joint")
    solver.addData("matelles-stylolites.txt", "stylo")
    solver.run()
}
