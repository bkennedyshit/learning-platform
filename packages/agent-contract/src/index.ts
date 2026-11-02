/**
 * Learning-agent contract. Currently only v1 is defined. New wire-breaking
 * versions must be added under a new namespace (v2, …) without mutating v1.
 */
export * as v1 from "./v1/index.js";
export * from "./v1/index.js";
export { CONTRACT_VERSION } from "./v1/types.js";
