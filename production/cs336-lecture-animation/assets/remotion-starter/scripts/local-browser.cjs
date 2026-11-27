const {accessSync,statSync,constants}=require('node:fs');
const {delimiter,resolve}=require('node:path');

function usable(file){
  try{accessSync(file,constants.X_OK);return statSync(file).isFile();}catch{return false;}
}
function localBrowser(){
  if(process.env.REMOTION_BROWSER){
    const file=resolve(process.env.REMOTION_BROWSER);
    if(!usable(file))throw Error('REMOTION_BROWSER must point to an executable browser: '+file);
    return file;
  }
  const binaries=['google-chrome','google-chrome-stable','chromium','chromium-browser'];
  for(const dir of (process.env.PATH??'').split(delimiter).filter(Boolean))
    for(const bin of binaries){
      const file=resolve(dir,bin);
      if(usable(file))return file;
    }
  throw Error('No local Chrome/Chromium. Set REMOTION_BROWSER to an existing browser executable.');
}
function ensureFlag(args){
  if(args.some(a=>a==='--browser-executable'||a.startsWith('--browser-executable=')))return args;
  return [...args,'--browser-executable='+localBrowser()];
}
module.exports={localBrowser,ensureFlag};
