import type { ComplianceRepository } from "./repository.js";

export class ConsentRequiredError extends Error {
  constructor() {
    super("COPPA Consent Required: Cannot write personal data for under-13 user without granted consent.");
    this.name = "ConsentRequiredError";
  }
}

export class ComplianceService {
  constructor(private readonly repo: ComplianceRepository) {}

  /**
   * Checks if the student is under 13 and lacks consent.
   * Throws ConsentRequiredError if writes should be blocked.
   */
  async checkConsentGate(accountId: string): Promise<void> {
    const info = await this.repo.getStudentConsentInfo(accountId);
    if (!info) return;

    if (info.birthdate) {
      const ageMs = Date.now() - info.birthdate.getTime();
      const ageYears = ageMs / (1000 * 60 * 60 * 24 * 365.25);
      if (ageYears < 13 && info.consent_status !== "granted") {
        throw new ConsentRequiredError();
      }
    }
  }

  /**
   * Records an audit log when an authorized account accesses a student's records.
   */
  async auditAccess(
    accessorAccountId: string,
    studentAccountId: string,
    lessonId?: string
  ): Promise<void> {
    await this.repo.recordAccessAudit(accessorAccountId, studentAccountId, lessonId);
  }

  /**
   * Deletes a student's personal data (FERPA/COPPA deletion requirement).
   */
  async deleteStudentData(studentAccountId: string): Promise<void> {
    await this.repo.deleteStudentData(studentAccountId);
  }
}

