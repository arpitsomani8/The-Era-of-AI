import React, { useState, useRef, useEffect, useMemo, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  ZoomIn, 
  ZoomOut, 
  RotateCcw, 
  Share2, 
  Search, 
  Filter, 
  Info,
  Layers,
  ChevronRight
} from 'lucide-react';
import allNodesData from '../data/allNodes.json';
import crossLinksData from '../data/crossLinks.json';
import NodeInspector from '../components/NodeInspector';

export default function MindMapPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [selectedNodeId, setSelectedNodeId] = useState(() => searchParams.get('node') || null);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeDomain, setActiveDomain] = useState('all');
  const [showInterlinks, setShowInterlinks] = useState(true);

  // SVG Pan & Zoom Transform State
  const [transform, setTransform] = useState({ x: 0, y: 0, k: 0.85 });
  const [isDragging, setIsDragging] = useState(false);
  const dragStartRef = useRef({ x: 0, y: 0 });
  const svgRef = useRef(null);

  // Sync selected node with URL parameter
  useEffect(() => {
    const nodeFromParam = searchParams.get('node');
    if (nodeFromParam) {
      setSelectedNodeId(nodeFromParam);
    }
  }, [searchParams]);

  const handleSelectNode = (id) => {
    setSelectedNodeId(id);
    if (id) {
      setSearchParams({ node: id });
    } else {
      setSearchParams({});
    }
  };

  const selectedNode = useMemo(() => {
    return allNodesData.find((n) => n.id === selectedNodeId) || null;
  }, [selectedNodeId]);

  // Color scheme by category
  const categoryConfig = {
    center: { fill: '#4f46e5', stroke: '#818cf8', text: '#ffffff', label: 'Universe' },
    math: { fill: '#1e3a8a', stroke: '#3b82f6', text: '#93c5fd', label: 'Math' },
    data: { fill: '#064e3b', stroke: '#10b981', text: '#6ee7b7', label: 'Data Preprocessing' },
    ml: { fill: '#581c87', stroke: '#a855f7', text: '#d8b4fe', label: 'Classical ML' },
    eval: { fill: '#78350f', stroke: '#f59e0b', text: '#fcd34d', label: 'Evaluation' },
    dl: { fill: '#831843', stroke: '#ec4899', text: '#fbcfe8', label: 'Deep Learning' },
    genai: { fill: '#312e81', stroke: '#6366f1', text: '#c7d2fe', label: 'GenAI & LLMs' },
    mlops: { fill: '#134e4a', stroke: '#14b8a6', text: '#99f6e4', label: 'MLOps' }
  };

  // Center the view on initial mount
  useEffect(() => {
    if (svgRef.current) {
      const rect = svgRef.current.getBoundingClientRect();
      setTransform({
        x: rect.width / 2,
        y: rect.height / 2,
        k: 0.8
      });
    }
  }, []);

  // Filtered nodes
  const filteredNodes = useMemo(() => {
    return allNodesData.filter((node) => {
      // Domain filter
      if (activeDomain !== 'all') {
        if (node.id !== 'root' && node.category !== activeDomain) {
          return false;
        }
      }
      // Search query
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchLabel = node.label?.toLowerCase().includes(q);
        const matchDef = node.def?.toLowerCase().includes(q);
        const matchSub = node.subtopics?.some((s) => s.toLowerCase().includes(q));
        if (!matchLabel && !matchDef && !matchSub) return false;
      }
      return true;
    });
  }, [activeDomain, searchQuery]);

  // Hierarchy lines calculation
  const hierarchyLinks = useMemo(() => {
    const links = [];
    const nodeMap = new Map(allNodesData.map((n) => [n.id, n]));

    for (const node of allNodesData) {
      if (node.connections) {
        for (const targetId of node.connections) {
          const target = nodeMap.get(targetId);
          if (target) {
            links.push({
              source: node,
              target: target,
              id: `${node.id}-${target.id}`
            });
          }
        }
      }
    }
    return links;
  }, []);

  // Pan handlers
  const handleMouseDown = (e) => {
    if (e.button !== 0) return; // Only left click
    setIsDragging(true);
    dragStartRef.current = {
      x: e.clientX - transform.x,
      y: e.clientY - transform.y
    };
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setTransform((prev) => ({
      ...prev,
      x: e.clientX - dragStartRef.current.x,
      y: e.clientY - dragStartRef.current.y
    }));
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.12 : 0.88;
    setTransform((prev) => {
      const newScale = Math.min(Math.max(prev.k * zoomFactor, 0.2), 3.0);
      return {
        ...prev,
        k: newScale
      };
    });
  };

  const zoom = (direction) => {
    const factor = direction > 0 ? 1.25 : 0.8;
    setTransform((prev) => ({
      ...prev,
      k: Math.min(Math.max(prev.k * factor, 0.2), 3.0)
    }));
  };

  const resetView = () => {
    if (svgRef.current) {
      const rect = svgRef.current.getBoundingClientRect();
      setTransform({
        x: rect.width / 2,
        y: rect.height / 2,
        k: 0.8
      });
    }
  };

  return (
    <div className="relative flex-1 w-full h-full overflow-hidden flex flex-col bg-slate-950 select-none">
      {/* Mindmap Toolbar */}
      <div className="bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-4 py-2 flex flex-wrap items-center justify-between gap-2 z-10 shrink-0">
        <div className="flex items-center space-x-2 flex-wrap gap-y-1">
          {/* Search Box */}
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search 34+ modules (AdamW, LoRA, ROC)..."
              className="bg-slate-950 border border-slate-800 text-xs text-white rounded-lg pl-8 pr-4 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 w-52 md:w-72 placeholder-slate-500"
            />
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-500" />
            {searchQuery && (
              <button 
                onClick={() => setSearchQuery('')}
                className="absolute right-2 top-2 text-slate-500 hover:text-white text-xs"
              >
                &times;
              </button>
            )}
          </div>

          {/* Domain Filter Pills */}
          <div className="hidden lg:flex items-center space-x-1 text-xs">
            {[
              { id: 'all', label: 'All' },
              { id: 'math', label: 'Math' },
              { id: 'data', label: 'Data' },
              { id: 'ml', label: 'Classical ML' },
              { id: 'eval', label: 'Evaluation' },
              { id: 'dl', label: 'Deep Learning' },
              { id: 'genai', label: 'GenAI & LLM' }
            ].map((dom) => (
              <button
                key={dom.id}
                onClick={() => setActiveDomain(dom.id)}
                className={`px-2.5 py-1 rounded-md text-xs font-medium transition ${
                  activeDomain === dom.id
                    ? 'bg-indigo-600 text-white shadow'
                    : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {dom.label}
              </button>
            ))}
          </div>
        </div>

        {/* Zoom & View Controls */}
        <div className="flex items-center space-x-1.5 text-xs">
          <button
            onClick={() => zoom(1)}
            title="Zoom In"
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={() => zoom(-1)}
            title="Zoom Out"
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={resetView}
            title="Reset View to Center"
            className="p-1.5 px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition flex items-center gap-1 font-medium"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset</span>
          </button>
          <button
            onClick={() => setShowInterlinks(!showInterlinks)}
            title="Toggle Inter-Domain Cross-Links"
            className={`p-1.5 px-2.5 rounded-lg border transition text-xs font-semibold flex items-center gap-1.5 ${
              showInterlinks
                ? 'bg-indigo-600/20 text-indigo-300 border-indigo-500/40 hover:bg-indigo-600/30'
                : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-white'
            }`}
          >
            <Share2 className="w-3.5 h-3.5" />
            <span>Links: {showInterlinks ? 'ON' : 'OFF'}</span>
          </button>
        </div>
      </div>

      {/* SVG Canvas Area */}
      <div
        className={`relative flex-1 w-full h-full overflow-hidden ${
          isDragging ? 'grabbing-cursor' : 'grab-cursor'
        }`}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
      >
        {/* Subtle Background Grid Pattern */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-20">
          <defs>
            <pattern id="gridPattern" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="0.8" className="text-slate-700" />
              <circle cx="0" cy="0" r="1.2" fill="currentColor" className="text-slate-600" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#gridPattern)" />
        </svg>

        {/* Dynamic Zoomable Graph SVG */}
        <svg ref={svgRef} className="w-full h-full overflow-visible">
          <defs>
            {/* Arrowhead marker for cross links */}
            <marker
              id="arrowhead-cross"
              markerWidth="8"
              markerHeight="6"
              refX="7"
              refY="3"
              orient="auto"
            >
              <polygon points="0 0, 8 3, 0 6" fill="#f59e0b" />
            </marker>
          </defs>

          <g transform={`translate(${transform.x}, ${transform.y}) scale(${transform.k})`}>
            {/* 1. Hierarchy Lines (Root -> Hubs -> Topics) */}
            <g id="hierarchyLines">
              {hierarchyLinks.map((link) => {
                const isSelected = selectedNodeId === link.source.id || selectedNodeId === link.target.id;
                return (
                  <line
                    key={link.id}
                    x1={link.source.x || 0}
                    y1={link.source.y || 0}
                    x2={link.target.x || 0}
                    y2={link.target.y || 0}
                    stroke={isSelected ? '#818cf8' : '#334155'}
                    strokeWidth={isSelected ? 2.5 : 1.5}
                    strokeDasharray={link.source.level === 0 ? '4 4' : 'none'}
                    className="transition-colors duration-200"
                  />
                );
              })}
            </g>

            {/* 2. Cross-Domain Links */}
            {showInterlinks && (
              <g id="crossLinks">
                {crossLinksData.map((link, idx) => {
                  const nodeMap = new Map(allNodesData.map((n) => [n.id, n]));
                  const fromNode = nodeMap.get(link.from);
                  const toNode = nodeMap.get(link.to);
                  if (!fromNode || !toNode) return null;

                  const isLinkedToSelected = selectedNodeId === link.from || selectedNodeId === link.to;

                  // Curved path calculation
                  const dx = (toNode.x || 0) - (fromNode.x || 0);
                  const dy = (toNode.y || 0) - (fromNode.y || 0);
                  const cx = (fromNode.x || 0) + dx * 0.5 - dy * 0.2;
                  const cy = (fromNode.y || 0) + dy * 0.5 + dx * 0.2;

                  return (
                    <g key={idx} className="cursor-pointer group">
                      <path
                        d={`M ${fromNode.x || 0} ${fromNode.y || 0} Q ${cx} ${cy} ${toNode.x || 0} ${toNode.y || 0}`}
                        fill="none"
                        stroke={isLinkedToSelected ? '#fbbf24' : '#f59e0b'}
                        strokeWidth={isLinkedToSelected ? 2.5 : 1.2}
                        strokeDasharray="5,5"
                        strokeOpacity={isLinkedToSelected ? 0.95 : 0.45}
                        markerEnd="url(#arrowhead-cross)"
                      />
                    </g>
                  );
                })}
              </g>
            )}

            {/* 3. Node Elements */}
            <g id="nodesGroup">
              {filteredNodes.map((node) => {
                const isSelected = selectedNodeId === node.id;
                const cfg = categoryConfig[node.category] || categoryConfig.ml;
                const isRoot = node.level === 0;
                const isHub = node.level === 1;

                const nodeWidth = isRoot ? 260 : isHub ? 210 : 180;
                const nodeHeight = isRoot ? 60 : isHub ? 48 : 42;
                const rx = isRoot ? 16 : 10;

                return (
                  <g
                    key={node.id}
                    transform={`translate(${node.x || 0}, ${node.y || 0})`}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleSelectNode(node.id);
                    }}
                    className="cursor-pointer group"
                  >
                    {/* Node background pill */}
                    <rect
                      x={-nodeWidth / 2}
                      y={-nodeHeight / 2}
                      width={nodeWidth}
                      height={nodeHeight}
                      rx={rx}
                      fill={isSelected ? '#1e1b4b' : isRoot ? '#312e81' : '#0f172a'}
                      stroke={isSelected ? '#a5b4fc' : cfg.stroke}
                      strokeWidth={isSelected ? 3 : isHub ? 2 : 1.5}
                      filter="drop-shadow(0 4px 6px rgba(0,0,0,0.4))"
                      className="transition-all duration-200 group-hover:scale-105"
                    />

                    {/* Small category indicator dot */}
                    <circle
                      cx={-nodeWidth / 2 + 16}
                      cy={0}
                      r={isRoot ? 6 : 4}
                      fill={cfg.stroke}
                    />

                    {/* Node text label */}
                    <text
                      x={-nodeWidth / 2 + 28}
                      y={4}
                      fill={isSelected ? '#ffffff' : '#f8fafc'}
                      fontSize={isRoot ? 14 : isHub ? 12 : 11}
                      fontWeight={isRoot ? '700' : isHub ? '600' : '500'}
                      fontFamily="system-ui, sans-serif"
                    >
                      {node.label}
                    </text>
                  </g>
                );
              })}
            </g>
          </g>
        </svg>

        {/* Legend Overlay at bottom-left */}
        <div className="absolute bottom-4 left-4 bg-slate-900/90 backdrop-blur-md border border-slate-800 rounded-xl px-4 py-2 text-xs text-slate-300 shadow-xl pointer-events-none hidden md:flex items-center space-x-4">
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
            <span>Math</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
            <span>Data</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
            <span>Classical ML</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-pink-500"></span>
            <span>Deep Learning</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
            <span>GenAI & LLMs</span>
          </div>
          <div className="text-slate-500 border-l border-slate-700 pl-3">
            Drag to pan &bull; Scroll to zoom &bull; Click node to inspect details
          </div>
        </div>
      </div>

      {/* Slide-over Inspector Drawer for Node Details */}
      <NodeInspector
        node={selectedNode}
        crossLinks={crossLinksData}
        onClose={() => handleSelectNode(null)}
        onSelectNode={handleSelectNode}
      />
    </div>
  );
}
