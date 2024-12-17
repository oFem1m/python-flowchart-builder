import React, {useState} from 'react';
import FlowChart from './FlowChart';

const App: React.FC = () => {
    const [code, setCode] = useState(''); // Состояние для ввода кода
    const [parsedData, setParsedData] = useState(null); // Данные после парсинга

    // Функция для отправки кода на сервер и получения парсинга
    const handleDrawClick = async () => {
        try {
            const response = await fetch('http://localhost:8000/parse/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code}),
            });
            const data = await response.json();
            setParsedData(data);
        } catch (error) {
            console.error('Error parsing code:', error);
        }
    };

    return (
        <div style={{display: 'flex', height: '100vh'}}>
            {/* Левая колонка: поле ввода */}
            <div style={{flex: 1, padding: '20px', background: '#f4f4f4'}}>
                <h2>Введите код:</h2>
                <textarea
                    rows={20}
                    style={{width: '100%', resize: 'none'}}
                    placeholder="Введите Python код здесь..."
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                />
                <button onClick={handleDrawClick} style={{marginTop: '10px'}}>
                    Нарисовать
                </button>
            </div>

            {/* Правая колонка: canvas */}
            <div style={{flex: 3, background: '#ffffff', height: '100%', overflow: 'hidden'}}>
                <FlowChart parsedData={parsedData}/>
            </div>
        </div>
    );
};

export default App;
