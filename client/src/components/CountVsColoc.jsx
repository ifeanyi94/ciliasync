import React, { useState } from 'react';

export default function CountVsColoc() {
  const [activeTab, setActiveTab] = useState('cilia');

  return (
    <div className="w-full max-w-xl mx-auto bg-white rounded-xl shadow-lg border border-blue-100 p-6">
      {/* Tabs */}
      <div className="flex justify-center space-x-4 mb-6">
        <button
          onClick={() => setActiveTab('cilia')}
          className={`px-5 py-2 rounded-full font-semibold transition-all duration-300 focus:outline-none ${
            activeTab === 'cilia'
              ? "text-white bg-gradient-to-r from-sky-500 via-blue-500 to-indigo-500 hover:from-sky-600 hover:to-indigo-600 px-5 py-2 rounded-full shadow-md"
              : 'bg-sky-100 text-sky-800 hover:bg-sky-200'
          }`}
        >
          🧫 Cilia Count
        </button>
        <button
          onClick={() => setActiveTab('coloc')}
          className={`px-5 py-2 rounded-full font-semibold transition-all duration-300 focus:outline-none ${
            activeTab === 'coloc'
              ? "text-white bg-gradient-to-r from-sky-500 via-blue-500 to-indigo-500 hover:from-sky-600 hover:to-indigo-600 px-5 py-2 rounded-full shadow-md"
              : 'bg-sky-100 text-sky-800 hover:bg-sky-200'
          }`}
        >
          🔬 Co-localization
        </button>
      </div>

      {/* Content */}
      <div className="bg-sky-50 p-6 rounded-lg shadow-inner">
        {activeTab === 'cilia' ? (
          <div>
            <h2 className="text-xl font-bold text-sky-700 mb-2">Cilia Count Results</h2>
            <p className="text-gray-600 text-sm">
              This will show count stats, bounding boxes, and processed cilia detection images.
            </p>
          </div>
        ) : (
          <div>
            <h2 className="text-xl font-bold text-sky-700 mb-2">Co-localization Results</h2>
            <p className="text-gray-600 text-sm">
              This will show overlap percentages, colocalization metrics, and channel-based analysis.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
