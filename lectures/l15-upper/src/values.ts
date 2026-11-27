export const len=(a:{length:number})=>a.length;
export const sum=(values: Iterable<number|boolean>)=>Array.from(values).reduce<number>((t,v)=>t+Number(v),0);
export const min=(...a:(number|number[])[])=>Math.min(...a.flat());
export const max=(...a:(number|number[])[])=>Math.max(...a.flat());
export const at=<T>(a:Record<PropertyKey,T>|ArrayLike<T>,key:PropertyKey):T=>{
  const k=typeof key==='number'&&key<0&&typeof a.length==='number'? Number(a.length)+key:key;
  return (a as Record<PropertyKey,T>)[k];
};
export const slice=<T>(value:T[]|string,from?:number,to?:number,step=1):T[]|string=>{
  if(step===1)return value.slice(from,to);
  if(step===0)throw Error('A slice must advance');
  const end=value.length;const a=typeof value==='string'?Array.from(value):value;
  const index=(v:number)=>v<0?end+v:v;
  const result:(T|string)[]=[];
  if(step>0){for(let j=Math.max(0,index(from??0));j<Math.min(end,index(to??end));j+=step)result.push(a[j]);}
  else {for(let j=Math.min(end-1,index(from??end-1));j>(to===undefined?-1:index(to));j+=step)result.push(a[j]);}
  return typeof value==='string'?result.join(''):result as T[];
};
export const range=(first:number,last?:number,step=1)=>{
  const a=last===undefined?0:first, b=last??first;
  return Array.from({length:Math.max(0,Math.ceil((b-a)/step))},(_,i)=>a+i*step);
};
export const zip=(...items:ArrayLike<unknown>[])=>range(Math.min(...items.map(a=>a.length))).map(i=>items.map(a=>a[i]));
export const enumerate=<T>(a:ArrayLike<T>,begin=0)=>Array.from(a,(value,i)=>[i+begin,value]);
export const repeat=<T>(a:T[],n:number)=>Array.from({length:n},()=>a).flat();
export const any=(a:unknown[])=>a.some(Boolean);
export const all=(a:unknown[])=>a.every(Boolean);
export const getattr=<T,F>(a:Record<string,T>,k:string,b:F):T|F=>a[k]??b;
export const contains=(a:unknown[]|string|Record<PropertyKey,unknown>,k:PropertyKey)=>
  typeof a==='string'?a.includes(String(k)):Array.isArray(a)?a.includes(k):Object.hasOwn(a,k);
export const isclose=(a:number,b:number)=>Math.abs(a-b)<=Math.max(1e-9*Math.max(Math.abs(a),Math.abs(b)),1e-12);
export const round=(v:number,p=0)=>Number(v.toFixed(p));
export const fmt=(value:number,format:string)=>{
  const spec=/^([+])?(0\d+)?(?:\.(\d+))?([d f%g])$/.exec(format);
  if(!spec)return String(value);
  const [,signed,width,digits,c]=spec;
  const allDigits=digits===undefined?0:Number(digits);
  const sign=signed&&value>=0?'+':'';
  if(c==='f')return sign+value.toFixed(allDigits);
  if(c==='%')return sign+(value*100).toFixed(allDigits)+'%';
  if(c==='d')return sign+String(Math.trunc(value)).padStart(Number(width??0),'0');
  return sign+String(value);
};
export const printf=(pattern:string,n:number)=>pattern.replace('%d',String(Math.trunc(n)));
export const bisect_left=(a:number[],n:number)=>{const i=a.findIndex(v=>v>=n);return i<0?a.length:i;};
export const bisect_right=(a:number[],n:number)=>{const i=a.findIndex(v=>v>n);return i<0?a.length:i;};
