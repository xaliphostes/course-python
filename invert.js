/**
 * PROCEDURAL programming in JavaScript
 */

const fs = require('fs')

// Normalize a vector
function normalize(n) {
    const l = Math.sqrt(n[0] ** 2 + n[1] ** 2)
    return [n[0] / l, n[1] / l]
}

// The dot product of two vectors
function dot(n1, n2) {
    return n1[0] * n2[0] + n1[1] * n2[1]
}

// Linear interpolation between v0 and v1. t must be in [0,1]
function lerp(v0, v1, t) {
    return (1 - t) * v0 + t * v1
}

// Contruct a stress according to (theta, k) tensor and determine
// the 2 principal directions
function principalDirections(theta, k) {
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

function costJoint(n, eigen) {
    return 1.0 - Math.abs(dot(n, eigen.S1))
}

function costStylo(n, eigen) {
    return 1.0 - Math.abs(dot(n, eigen.S3))
}

// Monte Carlo simulation (i.e., random)
function mc(data, n) {
    let theta = 0, k = 0, cost = 1e9
    for (let i=0; i<n; ++i) {
        const THETA = lerp(0, 180, Math.random()), K = lerp(0, 1, Math.random()), remote = principalDirections(THETA, K)
        const c = data.reduce( (c, d) => c + d.cost(d.n, remote), 0) / data.length
        if (c < cost) {
            cost = c; theta = THETA; k = K
            console.log(theta, k, c)
        }
    }
}

// --------------------------------------------------------
//                          R U N
// --------------------------------------------------------

const data = []

function addData(file, fct) {
    fs.readFileSync(file, 'utf8')
      .split('\n')
      .forEach( line => data.push({
        n: line.split(' ').map( v => parseFloat(v)),
        cost: fct
    }) )
}

addData("matelles-joints.txt", costJoint)
addData("matelles-stylolites.txt", costStylo)
mc(data, 10000)
