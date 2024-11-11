import React from 'react';
import FlowChart from './FlowChart.tsx';

const App: React.FC = () => {
    return (
        <div style={{ padding: '20px' }}>
            <h1>Python Flowchart Builder</h1>
            <FlowChart />
        </div>
    );
};

export default App;
