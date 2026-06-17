'use client';
import { useState, useEffect } from 'react';
import { orgService, Classroom, Organization } from '../lib/services';

export default function ClassroomManager() {
  const [org, setOrg] = useState<Organization | null>(null);
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [newClassName, setNewClassName] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    orgService.getOrganization().then(setOrg);
    orgService.getClassrooms().then(setClassrooms);
  }, []);

  const handleCreate = async () => {
    if (!newClassName) return;
    const c = await orgService.createClassroom(newClassName, 'edu1');
    setClassrooms([...classrooms, c]);
    setNewClassName('');
  };

  const handleAddStudent = async (classId: string) => {
    try {
      setError('');
      await orgService.addStudentToClassroom(classId, `stu${Date.now()}`);
      const updated = await orgService.getClassrooms();
      setClassrooms([...updated]);
      const updatedOrg = await orgService.getOrganization();
      setOrg({ ...updatedOrg });
    } catch (e: any) {
      setError(e.message);
    }
  };

  const handleAssignPath = async (classId: string) => {
    await orgService.assignPath(classId, 'path_algebra_advanced');
    const updated = await orgService.getClassrooms();
    setClassrooms([...updated]);
  };

  if (!org) return <div>Loading...</div>;

  return (
    <div className="glass-panel animate-in">
      <h2 style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        Organization Manager
        <span className={org.usedSeats >= org.purchasedSeats ? "badge danger" : "badge success"}>
          Seats: {org.usedSeats} / {org.purchasedSeats}
        </span>
      </h2>
      
      {error && <div style={{ background: 'rgba(239, 68, 68, 0.2)', color: '#fca5a5', padding: '12px', borderRadius: '8px', marginBottom: '16px' }}>{error}</div>}

      <div style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
        <input 
          placeholder="New Classroom Name" 
          value={newClassName} 
          onChange={e => setNewClassName(e.target.value)}
          style={{ marginBottom: 0 }}
        />
        <button className="btn" onClick={handleCreate}>Create</button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {classrooms.map(c => (
          <div key={c.id} style={{ background: 'rgba(0,0,0,0.2)', padding: '16px', borderRadius: '8px', border: '1px solid var(--glass-border)' }}>
            <h3 style={{ margin: '0 0 12px 0' }}>{c.name} <span className="badge" style={{ marginLeft: '8px' }}>Path: {c.assignedPathId || 'None'}</span></h3>
            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <button className="btn btn-secondary" onClick={() => handleAddStudent(c.id)}>Add Student</button>
              <button className="btn btn-secondary" onClick={() => handleAssignPath(c.id)}>Assign Path</button>
            </div>
            <div style={{ marginTop: '12px', fontSize: '0.9rem', color: '#94a3b8' }}>
              Students Enrolled: {c.studentIds.length}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
