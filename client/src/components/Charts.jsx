// C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\client\src\components\Charts.jsx

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, Legend, ScatterChart, Scatter, CartesianGrid } from 'recharts';

// Chart 1: Cilia Count Per Condition
export function CiliaCountChart({ data }) {
  return (
    <div className="w-full h-64">
      <ResponsiveContainer>
        <BarChart data={data}>
          <XAxis dataKey="condition" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="cilia_count" fill="#4f46e5" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

// Chart 2: Membrane vs Cytoplasm Colocalization
export function ColocalizationLineChart({ data }) {
  return (
    <div className="w-full h-64">
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="membrane_coloc" stroke="#10b981" />
          <Line type="monotone" dataKey="cytoplasm_coloc" stroke="#ef4444" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

// Chart 3: Scatterplot — Coloc % vs Another Variable
export function ColocScatterPlot({ data }) {
  return (
    <div className="w-full h-64">
      <ResponsiveContainer>
        <ScatterChart>
          <CartesianGrid />
          <XAxis type="number" dataKey="cilia_count" name="Cilia Count" />
          <YAxis type="number" dataKey="coloc_percent" name="Colocalization %" />
          <Tooltip />
          <Scatter name="Samples" data={data} fill="#6366f1" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
