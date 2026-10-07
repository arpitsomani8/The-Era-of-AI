import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import MindMapPage from './MindMapPage';
import SyllabusPage from './SyllabusPage';

/**
 * KnowledgeHubPage: Unified curriculum portal hosting both the 
 * Interactive 2D Mind Map and Line-wise Syllabus on the same page.
 * Default view is 'mindmap'.
 */
export default function KnowledgeHubPage() {
  const location = useLocation();
  const navigate = useNavigate();

  // If path is '/syllabus', active view is 'syllabus', otherwise default is 'mindmap'
  const isSyllabus = location.pathname.toLowerCase().includes('/syllabus');

  return (
    <div className="relative w-full h-full flex-1 flex flex-col overflow-hidden">
      {isSyllabus ? (
        <SyllabusPage onSwitchToMindMap={() => navigate('/mindmap')} />
      ) : (
        <MindMapPage onSwitchToSyllabus={() => navigate('/syllabus')} />
      )}
    </div>
  );
}
