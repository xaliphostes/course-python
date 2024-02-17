const fs = require('fs')

function normalize(n) {
    const l = Math.sqrt(n[0] ** 2 + n[1] ** 2)
    return [n[0] / l, n[1] / l]
}

const dot = (n1, n2) => n1[0] * n2[0] + n1[1] * n2[1]

const lerp = (v0, v1, t) => (1 - t) * v0 + t * v1

function remoteStress(theta, k) {
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

const costJoint = (n, eigen) => 1.0 - Math.abs(dot(n, eigen.S1))

const costStylo = (n, eigen) => 1.0 - Math.abs(dot(n, eigen.S3))

function mc(data, n) {
    let theta = 0
    let k = 0
    let cost = Number.POSITIVE_INFINITY
    for (let i=0; i<n; ++i) {
        const THETA = lerp(0, 180, Math.random())
        const K = lerp(0, 1, Math.random())
        const remote = remoteStress(THETA, K)
        const c = data.reduce( (c, d) => c + d.cost(d.n, remote), 0) / data.length
        if (c < cost) {
            cost = c
            theta = THETA
            k = K
            console.log(theta, k, c)
        }
    }
}

function generateDomain(data, n) {
    const z = new Array(n*n).fill(0)
    let l = 0
    for (let i = 0; i < n; ++i) {
        const k = lerp(0, 1, i/(n-1))
        for (let j = 0; j < n; ++j) {
            const theta = lerp(0, 180, j/(n-1))
            const remote = remoteStress(theta, k)
            z[l++] = data.reduce((c, d) => c + d.cost(d.n, remote), 0) / data.length
        }
    }

    return z
}

// -------------------------------------------

const data = []

function addData(file, fct) {
    fs.readFileSync(file, 'utf8').split('\n').forEach( line => data.push({
        n: line.split(' ').map( v => parseFloat(v)),
        cost: fct
    }) )
}

addData("matelles-joints.txt", costJoint)
addData("matelles-stylolites.txt", costStylo)
mc(data, 10000)

generateDomain(data, 50)
