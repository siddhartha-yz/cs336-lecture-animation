/* Scope the Studio's editable project server to the machine running it. */
const server = require('node:net').Server.prototype;
const listen = server.listen;
const target = process.argv.find((s)=> s.startsWith('--port='));
const port = target ? Number(target.slice(7)) : 3095;
if (!Number.isInteger(port) || port < 1024 || port > 65535) throw Error('Invalid Studio port');
server.listen=function(...args) {
  if (args[0]?.port===port) args[0]={...args[0],host:'127.0.0.1'};
  return listen.apply(this,args);
};
const cli=require('node:path').resolve(__dirname,'../node_modules/@remotion/cli/remotion-cli.js');
process.argv=[process.argv[0],cli,'studio','src/index.ts','--no-open',`--port=${port}`];
require(cli);
