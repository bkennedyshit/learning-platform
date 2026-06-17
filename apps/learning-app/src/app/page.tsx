"use client";

import React from "react";
import Link from "next/link";

export default function Home() {
  return (
    <div style={{ paddingBottom: 'var(--space-3xl)' }}>
      {/* Marketing nav */}
      <nav className="glass-panel" style={{
        position: 'fixed', top: '1.5rem', left: '50%', transform: 'translateX(-50%)',
        width: 'calc(100% - 3rem)', maxWidth: '1280px', padding: '1rem 2rem',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        zIndex: 100, borderRadius: 'var(--radius-full)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{
            width: '32px', height: '32px', borderRadius: '8px',
            background: 'linear-gradient(135deg, var(--accent-primary), var(--secondary-color))',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: 'white', fontWeight: 'bold', fontSize: '1.2rem'
          }}>A</div>
          <span style={{ fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: '1.25rem', letterSpacing: '-0.02em' }}>
            Aura
          </span>
        </div>
        <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
          <Link href="/learn?catalog=k12" style={{ fontWeight: 500, fontSize: '0.95rem' }}>K-12</Link>
          <Link href="/learn?catalog=advanced" style={{ fontWeight: 500, fontSize: '0.95rem' }}>College</Link>
          <Link href="/learn" style={{ fontWeight: 500, fontSize: '0.95rem' }}>Catalog</Link>
        </div>
        <div>
          <Link href="/learn" className="btn-primary" style={{ padding: '0.5rem 1.5rem', fontSize: '0.95rem' }}>
            Start Learning
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container" style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center',
        paddingTop: '10rem', paddingBottom: 'var(--space-3xl)'
      }}>
        <div className="animate-fade-in-up" style={{
          display: 'inline-block', padding: '0.5rem 1rem', borderRadius: 'var(--radius-full)',
          background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)',
          color: 'var(--accent-primary)', fontWeight: 600, fontSize: '0.875rem', marginBottom: 'var(--space-md)'
        }}>
          ✨ The Future of Education is Here
        </div>

        <h1 className="animate-fade-in-up delay-100" style={{
          fontSize: 'clamp(3rem, 8vw, 5.5rem)', maxWidth: '900px', marginBottom: 'var(--space-lg)', lineHeight: 1.1
        }}>
          Master Any Subject with <br />
          <span className="text-gradient-accent">Intelligent Learning</span>
        </h1>

        <p className="animate-fade-in-up delay-200" style={{
          fontSize: '1.25rem', color: 'var(--text-secondary)', maxWidth: '600px', marginBottom: 'var(--space-2xl)'
        }}>
          Experience a personalized curriculum that adapts to your pace.
          From foundational K-12 concepts to advanced College coursework.
        </p>

        <div className="animate-fade-in-up delay-300" style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'center' }}>
          <Link href="/learn" className="btn-primary" style={{ padding: '1rem 2.5rem', fontSize: '1.1rem' }}>
            Start Learning Free
          </Link>
          <Link href="/learn" className="btn-secondary" style={{ padding: '1rem 2.5rem', fontSize: '1.1rem' }}>
            Explore Curriculums
          </Link>
        </div>
      </section>

      {/* Curriculum Section */}
      <section className="container" id="curriculum" style={{ paddingTop: 'var(--space-2xl)' }}>
        <div style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)' }}>
          <h2 style={{ fontSize: '2.5rem', marginBottom: 'var(--space-sm)' }}>Tailored Pathways</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>Curriculum designed for every stage of your academic journey.</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', alignItems: 'stretch' }}>
          <div className="glass-panel animate-float" style={{ padding: '3rem 2rem', display: 'flex', flexDirection: 'column' }}>
            <div style={{
              width: '64px', height: '64px', borderRadius: '16px',
              background: 'linear-gradient(135deg, var(--accent-primary), rgba(99, 102, 241, 0.2))',
              display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem', fontSize: '2rem'
            }}>🎒</div>
            <h3 style={{ fontSize: '1.75rem', marginBottom: '1rem' }}>K-12 Education</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem', flex: 1 }}>
              Build a strong foundation. Interactive modules cover Math, Science, Reading, and more.
            </p>
            <Link href="/learn?catalog=k12" className="btn-secondary" style={{ width: '100%', marginTop: 'auto', textAlign: 'center' }}>
              View K-12 Program
            </Link>
          </div>

          <div className="glass-panel animate-float" style={{ padding: '3rem 2rem', display: 'flex', flexDirection: 'column', animationDelay: '1.5s' }}>
            <div style={{
              width: '64px', height: '64px', borderRadius: '16px',
              background: 'linear-gradient(135deg, var(--secondary-color), rgba(236, 72, 153, 0.2))',
              display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem', fontSize: '2rem'
            }}>🎓</div>
            <h3 style={{ fontSize: '1.75rem', marginBottom: '1rem' }}>College Prep & Higher Ed</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem', flex: 1 }}>
              Tackle complex subjects with confidence. From Calculus to Computer Science and beyond.
            </p>
            <Link href="/learn?catalog=advanced" className="btn-secondary" style={{ width: '100%', marginTop: 'auto', textAlign: 'center' }}>
              View College Program
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
