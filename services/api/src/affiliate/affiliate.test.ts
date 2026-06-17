import assert from "node:assert/strict";
import test from "node:test";
import { AffiliateService } from "./service.js";
import type { AffiliateRepository, AffiliateStats } from "./repository.js";

class MockAffiliateRepository {
  private affiliates = new Map<string, { id: string; accountId: string; referralId: string }>();
  private referrals = new Map<string, { id: string; affiliateId: string; token: string }>();
  private conversions = new Map<string, { id: string; referralId: string; accountId: string }>();
  private nextId = 1;

  async createAffiliate(accountId: string, referralId: string): Promise<void> {
    if (Array.from(this.affiliates.values()).some((a) => a.accountId === accountId)) {
      throw new Error("Duplicate account_id in affiliates");
    }
    const id = String(this.nextId++);
    this.affiliates.set(id, { id, accountId, referralId });
  }

  async getAffiliateIdByReferralId(referralId: string): Promise<string | undefined> {
    const affiliate = Array.from(this.affiliates.values()).find((a) => a.referralId === referralId);
    return affiliate?.id;
  }

  async getAffiliateIdByAccountId(accountId: string): Promise<string | undefined> {
    const affiliate = Array.from(this.affiliates.values()).find((a) => a.accountId === accountId);
    return affiliate?.id;
  }

  async createReferral(affiliateId: string, attributionToken: string): Promise<void> {
    const id = String(this.nextId++);
    this.referrals.set(id, { id, affiliateId, token: attributionToken });
  }

  async getReferralIdByToken(attributionToken: string): Promise<string | undefined> {
    const referral = Array.from(this.referrals.values()).find((r) => r.token === attributionToken);
    return referral?.id;
  }

  async createConversion(referralId: string, accountId: string): Promise<void> {
    if (Array.from(this.conversions.values()).some((c) => c.referralId === referralId)) {
      throw new Error("Duplicate referral_id in conversions");
    }
    if (Array.from(this.conversions.values()).some((c) => c.accountId === accountId)) {
      throw new Error("Duplicate account_id in conversions");
    }
    const id = String(this.nextId++);
    this.conversions.set(id, { id, referralId, accountId });
  }

  async getStats(accountId: string): Promise<AffiliateStats> {
    const affiliate = Array.from(this.affiliates.values()).find((a) => a.accountId === accountId);
    if (!affiliate) {
      return { referrals: 0, conversions: 0 };
    }

    const affiliateReferrals = Array.from(this.referrals.values()).filter(
      (r) => r.affiliateId === affiliate.id
    );
    const referralIds = new Set(affiliateReferrals.map((r) => r.id));

    const affiliateConversions = Array.from(this.conversions.values()).filter((c) =>
      referralIds.has(c.referralId)
    );

    return {
      referrals: affiliateReferrals.length,
      conversions: affiliateConversions.length,
    };
  }
}

test("AffiliateManager: single-attribution and conversion <= referral counts", async () => {
  const repo = new MockAffiliateRepository() as unknown as AffiliateRepository;
  const service = new AffiliateService(repo);

  const affiliateAccountId = "affiliate-account-1";
  const visitorAccountId = "visitor-account-1";

  // Register affiliate
  const referralId = await service.registerAffiliate(affiliateAccountId);
  assert.ok(referralId, "Referral ID must be generated");

  // Attribute visit
  const token = await service.attributeVisit(referralId);
  assert.ok(token, "Attribution token must be generated");

  // Verify stats before conversion
  let stats = await service.getAffiliateStats(affiliateAccountId);
  assert.equal(stats.referrals, 1);
  assert.equal(stats.conversions, 0);

  // Record conversion
  await service.recordConversion(token, visitorAccountId);

  // Verify stats after conversion
  stats = await service.getAffiliateStats(affiliateAccountId);
  assert.equal(stats.referrals, 1);
  assert.equal(stats.conversions, 1);
  assert.ok(
    stats.conversions <= stats.referrals,
    "Conversions count must be less than or equal to referrals count"
  );

  // Property 12 constraints
  // 1. Single-attribution: Cannot convert the same referral token again (it would violate unique referral_id in conversions)
  await assert.rejects(
    service.recordConversion(token, "another-visitor-account"),
    /Duplicate referral_id in conversions/
  );

  // 2. Cannot double-convert the same account (violates unique account_id in conversions)
  const token2 = await service.attributeVisit(referralId);
  await assert.rejects(
    service.recordConversion(token2, visitorAccountId),
    /Duplicate account_id in conversions/
  );

  stats = await service.getAffiliateStats(affiliateAccountId);
  assert.equal(stats.referrals, 2);
  assert.equal(stats.conversions, 1);
  assert.ok(
    stats.conversions <= stats.referrals,
    "Conversions count must remain <= referrals count after failed attempts"
  );
});
