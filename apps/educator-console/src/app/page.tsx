import ClassroomManager from '../components/ClassroomManager';
import EducatorDashboard from '../components/EducatorDashboard';

export default function Home() {
  return (
    <div>
      <div style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '8px' }}>Welcome, Educator</h1>
        <p style={{ color: '#94a3b8', fontSize: '1.1rem' }}>Manage your organization and monitor student progress.</p>
      </div>
      
      <div className="grid">
        <ClassroomManager />
        <EducatorDashboard />
      </div>
    </div>
  );
}
