import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  StepForward, 
  Sliders, 
  Layers, 
  Cpu, 
  Zap, 
  Sparkles, 
  Activity, 
  Calculator, 
  TrendingDown,
  Info,
  CheckCircle2
} from 'lucide-react';
import KaTeXRenderer from './KaTeXRenderer';

// 2D TOY DATASET GENERATORS
function generateDataset(type, count = 160, noise = 0.15) {
  const points = [];
  const half = Math.floor(count / 2);

  if (type === 'circles') {
    // Inner circle (class 0), outer ring (class 1)
    for (let i = 0; i < half; i++) {
      const r = (Math.random() * 0.45);
      const theta = Math.random() * Math.PI * 2;
      points.push({
        x: r * Math.cos(theta) + (Math.random() - 0.5) * noise,
        y: r * Math.sin(theta) + (Math.random() - 0.5) * noise,
        label: 0
      });
    }
    for (let i = 0; i < half; i++) {
      const r = 0.65 + (Math.random() * 0.35);
      const theta = Math.random() * Math.PI * 2;
      points.push({
        x: r * Math.cos(theta) + (Math.random() - 0.5) * noise,
        y: r * Math.sin(theta) + (Math.random() - 0.5) * noise,
        label: 1
      });
    }
  } else if (type === 'xor') {
    for (let i = 0; i < count; i++) {
      const x = (Math.random() * 2 - 1) * 0.9;
      const y = (Math.random() * 2 - 1) * 0.9;
      const margin = 0.08;
      const xAdj = x + (x > 0 ? margin : -margin);
      const yAdj = y + (y > 0 ? margin : -margin);
      const label = (xAdj * yAdj > 0) ? 1 : 0;
      points.push({
        x: x + (Math.random() - 0.5) * noise,
        y: y + (Math.random() - 0.5) * noise,
        label
      });
    }
  } else if (type === 'moons') {
    for (let i = 0; i < half; i++) {
      const angle = (i / half) * Math.PI;
      points.push({
        x: Math.cos(angle) * 0.65 - 0.3 + (Math.random() - 0.5) * noise,
        y: Math.sin(angle) * 0.65 - 0.15 + (Math.random() - 0.5) * noise,
        label: 0
      });
    }
    for (let i = 0; i < half; i++) {
      const angle = (i / half) * Math.PI;
      points.push({
        x: 0.3 - Math.cos(angle) * 0.65 + (Math.random() - 0.5) * noise,
        y: 0.15 - Math.sin(angle) * 0.65 + (Math.random() - 0.5) * noise,
        label: 1
      });
    }
  } else if (type === 'spiral') {
    for (let i = 0; i < half; i++) {
      const r = (i / half) * 0.9 + 0.1;
      const t = 1.75 * i / half * 2 * Math.PI;
      points.push({
        x: r * Math.sin(t) + (Math.random() - 0.5) * noise,
        y: r * Math.cos(t) + (Math.random() - 0.5) * noise,
        label: 0
      });
    }
    for (let i = 0; i < half; i++) {
      const r = (i / half) * 0.9 + 0.1;
      const t = 1.75 * i / half * 2 * Math.PI + Math.PI;
      points.push({
        x: r * Math.sin(t) + (Math.random() - 0.5) * noise,
        y: r * Math.cos(t) + (Math.random() - 0.5) * noise,
        label: 1
      });
    }
  }

  return points;
}

