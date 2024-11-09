import React, { useState } from 'react';
import FlowChartCanvas from './FlowChartCanvas';

const FlowChart: React.FC = () => {
    const [inputCode, setInputCode] = useState<string>('');

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInputCode(e.target.value);
    };

    return (
        <div>
            <textarea
                value={inputCode}
                onChange={handleInputChange}
                placeholder="Введите Python функцию"
                rows={10}
                style={{ width: '100%', marginBottom: '10px' }}
            />
            <FlowChartCanvas code={inputCode} />
        </div>
    );
};

export default FlowChart;
