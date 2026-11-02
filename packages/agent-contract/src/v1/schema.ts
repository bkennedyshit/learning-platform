/**
 * Hand-rolled, dependency-free runtime schema validation.
 *
 * The learning-agent contract deliberately avoids third-party validation
 * libraries so the versioned wire format stays inspectable and stable.
 */

export type SchemaNode =
  | StringSchema
  | NumberSchema
  | BooleanSchema
  | ArraySchema
  | ObjectSchema
  | UnknownSchema;

export interface StringSchema {
  type: "string";
  enum?: readonly string[];
  minLength?: number;
  maxLength?: number;
  pattern?: string;
}

export interface NumberSchema {
  type: "number";
  integer?: boolean;
  min?: number;
  max?: number;
}

export interface BooleanSchema {
  type: "boolean";
}

export interface ArraySchema {
  type: "array";
  items: SchemaNode;
  minItems?: number;
  maxItems?: number;
}

export interface ObjectSchema {
  type: "object";
  properties: Record<string, SchemaNode>;
  required?: readonly string[];
  /** Defaults to false: unknown keys are rejected. */
  additionalProperties?: boolean;
}

export interface UnknownSchema {
  type: "unknown";
}

export interface ValidationError {
  path: string;
  message: string;
}

export interface ValidationResult {
  ok: boolean;
  errors: ValidationError[];
}

export class ContractValidationError extends Error {
  constructor(
    message: string,
    readonly errors: ValidationError[]
  ) {
    super(message);
    this.name = "ContractValidationError";
  }
}

export function validate(schema: SchemaNode, value: unknown, path = "$"): ValidationResult {
  const errors: ValidationError[] = [];
  validateNode(schema, value, path, errors);
  return { ok: errors.length === 0, errors };
}

/** Validate and return the value typed as T, or throw ContractValidationError. */
export function parse<T>(schema: SchemaNode, value: unknown, label = "value"): T {
  const result = validate(schema, value);
  if (!result.ok) {
    const detail = result.errors.map((e) => `${e.path}: ${e.message}`).join("; ");
    throw new ContractValidationError(`Invalid ${label}: ${detail}`, result.errors);
  }
  return value as T;
}

function validateNode(schema: SchemaNode, value: unknown, path: string, errors: ValidationError[]): void {
  switch (schema.type) {
    case "unknown":
      return;
    case "string":
      validateString(schema, value, path, errors);
      return;
    case "number":
      validateNumber(schema, value, path, errors);
      return;
    case "boolean":
      if (typeof value !== "boolean") {
        errors.push({ path, message: "expected boolean" });
      }
      return;
    case "array":
      validateArray(schema, value, path, errors);
      return;
    case "object":
      validateObject(schema, value, path, errors);
      return;
  }
}

function validateString(schema: StringSchema, value: unknown, path: string, errors: ValidationError[]): void {
  if (typeof value !== "string") {
    errors.push({ path, message: "expected string" });
    return;
  }
  if (schema.enum && !schema.enum.includes(value)) {
    errors.push({ path, message: `expected one of ${schema.enum.join(", ")}` });
  }
  if (schema.minLength !== undefined && value.length < schema.minLength) {
    errors.push({ path, message: `shorter than minLength ${schema.minLength}` });
  }
  if (schema.maxLength !== undefined && value.length > schema.maxLength) {
    errors.push({ path, message: `longer than maxLength ${schema.maxLength}` });
  }
  if (schema.pattern !== undefined && !new RegExp(schema.pattern).test(value)) {
    errors.push({ path, message: `does not match pattern ${schema.pattern}` });
  }
}

function validateNumber(schema: NumberSchema, value: unknown, path: string, errors: ValidationError[]): void {
  if (typeof value !== "number" || Number.isNaN(value)) {
    errors.push({ path, message: "expected number" });
    return;
  }
  if (schema.integer && !Number.isInteger(value)) {
    errors.push({ path, message: "expected integer" });
  }
  if (schema.min !== undefined && value < schema.min) {
    errors.push({ path, message: `less than min ${schema.min}` });
  }
  if (schema.max !== undefined && value > schema.max) {
    errors.push({ path, message: `greater than max ${schema.max}` });
  }
}

function validateArray(schema: ArraySchema, value: unknown, path: string, errors: ValidationError[]): void {
  if (!Array.isArray(value)) {
    errors.push({ path, message: "expected array" });
    return;
  }
  if (schema.minItems !== undefined && value.length < schema.minItems) {
    errors.push({ path, message: `fewer than minItems ${schema.minItems}` });
  }
  if (schema.maxItems !== undefined && value.length > schema.maxItems) {
    errors.push({ path, message: `more than maxItems ${schema.maxItems}` });
  }
  value.forEach((item, index) => {
    validateNode(schema.items, item, `${path}[${index}]`, errors);
  });
}

function validateObject(schema: ObjectSchema, value: unknown, path: string, errors: ValidationError[]): void {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    errors.push({ path, message: "expected object" });
    return;
  }
  const record = value as Record<string, unknown>;
  const required = schema.required ?? [];
  for (const key of required) {
    if (record[key] === undefined) {
      errors.push({ path: `${path}.${key}`, message: "required" });
    }
  }
  const allowAdditional = schema.additionalProperties ?? false;
  for (const key of Object.keys(record)) {
    const propSchema = schema.properties[key];
    if (!propSchema) {
      if (!allowAdditional) {
        errors.push({ path: `${path}.${key}`, message: "unexpected property" });
      }
      continue;
    }
    // Optional properties may be omitted; undefined is treated as absent.
    if (record[key] === undefined) {
      continue;
    }
    validateNode(propSchema, record[key], `${path}.${key}`, errors);
  }
}