// ACTIVATION FUNCTIONS & DERIVATIVES
const ACTIVATIONS = {
  relu: {
    fn: (x) => Math.max(0, x),
    df: (x) => (x > 0 ? 1 : 0),
    name: 'ReLU',
    formula: 'f(x) = \\max(0, x)'
  },
  tanh: {
    fn: (x) => Math.tanh(x),
    df: (x) => 1 - Math.tanh(x) ** 2,
    name: 'Tanh',
    formula: 'f(x) = \\tanh(x)'
  },
  sigmoid: {
    fn: (x) => 1 / (1 + Math.exp(-Math.max(-15, Math.min(15, x)))),
    df: (x) => {
      const s = 1 / (1 + Math.exp(-Math.max(-15, Math.min(15, x))));
      return s * (1 - s);
    },
    name: 'Sigmoid',
    formula: 'f(x) = \\frac{1}{1 + e^{-x}}'
  },
  gelu: {
    fn: (x) => 0.5 * x * (1 + Math.tanh(Math.sqrt(2 / Math.PI) * (x + 0.044715 * x ** 3))),
    df: (x) => {
      const c = Math.sqrt(2 / Math.PI);
      const inner = c * (x + 0.044715 * x ** 3);
      const tanhVal = Math.tanh(inner);
      const sech2 = 1 - tanhVal * tanhVal;
      return 0.5 * (1 + tanhVal) + 0.5 * x * sech2 * c * (1 + 3 * 0.044715 * x * x);
    },
    name: 'GELU',
    formula: 'f(x) = x \\Phi(x)'
  }
};

