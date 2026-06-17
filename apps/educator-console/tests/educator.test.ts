import { orgService } from '../src/lib/services';

describe('Educator Console', () => {
  it('enforces seat ceiling', async () => {
    const org = await orgService.getOrganization();
    org.usedSeats = org.purchasedSeats;
    await expect(orgService.addStudentToClassroom('class1', 'stu_new'))
      .rejects.toThrow('Seat limit reached: Cannot add student beyond purchased seats.');
  });

  it('classroom assignment enrolls all students', async () => {
    await orgService.assignPath('class1', 'test_path');
    const classes = await orgService.getClassrooms();
    expect(classes.find(c => c.id === 'class1')?.assignedPathId).toBe('test_path');
  });

  it('scoping educator', async () => {
    const classes = await orgService.getClassrooms();
    expect(classes[0].educatorIds).toContain('edu1');
  });
});
