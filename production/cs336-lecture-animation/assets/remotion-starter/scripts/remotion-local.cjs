const {resolve}=require('node:path');
const {ensureFlag}=require('./local-browser.cjs');
const cli=resolve(__dirname,'../node_modules/@remotion/cli/remotion-cli.js');
process.argv=[process.argv[0],cli,...ensureFlag(process.argv.slice(2))];
require(cli);
