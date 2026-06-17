export class InvalidCredentialsError extends Error {
  constructor() {
    super("Invalid email or password.");
    this.name = "InvalidCredentialsError";
  }
}

export class EmailAlreadyRegisteredError extends Error {
  constructor() {
    super("An account with this email already exists.");
    this.name = "EmailAlreadyRegisteredError";
  }
}

export class AuthorizationDeniedError extends Error {
  constructor() {
    super("Access denied.");
    this.name = "AuthorizationDeniedError";
  }
}

export class InvalidTokenError extends Error {
  constructor() {
    super("The token is invalid or has expired.");
    this.name = "InvalidTokenError";
  }
}