export default function NeuralNetworkPlayground() {
  // Settings
  const [datasetType, setDatasetType] = useState('circles'); // 'circles' | 'moons' | 'xor' | 'spiral'
  const [hiddenLayers, setHiddenLayers] = useState([4, 4]); // Neurons per hidden layer (1-3 layers, 2-8 neurons)
  const [activation, setActivation] = useState('tanh');
  const [learningRate, setLearningRate] = useState(0.12);
  const [isTraining, setIsTraining] = useState(false);
  const [epoch, setEpoch] = useState(0);
  const [lossHistory, setLossHistory] = useState([]);
  const [currentLoss, setCurrentLoss] = useState(0.69);
  const [currentAccuracy, setCurrentAccuracy] = useState(50);
  const [hoveredNeuron, setHoveredNeuron] = useState(null);

  const canvasRef = useRef(null);
  const networkRef = useRef(null);
  const animFrameIdRef = useRef(null);

  // Generate Dataset Points
  const dataset = useMemo(() => {
    return generateDataset(datasetType, 160, 0.12);
  }, [datasetType]);

  // Initialize Network Parameters (Xavier / He initialization)
  const initNetwork = useCallback((layers, actKey) => {
    const layerSizes = [2, ...layers, 1]; // Input: (x, y), Output: probability
    const weights = [];
    const biases = [];

    for (let l = 0; l < layerSizes.length - 1; l++) {
      const inDim = layerSizes[l];
      const outDim = layerSizes[l + 1];
      const std = Math.sqrt(2 / (inDim + outDim));
      
      const W = [];
      for (let i = 0; i < inDim; i++) {
        const row = [];
        for (let j = 0; j < outDim; j++) {
          row.push((Math.random() * 2 - 1) * std);
        }
        W.push(row);
      }
      weights.push(W);

      const b = new Array(outDim).fill(0).map(() => (Math.random() - 0.5) * 0.05);
      biases.push(b);
    }

    networkRef.current = {
      layerSizes,
      weights,
      biases,
      activation: actKey
    };
    setEpoch(0);
    setLossHistory([]);
  }, []);

  // Reset or initialize on layer/activation changes
  useEffect(() => {
    initNetwork(hiddenLayers, activation);
  }, [hiddenLayers, activation, datasetType, initNetwork]);

  // Forward Pass for a Single Input Vector [x, y]
  const forwardOne = useCallback((input) => {
    const net = networkRef.current;
    if (!net) return { output: 0.5, activations: [[input[0], input[1]]] };

    const act = ACTIVATIONS[net.activation] || ACTIVATIONS.tanh;
    const activations = [[input[0], input[1]]];
    const preActivations = [];

    let current = [input[0], input[1]];

    for (let l = 0; l < net.weights.length; l++) {
      const W = net.weights[l];
      const b = net.biases[l];
      const next = [];
      const zRow = [];

      const isOutput = l === net.weights.length - 1;

      for (let j = 0; j < b.length; j++) {
        let sum = b[j];
        for (let i = 0; i < current.length; i++) {
          sum += current[i] * W[i][j];
        }
        zRow.push(sum);
        // Final layer uses Sigmoid for binary probability output
        const val = isOutput 
          ? (1 / (1 + Math.exp(-Math.max(-15, Math.min(15, sum)))))
          : act.fn(sum);
        next.push(val);
      }
      preActivations.push(zRow);
      activations.push(next);
      current = next;
    }

    return {
      output: current[0],
      activations,
      preActivations
    };
  }, []);

  // Single Step Training: Forward & Backprop on Mini-Batch
  const trainStep = useCallback(() => {
    const net = networkRef.current;
    if (!net || dataset.length === 0) return;

    const act = ACTIVATIONS[net.activation] || ACTIVATIONS.tanh;
    const N = dataset.length;

    // Accumulate Gradients
    const dW = net.weights.map(layer => layer.map(row => new Array(row.length).fill(0)));
    const dB = net.biases.map(layer => new Array(layer.length).fill(0));

    let totalLoss = 0;
    let correctCount = 0;

    for (let p = 0; p < N; p++) {
      const pt = dataset[p];
      const { output, activations, preActivations } = forwardOne([pt.x, pt.y]);

      const pred = Math.max(1e-7, Math.min(1 - 1e-7, output));
      const target = pt.label;

      // Binary Cross Entropy Loss: -(y*log(p) + (1-y)*log(1-p))
      const loss = -(target * Math.log(pred) + (1 - target) * Math.log(1 - pred));
      totalLoss += loss;

      if ((pred >= 0.5 ? 1 : 0) === target) {
        correctCount++;
      }

      // Backpropagation Output Layer Error: delta = pred - target
      let delta = [pred - target];

      for (let l = net.weights.length - 1; l >= 0; l--) {
        const A_prev = activations[l];
        const W = net.weights[l];
        const nextDelta = new Array(A_prev.length).fill(0);

        for (let j = 0; j < delta.length; j++) {
          const d_j = delta[j];
          dB[l][j] += d_j;

          for (let i = 0; i < A_prev.length; i++) {
            dW[l][i][j] += A_prev[i] * d_j;

            // Backpropagate to previous layer
            if (l > 0) {
              nextDelta[i] += d_j * W[i][j];
            }
          }
        }

        if (l > 0) {
          const z_prev = preActivations[l - 1];
          for (let i = 0; i < nextDelta.length; i++) {
            nextDelta[i] *= act.df(z_prev[i]);
          }
          delta = nextDelta;
        }
      }
    }

    // Gradient Descent Update with Learning Rate
    const lr = learningRate / N;
    for (let l = 0; l < net.weights.length; l++) {
      for (let i = 0; i < net.weights[l].length; i++) {
        for (let j = 0; j < net.weights[l][i].length; j++) {
          net.weights[l][i][j] -= lr * dW[l][i][j];
        }
      }
      for (let j = 0; j < net.biases[l].length; j++) {
        net.biases[l][j] -= lr * dB[l][j];
      }
    }

    const avgLoss = totalLoss / N;
    const acc = Math.round((correctCount / N) * 100);

    setCurrentLoss(avgLoss);
    setCurrentAccuracy(acc);
    setEpoch(prev => prev + 1);
    setLossHistory(prev => [...prev.slice(-39), avgLoss]);
  }, [dataset, forwardOne, learningRate]);

  // Training Animation Loop
  useEffect(() => {
    if (!isTraining) return;

    let isMounted = true;
    const loop = () => {
      if (!isMounted) return;
      // Perform 2 mini-batches per frame for smooth real-time convergence
      trainStep();
      trainStep();
      animFrameIdRef.current = requestAnimationFrame(loop);
    };

    animFrameIdRef.current = requestAnimationFrame(loop);

    return () => {
      isMounted = false;
      if (animFrameIdRef.current) cancelAnimationFrame(animFrameIdRef.current);
    };
  }, [isTraining, trainStep]);

  // Render 2D Decision Boundary Heatmap Canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const width = (canvas.width = 320);
    const height = (canvas.height = 320);

    const resolution = 40; // 40x40 decision grid
    const cellW = width / resolution;
    const cellH = height / resolution;

    // Draw Decision Heatmap
    for (let gx = 0; gx < resolution; gx++) {
      for (let gy = 0; gy < resolution; gy++) {
        // Map grid cell center to coordinate space [-1.2, 1.2]
        const nx = ((gx + 0.5) / resolution) * 2.4 - 1.2;
        const ny = (1 - (gy + 0.5) / resolution) * 2.4 - 1.2;

        const { output } = forwardOne([nx, ny]);

        // Class 0 = Cyan/Blue, Class 1 = Rose/Amber
        const r = Math.round(output * 244 + (1 - output) * 30);
        const g = Math.round(output * 63 + (1 - output) * 144);
        const b = Math.round(output * 94 + (1 - output) * 255);

        ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
        ctx.fillRect(gx * cellW, gy * cellH, cellW + 1, cellH + 1);
      }
    }

    // Draw Coordinate Axis
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, height / 2);
    ctx.lineTo(width, height / 2);
    ctx.moveTo(width / 2, 0);
    ctx.lineTo(width / 2, height);
    ctx.stroke();

    // Draw Dataset Points
    for (const pt of dataset) {
      const px = ((pt.x + 1.2) / 2.4) * width;
      const py = ((1.2 - pt.y) / 2.4) * height;

      ctx.beginPath();
      ctx.arc(px, py, 4, 0, Math.PI * 2);
      ctx.fillStyle = pt.label === 1 ? '#fb7185' : '#38bdf8';
      ctx.fill();

      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
  }, [dataset, forwardOne, epoch]);

  // Helper for adding/removing layers
  const addLayer = () => {
    if (hiddenLayers.length < 3) {
      setHiddenLayers([...hiddenLayers, 4]);
    }
  };

  const removeLayer = () => {
    if (hiddenLayers.length > 1) {
      setHiddenLayers(hiddenLayers.slice(0, -1));
    }
  };

  const setNeuronCount = (layerIdx, count) => {
    const next = [...hiddenLayers];
    next[layerIdx] = Math.max(2, Math.min(8, count));
    setHiddenLayers(next);
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Top Header Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <Cpu className="w-4 h-4" />
              </span>
              <h2 className="text-base font-bold text-white tracking-wide">
                Interactive Neural Network Playground
              </h2>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-mono">
                Live Backprop
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Design multi-layer perceptron architectures, choose nonlinear activation functions, and inspect real-time decision boundary separation and gradient weight updates.
            </p>
          </div>

          {/* Quick Metrics Badge */}
          <div className="flex items-center gap-3 bg-slate-950 p-2 px-4 rounded-xl border border-slate-800/80 text-xs shrink-0">
            <div>
              <span className="text-[10px] text-slate-500 block uppercase font-mono">Epoch</span>
              <span className="font-mono font-bold text-white">{epoch}</span>
            </div>
            <div className="w-[1px] h-6 bg-slate-800" />
            <div>
              <span className="text-[10px] text-slate-500 block uppercase font-mono">Loss (BCE)</span>
              <span className="font-mono font-bold text-amber-400">{currentLoss.toFixed(4)}</span>
            </div>
            <div className="w-[1px] h-6 bg-slate-800" />
            <div>
              <span className="text-[10px] text-slate-500 block uppercase font-mono">Accuracy</span>
              <span className={`font-mono font-bold ${currentAccuracy > 85 ? 'text-emerald-400' : 'text-cyan-400'}`}>
                {currentAccuracy}%
              </span>
            </div>
          </div>
        </div>

        {/* Global Controls Row */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-3 border-t border-slate-800/80">
          {/* Dataset Selector */}
          <div className="space-y-1">
            <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Classification Problem:
            </label>
            <div className="grid grid-cols-2 gap-1.5">
              {[
                { id: 'circles', label: 'Circles' },
                { id: 'moons', label: 'Two Moons' },
                { id: 'xor', label: 'XOR Grid' },
                { id: 'spiral', label: 'Spiral' }
              ].map(d => (
                <button
                  key={d.id}
                  onClick={() => {
                    setIsTraining(false);
                    setDatasetType(d.id);
                  }}
                  className={`px-2.5 py-1.5 rounded-lg text-xs font-medium transition text-left truncate ${
                    datasetType === d.id
                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm'
                      : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                  }`}
                >
                  {d.label}
                </button>
              ))}
            </div>
          </div>

          {/* Activation Selector */}
          <div className="space-y-1">
            <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Hidden Activation:
            </label>
            <div className="grid grid-cols-2 gap-1.5">
              {Object.keys(ACTIVATIONS).map(actKey => (
                <button
                  key={actKey}
                  onClick={() => {
                    setActivation(actKey);
                  }}
                  className={`px-2.5 py-1.5 rounded-lg text-xs font-medium transition text-left truncate ${
                    activation === actKey
                      ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 shadow-sm'
                      : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                  }`}
                >
                  {ACTIVATIONS[actKey].name}
                </button>
              ))}
            </div>
          </div>

          {/* Learning Rate Slider */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <span>Learning Rate (<KaTeXRenderer math="\alpha" inline={true} />):</span>
              <span className="text-emerald-400 font-mono">{learningRate.toFixed(2)}</span>
            </div>
            <input
              type="range"
              min="0.02"
              max="0.5"
              step="0.02"
              value={learningRate}
              onChange={(e) => setLearningRate(parseFloat(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono">
              <span>0.02 (Stable)</span>
              <span>0.50 (Aggressive)</span>
            </div>
          </div>

          {/* Action Buttons: Play/Pause/Step/Reset */}
          <div className="space-y-1">
            <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Training Loop:
            </label>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsTraining(!isTraining)}
                className={`flex-1 py-2 px-3 rounded-xl font-semibold text-xs transition flex items-center justify-center gap-1.5 shadow-md ${
                  isTraining
                    ? 'bg-amber-600 hover:bg-amber-500 text-white shadow-amber-600/30'
                    : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-600/30'
                }`}
              >
                {isTraining ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
                <span>{isTraining ? 'Pause' : 'Train'}</span>
              </button>

              <button
                onClick={() => {
                  setIsTraining(false);
                  trainStep();
                }}
                className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition"
                title="Single Epoch Step"
              >
                <StepForward className="w-4 h-4" />
              </button>

              <button
                onClick={() => {
                  setIsTraining(false);
                  initNetwork(hiddenLayers, activation);
                }}
                className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition"
                title="Reset Weights"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Interactive Grid: Decision Boundary + Physical Synaptic Architecture */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left: 2D Decision Boundary Canvas & Live Loss Curve */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                <Activity className="w-3.5 h-3.5 text-emerald-400" />
                2D Decision Boundary Heatmap
              </h3>
              <div className="flex items-center gap-2 text-[10px] font-mono text-slate-400">
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-cyan-400" />
                  Class 0
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-rose-400" />
                  Class 1
                </span>
              </div>
            </div>

            {/* Canvas Container */}
            <div className="flex justify-center p-2 bg-slate-950 rounded-2xl border border-slate-800/80 shadow-inner">
              <canvas
                ref={canvasRef}
                className="w-full max-w-[280px] aspect-square rounded-xl shadow-lg"
              />
            </div>

            {/* Mini Real-Time Loss Curve */}
            <div className="space-y-1.5 pt-2 border-t border-slate-800/80">
              <div className="flex items-center justify-between text-[11px] text-slate-400">
                <span className="flex items-center gap-1 font-mono">
                  <TrendingDown className="w-3.5 h-3.5 text-emerald-400" />
                  Loss History (Last 40 epochs)
                </span>
                <span className="font-mono text-white text-[10px]">
                  {lossHistory.length > 0 ? lossHistory[lossHistory.length - 1].toFixed(4) : '0.0000'}
                </span>
              </div>

              <div className="h-16 w-full bg-slate-950 rounded-xl border border-slate-800/80 p-2 flex items-end gap-1">
                {lossHistory.map((val, idx) => {
                  const maxLoss = 1.5;
                  const barHeight = Math.min(100, Math.max(8, (val / maxLoss) * 100));
                  return (
                    <div
                      key={`loss-${idx}`}
                      className="flex-1 bg-gradient-to-t from-emerald-600 to-cyan-400 rounded-t transition-all duration-150"
                      style={{ height: `${barHeight}%` }}
                      title={`Epoch -${lossHistory.length - idx}: Loss ${val.toFixed(4)}`}
                    />
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* Right: Neural Architecture & Synapse Weight Graph */}
        <div className="lg:col-span-7 space-y-4">
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-3 flex-wrap gap-2">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-indigo-400" />
                Network Architecture & Synaptic Weights
              </h3>

              {/* Layer Manipulation Controls */}
              <div className="flex items-center gap-2">
                <button
                  onClick={removeLayer}
                  disabled={hiddenLayers.length <= 1}
                  className="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300 text-xs font-mono"
                  title="Remove Hidden Layer"
                >
                  - Layer
                </button>
                <span className="text-[11px] font-mono text-indigo-300">
                  {hiddenLayers.length} Hidden Layer{hiddenLayers.length > 1 ? 's' : ''}
                </span>
                <button
                  onClick={addLayer}
                  disabled={hiddenLayers.length >= 3}
                  className="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300 text-xs font-mono"
                  title="Add Hidden Layer"
                >
                  + Layer
                </button>
              </div>
            </div>

            {/* Neuron Count Steppers per Hidden Layer */}
            <div className="flex items-center gap-3 overflow-x-auto pb-1">
              <div className="p-2 rounded-xl bg-slate-950 border border-slate-800 text-[11px] text-slate-400 shrink-0">
                <span className="text-cyan-400 font-bold block">Input Layer</span>
                <span>2 Features ($X_1, X_2$)</span>
              </div>

              {hiddenLayers.map((count, lIdx) => (
                <div 
                  key={`layer-ctrl-${lIdx}`}
                  className="p-2 rounded-xl bg-slate-950 border border-slate-800 text-[11px] text-slate-400 flex items-center gap-2 shrink-0"
                >
                  <div>
                    <span className="text-indigo-400 font-bold block">Hidden #{lIdx + 1}</span>
                    <span>{count} Neurons</span>
                  </div>
                  <div className="flex flex-col gap-0.5">
                    <button
                      onClick={() => setNeuronCount(lIdx, count + 1)}
                      disabled={count >= 8}
                      className="px-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-[9px] disabled:opacity-30"
                    >
                      ▲
                    </button>
                    <button
                      onClick={() => setNeuronCount(lIdx, count - 1)}
                      disabled={count <= 2}
                      className="px-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-[9px] disabled:opacity-30"
                    >
                      ▼
                    </button>
                  </div>
                </div>
              ))}

              <div className="p-2 rounded-xl bg-slate-950 border border-slate-800 text-[11px] text-slate-400 shrink-0">
                <span className="text-rose-400 font-bold block">Output Layer</span>
                <span>Sigmoid (<KaTeXRenderer math="\hat{y} \in [0, 1]" inline={true} />)</span>
              </div>
            </div>

            {/* SVG Visual Neural Graph */}
            <div className="relative bg-slate-950 rounded-2xl border border-slate-800 p-4 overflow-hidden min-h-[260px] flex items-center justify-center">
              {networkRef.current && (
                <svg className="w-full h-64" viewBox="0 0 540 240">
                  {/* Synaptic Weights (Lines) */}
                  {networkRef.current.weights.map((layerW, lIdx) => {
                    const layerSizes = networkRef.current.layerSizes;
                    const inCount = layerSizes[lIdx];
                    const outCount = layerSizes[lIdx + 1];

                    const x1 = 70 + lIdx * (400 / (layerSizes.length - 1));
                    const x2 = 70 + (lIdx + 1) * (400 / (layerSizes.length - 1));

                    return layerW.map((row, i) => {
                      const y1 = 120 + (i - (inCount - 1) / 2) * Math.min(42, 200 / inCount);

                      return row.map((wVal, j) => {
                        const y2 = 120 + (j - (outCount - 1) / 2) * Math.min(42, 200 / outCount);
                        const isPos = wVal >= 0;
                        const absW = Math.min(4, Math.abs(wVal) * 1.5 + 0.5);

                        return (
                          <line
                            key={`syn-${lIdx}-${i}-${j}`}
                            x1={x1}
                            y1={y1}
                            x2={x2}
                            y2={y2}
                            stroke={isPos ? '#38bdf8' : '#f43f5e'}
                            strokeWidth={absW}
                            strokeOpacity={Math.min(0.85, Math.abs(wVal) * 0.4 + 0.2)}
                          />
                        );
                      });
                    });
                  })}

                  {/* Neurons (Circles) */}
                  {networkRef.current.layerSizes.map((count, lIdx) => {
                    const totalLayers = networkRef.current.layerSizes.length;
                    const cx = 70 + lIdx * (400 / (totalLayers - 1));
                    const isInput = lIdx === 0;
                    const isOutput = lIdx === totalLayers - 1;

                    return Array.from({ length: count }).map((_, nIdx) => {
                      const cy = 120 + (nIdx - (count - 1) / 2) * Math.min(42, 200 / count);
                      const isHovered = hoveredNeuron && hoveredNeuron.l === lIdx && hoveredNeuron.n === nIdx;

                      return (
                        <g 
                          key={`neuron-${lIdx}-${nIdx}`}
                          onMouseEnter={() => setHoveredNeuron({ l: lIdx, n: nIdx })}
                          onMouseLeave={() => setHoveredNeuron(null)}
                          className="cursor-pointer"
                        >
                          <circle
                            cx={cx}
                            cy={cy}
                            r={isHovered ? 13 : 10}
                            fill={isInput ? '#0284c7' : isOutput ? '#e11d48' : '#4f46e5'}
                            stroke="#ffffff"
                            strokeWidth={isHovered ? 2.5 : 1.5}
                            className="transition-all duration-150"
                          />
                          <text
                            x={cx}
                            y={cy + 3}
                            textAnchor="middle"
                            fontSize="9"
                            fill="#ffffff"
                            fontWeight="bold"
                            className="pointer-events-none font-mono"
                          >
                            {isInput ? (nIdx === 0 ? 'X₁' : 'X₂') : isOutput ? 'ŷ' : `h${nIdx + 1}`}
                          </text>
                        </g>
                      );
                    });
                  })}
                </svg>
              )}
            </div>

            {/* Educational Formula & Legend Footnote */}
            <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-[11px] text-slate-400 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-slate-300">Synapse Legend:</span>
                <span className="text-[10px] font-mono text-cyan-400">Blue = Positive Weight • Red = Negative Weight</span>
              </div>
              <p className="leading-relaxed">
                During each forward pass, inputs are transformed as <KaTeXRenderer math="Z^{[l]} = A^{[l-1]} W^{[l]} + b^{[l]}" inline={true} />, followed by activation <KaTeXRenderer math={ACTIVATIONS[activation].formula} inline={true} />. Backpropagation computes <KaTeXRenderer math="\frac{\partial L}{\partial W}" inline={true} /> to reshape the decision boundary.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
