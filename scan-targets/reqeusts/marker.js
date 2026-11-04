const fs = require('fs');

fs.writeFileSync('/tmp/supply_chain_demo_marker.txt',
  `simulated malicious action executed at ${new Date().toISOString()}\n`);

console.log('[demo] postinstall script executed — marker written to /tmp/supply_chain_demo_marker.txt');