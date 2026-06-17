import { useEffect, useState } from "react";
import type { Track } from "./types";
import { fetchTracks } from "./api";
import Sidebar from "./components/Sidebar";
import ChapterView from "./components/ChapterView";
import DrillPane from "./components/DrillPane";

export default function App() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState<string | null>(null);
  const [selectedChapterNum, setSelectedChapterNum] = useState<string | null>(null);
  const [drillTrigger, setDrillTrigger] = useState(0);

  useEffect(() => {
    fetchTracks().then(setTracks);
  }, []);

  const handleSelect = (subjectId: string, chapterNum: string) => {
    setSelectedSubjectId(subjectId);
    setSelectedChapterNum(chapterNum);
  };

  return (
    <div className="h-screen grid grid-cols-[260px_1fr_1fr]">
      <Sidebar
        tracks={tracks}
        selectedSubjectId={selectedSubjectId}
        selectedChapterNum={selectedChapterNum}
        onSelect={handleSelect}
      />
      <main className="border-r border-gh-border overflow-hidden">
        {selectedSubjectId && selectedChapterNum ? (
          <ChapterView
            subjectId={selectedSubjectId}
            chapterNum={selectedChapterNum}
            onDrill={() => setDrillTrigger((t) => t + 1)}
          />
        ) : (
          <div className="h-full flex items-center justify-center text-gh-muted">
            Select a chapter from the sidebar.
          </div>
        )}
      </main>
      <section className="overflow-hidden">
        <DrillPane
          subjectId={selectedSubjectId}
          chapterNum={selectedChapterNum}
          trigger={drillTrigger}
        />
      </section>
    </div>
  );
}
