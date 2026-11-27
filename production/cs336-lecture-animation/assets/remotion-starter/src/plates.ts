import raw from './data/plates.json';
export type PlateMedia={file:string;pixels:[number,number];kind:'raster'|'vector';source:string};
export const plates=raw as unknown as Record<string,PlateMedia>;
