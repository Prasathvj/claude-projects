// Render Bit SVG strings for the Python generators: stdin = JSON list of BIT.render options, stdout = JSON list of SVG strings.
require('../hf/host/bit.js');
let s = ''; process.stdin.on('data', (d) => (s += d)).on('end', () => process.stdout.write(JSON.stringify(JSON.parse(s).map((o) => globalThis.BIT.render(o)))));
