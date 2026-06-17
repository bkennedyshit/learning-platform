import type { Pool } from "pg";

export interface AffiliateStats {
  referrals: number;
  conversions: number;
}

export class AffiliateRepository {
  constructor(private readonly pool: Pool) {}

  async createAffiliate(accountId: string, referralId: string): Promise<void> {
    await this.pool.query(
      `
        INSERT INTO affiliates (account_id, referral_id)
        VALUES ($1, $2)
      `,
      [accountId, referralId]
    );
  }

  async getAffiliateIdByReferralId(referralId: string): Promise<string | undefined> {
    const result = await this.pool.query<{ id: string }>(
      `
        SELECT id FROM affiliates
        WHERE referral_id = $1
      `,
      [referralId]
    );
    return result.rows[0]?.id;
  }

  async getAffiliateIdByAccountId(accountId: string): Promise<string | undefined> {
    const result = await this.pool.query<{ id: string }>(
      `
        SELECT id FROM affiliates
        WHERE account_id = $1
      `,
      [accountId]
    );
    return result.rows[0]?.id;
  }

  async createReferral(affiliateId: string, attributionToken: string): Promise<void> {
    await this.pool.query(
      `
        INSERT INTO referrals (affiliate_id, attribution_token)
        VALUES ($1, $2)
      `,
      [affiliateId, attributionToken]
    );
  }

  async getReferralIdByToken(attributionToken: string): Promise<string | undefined> {
    const result = await this.pool.query<{ id: string }>(
      `
        SELECT id FROM referrals
        WHERE attribution_token = $1
      `,
      [attributionToken]
    );
    return result.rows[0]?.id;
  }

  async createConversion(referralId: string, accountId: string): Promise<void> {
    await this.pool.query(
      `
        INSERT INTO conversions (referral_id, account_id)
        VALUES ($1, $2)
      `,
      [referralId, accountId]
    );
  }

  async getStats(accountId: string): Promise<AffiliateStats> {
    const result = await this.pool.query<{ referrals: string; conversions: string }>(
      `
        SELECT 
          COUNT(DISTINCT r.id) as referrals,
          COUNT(DISTINCT c.id) as conversions
        FROM affiliates a
        LEFT JOIN referrals r ON r.affiliate_id = a.id
        LEFT JOIN conversions c ON c.referral_id = r.id
        WHERE a.account_id = $1
      `,
      [accountId]
    );

    const row = result.rows[0];
    if (!row) {
      return { referrals: 0, conversions: 0 };
    }

    return {
      referrals: parseInt(row.referrals, 10),
      conversions: parseInt(row.conversions, 10),
    };
  }
}
