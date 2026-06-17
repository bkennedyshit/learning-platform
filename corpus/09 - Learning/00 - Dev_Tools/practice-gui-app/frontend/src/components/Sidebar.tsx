import { useEffect, useState } from "react";
import type { Track, ChapterMeta } from "../types";
import { fetchSubject } from "../api";

interface Props {
  tracks: Track[];
  selectedSubjectId: string | null;
  selectedChapterNum: string | null;
  onSelect: (subjectId: string, chapterNum: string) => void;
}

const TRACK_ICONS: Record<string, string> = {
  "07 - Math and Physics": "📐",
  "08 - App Architectures & Frameworks": "💻",
  "09 - VR & 3D Engineering": "🎮",
  "10 - AI & Machine Learning Systems": "🤖",
  "11 - Neuroscience & Computational Cognition": "🧠",
  "12 - Behavioral Psychology & Reinforcement Learning": "🎯",
  "13 - Biomechanics & Human-Computer Interface (HCI)": "🏃",
};

function shortTrackName(track: string): string {
  // Strip leading number prefix for display
  return track.replace(/^\d+\s*-\s*/, "");
}

function shortSubjectName(name: string): string {
  return name.replace(/^\d+\s*-\s*/, "");
}

export default function Sidebar({ tracks, selectedSubjectId, selectedChapterNum, onSelect }: Props) {
  const [expandedTracks, setExpandedTracks] = useState<Set<string>>(new Set(["07 - Math and Physics"]));
  const [expandedSubject, setExpandedSubject] = useState<string | null>(null);
  const [chapters, setChapters] = useState<ChapterMeta[]>([]);
  const [loadingChapters, setLoadingChapters] = useState(false);

  const toggleTrack = (track: string) => {
    setExpandedTracks((prev) => {
      const next = new Set(prev);
      if (next.has(track)) next.delete(track);
      else next.add(track);
      return next;
    });
  };

  const selectSubject = (subjectId: string) => {
    if (expandedSubject === subjectId) {
      setExpandedSubject(null);
      return;
    }
    setExpandedSubject(subjectId);
    setLoadingChapters(true);
    fetchSubject(subjectId)
      .then((detail) => setChapters(detail.chapters))
      .finally(() => setLoadingChapters(false));
  };

  // Auto-expand subject when selection changes externally
  useEffect(() => {
    if (selectedSubjectId && expandedSubject !== selectedSubjectId) {
      setExpandedSubject(selectedSubjectId);
      fetchSubject(selectedSubjectId).then((detail) => setChapters(detail.chapters));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedSubjectId]);

  return (
    <aside className="h-full overflow-y-auto border-r border-gh-border bg-gh-panel p-3">
      <h2 className="text-xs font-semibold text-gh-muted uppercase tracking-wide mb-3 px-1">
        Curriculum
      </h2>
      <nav className="space-y-1">
        {tracks.map((t) => (
          <div key={t.track}>
            {/* Track heading */}
            <button
              onClick={() => toggleTrack(t.track)}
              className="w-full text-left px-2 py-1.5 rounded text-sm font-semibold text-gh-text hover:bg-gh-border/30 transition-colors flex items-center gap-1.5"
            >
              <span className="text-xs">{expandedTracks.has(t.track) ? "▼" : "▶"}</span>
              <span>{TRACK_ICONS[t.track] ?? "📚"}</span>
              <span className="truncate">{shortTrackName(t.track)}</span>
            </button>

            {/* Subjects within track */}
            {expandedTracks.has(t.track) && (
              <div className="ml-4 mt-0.5 space-y-0.5">
                {t.subjects.map((sub) => (
                  <div key={sub.id}>
                    <button
                      onClick={() => selectSubject(sub.id)}
                      className={`w-full text-left px-2 py-1 rounded text-sm transition-colors flex items-center justify-between ${
                        expandedSubject === sub.id
                          ? "bg-gh-accent/10 text-gh-accent"
                          : "text-gh-text hover:bg-gh-border/20"
                      }`}
                    >
                      <span className="truncate">{shortSubjectName(sub.name)}</span>
                      <span className="text-xs text-gh-muted ml-1 shrink-0">{sub.chapter_count}</span>
                    </button>

                    {/* Chapters within subject */}
                    {expandedSubject === sub.id && (
                      <div className="ml-3 mt-0.5 space-y-0.5">
                        {loadingChapters ? (
                          <p className="text-xs text-gh-muted px-2 py-1">Loading…</p>
                        ) : (
                          chapters.map((ch) => (
                            <button
                              key={ch.num}
                              onClick={() => onSelect(sub.id, ch.num)}
                              className={`w-full text-left px-2 py-1 rounded text-xs transition-colors ${
                                selectedSubjectId === sub.id && selectedChapterNum === ch.num
                                  ? "bg-gh-accent/15 text-gh-accent"
                                  : "text-gh-text hover:bg-gh-border/20"
                              }`}
                            >
                              <span className="font-mono text-gh-muted mr-1.5">{ch.num}</span>
                              <span className="truncate">{ch.title}</span>
                            </button>
                          ))
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </nav>
    </aside>
  );
}
