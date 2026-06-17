import { randomBytes, randomUUID } from "node:crypto";
import type { AffiliateRepository, AffiliateStats } from "./repository.js";

export class AffiliateService {
  constructor(private readonly repo: AffiliateRepository) {}

  async registerAffiliate(accountId: string): Promise<string> {
    const referralId = randomBytes(8).toString("hex");
    await this.repo.createAffiliate(accountId, referralId);
    return referralId;
  }

  async attributeVisit(referralId: string): Promise<string> {
    const affiliateId = await this.repo.getAffiliateIdByReferralId(referralId);
    if (!affiliateId) {
      throw new Error(`Affiliate with referral_id ${referralId} not found`);
    }

    const attributionToken = randomUUID();
    await this.repo.createReferral(affiliateId, attributionToken);
    return attributionToken;
  }

  async recordConversion(attributionToken: string, accountId: string): Promise<void> {
    const referralId = await this.repo.getReferralIdByToken(attributionToken);
    if (!referralId) {
      throw new Error(`Referral with token ${attributionToken} not found`);
    }

    await this.repo.createConversion(referralId, accountId);
  }

  async getAffiliateStats(accountId: string): Promise<AffiliateStats> {
    const affiliateId = await this.repo.getAffiliateIdByAccountId(accountId);
    if (!affiliateId) {
      throw new Error(`Affiliate account ${accountId} not found`);
    }
    return this.repo.getStats(accountId);
  }
}
