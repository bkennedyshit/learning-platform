import type { Pool } from "pg";

export class ComplianceRepository {
  constructor(private readonly pool: Pool) {}

  async recordAccessAudit(
    accessorAccountId: string,
    studentAccountId: string,
    lessonId?: string
  ): Promise<void> {
    await this.pool.query(
      `
      INSERT INTO student_record_audits (accessor_account_id, student_account_id, lesson_id)
      VALUES ($1, $2, $3)
      `,
      [accessorAccountId, studentAccountId, lessonId || null]
    );
  }

  async deleteStudentData(studentAccountId: string): Promise<void> {
    // Delete personal data: progress, grasp_scores, review_schedules
    // Path enrollments might also be considered personal data if they track progress.
    // We can delete them too, or rely on them being wiped if the account is deleted.
    // The requirement says: "delete the Student's personal data within the period defined by the platform's data-retention policy."
    
    const client = await this.pool.connect();
    try {
      await client.query("BEGIN");
      await client.query(`DELETE FROM progress WHERE account_id = $1`, [studentAccountId]);
      await client.query(`DELETE FROM grasp_scores WHERE account_id = $1`, [studentAccountId]);
      await client.query(`DELETE FROM review_schedules WHERE account_id = $1`, [studentAccountId]);
      await client.query(`DELETE FROM path_enrollments WHERE account_id = $1`, [studentAccountId]);
      
      // Let's also anonymize or delete the account if requested? The task says "delete the Student's personal data"
      // If the account needs to be deleted, we delete it from `accounts` table.
      // But typically "delete student data" refers to the generated records. Let's delete the account too if that's what's meant, 
      // but maybe just the progress data is enough. 
      // "delete the Student's personal data" -> progress, grasp_scores are explicit.
      
      await client.query("COMMIT");
    } catch (err) {
      await client.query("ROLLBACK");
      throw err;
    } finally {
      client.release();
    }
  }

  async getAuditLogCount(studentAccountId: string): Promise<number> {
    const result = await this.pool.query<{ count: string }>(
      `SELECT count(*) FROM student_record_audits WHERE student_account_id = $1`,
      [studentAccountId]
    );
    return parseInt(result.rows[0]?.count ?? "0", 10);
  }

  async getStudentConsentInfo(accountId: string): Promise<{ birthdate: Date | null, consent_status: string } | undefined> {
    const result = await this.pool.query<{ birthdate: Date | null, consent_status: string }>(
      `SELECT birthdate, consent_status FROM accounts WHERE id = $1`,
      [accountId]
    );
    return result.rows[0];
  }
}

