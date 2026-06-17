import { AuthorizationDeniedError } from "./errors.js";
import type { Principal } from "./types.js";

export type OwnershipResolver = (resourceId: string) => Promise<string | undefined>;

export async function assertOwnsResource(
  principal: Principal,
  resourceId: string,
  resolveOwner: OwnershipResolver
): Promise<void> {
  const ownerId = await resolveOwner(resourceId).catch(() => undefined);

  if (!ownerId || ownerId !== principal.accountId) {
    throw new AuthorizationDeniedError();
  }
}

export function assertPlatformAdmin(principal: Principal): void {
  if (principal.role !== "platform_admin") {
    throw new AuthorizationDeniedError();
  }
}
