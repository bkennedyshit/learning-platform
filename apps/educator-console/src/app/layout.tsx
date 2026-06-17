import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Educator Console | Learning Platform',
  description: 'Manage classrooms, view student progress, and organize paths.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <header className="header">
          <div>
            <h1 style={{ margin: 0, fontSize: '1.5rem', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'var(--primary)', display: 'grid', placeItems: 'center' }}>
                <span style={{ fontSize: '1rem', fontWeight: 800 }}>L</span>
              </div>
              Educator Console
            </h1>
          </div>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.9rem' }}>Role: Org Admin</span>
            <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--secondary)', display: 'grid', placeItems: 'center', border: '1px solid var(--glass-border)' }}>
              A
            </div>
          </div>
        </header>
        <main className="main-content">
          {children}
        </main>
      </body>
    </html>
  );
}
