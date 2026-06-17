import assert from "node:assert/strict";
import test from "node:test";
import { ComplianceService, ConsentRequiredError } from "./service.js";
import type { ComplianceRepository } from "./repository.js";

test("compliance service throws ConsentRequiredError for under-13 user without consent", async () => {
  const birthdate = new Date();
  birthdate.setFullYear(birthdate.getFullYear() - 10); // 10 years old

  const mockRepo = {
    getStudentConsentInfo: async (accountId: string) => ({
      birthdate,
      consent_status: "pending"
    })
  } as unknown as ComplianceRepository;

  const service = new ComplianceService(mockRepo);

  await assert.rejects(
    () => service.checkConsentGate("student-1"),
    ConsentRequiredError
  );
});

test("compliance service allows writes for under-13 user with granted consent", async () => {
  const birthdate = new Date();
  birthdate.setFullYear(birthdate.getFullYear() - 10); // 10 years old

  const mockRepo = {
    getStudentConsentInfo: async (accountId: string) => ({
      birthdate,
      consent_status: "granted"
    })
  } as unknown as ComplianceRepository;

  const service = new ComplianceService(mockRepo);

  await assert.doesNotReject(() => service.checkConsentGate("student-1"));
});

test("compliance service allows writes for users 13 or over without consent", async () => {
  const birthdate = new Date();
  birthdate.setFullYear(birthdate.getFullYear() - 14); // 14 years old

  const mockRepo = {
    getStudentConsentInfo: async (accountId: string) => ({
      birthdate,
      consent_status: "pending"
    })
  } as unknown as ComplianceRepository;

  const service = new ComplianceService(mockRepo);

  await assert.doesNotReject(() => service.checkConsentGate("student-1"));
});

test("compliance service records audit access correctly", async () => {
  let recordedAccessor = "";
  let recordedStudent = "";
  let recordedLesson: string | undefined = undefined;

  const mockRepo = {
    recordAccessAudit: async (accessor: string, student: string, lessonId?: string) => {
      recordedAccessor = accessor;
      recordedStudent = student;
      recordedLesson = lessonId;
    }
  } as unknown as ComplianceRepository;

  const service = new ComplianceService(mockRepo);

  await service.auditAccess("educator-1", "student-1", "lesson-1");

  assert.equal(recordedAccessor, "educator-1");
  assert.equal(recordedStudent, "student-1");
  assert.equal(recordedLesson, "lesson-1");
});
