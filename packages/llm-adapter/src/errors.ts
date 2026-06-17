export class ProviderUnavailableError extends Error {
  constructor(message = "The configured language model provider is unavailable.") {
    super(message);
    this.name = "ProviderUnavailableError";
  }
}

export class ProviderConfigurationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ProviderConfigurationError";
  }
}
