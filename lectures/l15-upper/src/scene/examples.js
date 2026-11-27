// Frame-driven artwork, drawn by the Remotion Canvas composition.
import {min,max,sum,len,range,zip,enumerate,round,getattr,any,all,at,slice,repeat,contains,fmt,printf,isclose,bisect_left,bisect_right} from '../values';

// The little numerical examples in the film, with their actual assumptions.
export const PACK_LENGTHS = [3, 2, 2];
export const OFFSETS = [0, 3, 5, 7];
export const TOKENS = ["A₁", "A₂", "A₃", "B₁", "B₂", "C₁", "C₂"];
export const GROUP = [0, 0, 0, 1, 1, 2, 2];
export const SHOW_QUERY = 4;
export const SHOW_KEY = 1;
export const SFT_TARGET_PROBS = [0.5, 0.25, 0.8];
export const DEDUPE_IN = [3, 1, 3, 2, 1];
export const DEDUPE_EXPECT = [3, 1, 2];
export const REFERENCE = [0.8, 0.2];
export const SORTED = [1, 3, 3, 3, 7];
export const TARGET = 3;
export const FIRST_GE = 1;
export function bisect_steps(words, target, skip_equal=false) {
  let hi, lo, mid, steps;
  [lo, hi] = [0, len(words)];
  steps = [];
  while ((lo < hi)) {
    mid = Math.floor((lo + hi)/2);
    steps.push([lo, mid, hi]);
    if (((at(words, mid) < target) || (skip_equal && (at(words, mid) === target)))) {
      lo = (mid + 1);
    } else {
      hi = mid;
    }
  }
  return [Array.from(steps), lo];
}
export function allowed(query, key, isolate=true) {
  return ((key <= query) && ((!isolate) || (at(GROUP, query) === at(GROUP, key))));
}
export function attention(query, isolate=true, logits=null) {
  let den, weights, z;
  z = ((logits === null) ? repeat([0.0], len(GROUP)) : logits);
  weights = (()=>{const __list24=[];for(const [k, v] of enumerate(z)){__list24.push((allowed(query, k, isolate) ? Math.exp(v) : 0));}return __list24;})();
  den = sum(weights);
  return Array.from((()=>{const __list25=[];for(const w of weights){__list25.push((w / den));}return __list25;})());
}
export function bt(a, b) {
  return (1 / (1 + Math.exp((b - a))));
}
export function kl(p, q) {
  if (!(len(p) === len(q))) throw new Error("len(p) == len(q)");
  if (!(isclose(sum(p), 1) && isclose(sum(q), 1))) throw new Error("math.isclose(sum(p), 1) and math.isclose(sum(q), 1)");
  return max(0.0, sum((()=>{const __list26=[];for(const [v, w] of zip(p, q)){if(!((v > 0)))continue;__list26.push((v * Math.log((v / w))));}return __list26;})()));
}
export function sft_nll(target_probs) {
  return sum((()=>{const __list27=[];for(const v of target_probs){__list27.push((-Math.log(v)));}return __list27;})());
}
export function expected_score(probabilities, rewards) {
  if (!((len(probabilities) === len(rewards)) && isclose(sum(probabilities), 1))) throw new Error("len(probabilities) == len(rewards) and math.isclose(math.fsum(probabilities), 1)");
  return sum((()=>{const __list28=[];for(const [p, r] of zip(probabilities, rewards)){__list28.push((p * r));}return __list28;})());
}
