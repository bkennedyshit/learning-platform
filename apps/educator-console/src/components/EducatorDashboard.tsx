'use client';
import { useState, useEffect } from 'react';
import { orgService, progressService, Classroom, StudentProgress } from '../lib/services';

export default function EducatorDashboard() {
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [progressData, setProgressData] = useState<Record<string, StudentProgress[]>>({});

  useEffect(() => {
    const load = async () => {
      const classes = await orgService.getClassrooms();
      setClassrooms(classes);
      
      const pd: Record<string, StudentProgress[]> = {};
      for (const c of classes) {
        pd[c.id] = await progressService.getStudentProgress(c.studentIds);
      }
      setProgressData(pd);
    };
    load();
  }, []);

  return (
    <div className="glass-panel animate-in" style={{ animationDelay: '0.1s' }}>
      <h2>Educator Dashboard</h2>
      <p style={{ color: '#94a3b8', marginBottom: '24px' }}>Monitor student progress across your assigned classrooms.</p>

      {classrooms.map(c => (
        <div key={c.id} style={{ marginBottom: '32px' }}>
          <h3 style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '8px', marginBottom: '16px' }}>{c.name}</h3>
          
          <div style={{ overflowX: 'auto' }}>
            <table>
              <thead>
                <tr>
                  <th>Student ID</th>
                  <th>Completed Lessons</th>
                  <th>Grasp Score</th>
                  <th>Last Activity</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {progressData[c.id]?.map(p => (
                  <tr key={p.studentId} style={{ background: p.needsReview ? 'rgba(239, 68, 68, 0.05)' : 'transparent' }}>
                    <td style={{ fontWeight: 500 }}>{p.studentId}</td>
                    <td>{p.completedLessons}</td>
                    <td>
                      <span className={p.graspScore < 70 ? "badge danger" : "badge success"}>
                        {p.graspScore}
                      </span>
                    </td>
                    <td style={{ color: '#94a3b8', fontSize: '0.9rem' }}>{new Date(p.lastActivity).toLocaleDateString()}</td>
                    <td>
                      {p.needsReview ? (
                        <span style={{ color: '#fca5a5', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.9rem' }}>
                          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#ef4444' }}></span>
                          Needs Review
                        </span>
                      ) : (
                        <span style={{ color: '#94a3b8', fontSize: '0.9rem' }}>On Track</span>
                      )}
                    </td>
                  </tr>
                ))}
                {(!progressData[c.id] || progressData[c.id].length === 0) && (
                  <tr>
                    <td colSpan={5} style={{ textAlign: 'center', color: '#94a3b8', padding: '24px' }}>No students in this classroom</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
}
