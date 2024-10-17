import React, { useState } from 'react';
import ReactFlow, { Background, Controls, Node, Edge } from 'react-flow-renderer';

const FlowChart: React.FC = () => {
    const [inputCode, setInputCode] = useState<string>('');
    const [nodes, setNodes] = useState<Node[]>([]);
    const [edges, setEdges] = useState<Edge[]>([]);

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInputCode(e.target.value);
    };

    const handleGenerateFlow = () => {
        const newNodes = parsePythonCode(inputCode);
        const newEdges = generateEdges(newNodes);
        setNodes(newNodes);
        setEdges(newEdges);
    };

    const parsePythonCode = (code: string): Node[] => {
        const keywords = ['def', 'if', 'elif', 'else', 'while', 'for', 'continue', 'break', 'print', 'return'];
        const lines = code.split('\n');
        const nodes: Node[] = [];

        lines.forEach((line, index) => {
            const trimmedLine = line.trim();

            let label = '';
            let type = 'default';

            switch (true) {
                case keywords.some(kw => trimmedLine.startsWith(kw)): {
                    const keyword = keywords.find(kw => trimmedLine.startsWith(kw));
                    if (keyword === 'print') {
                        label = trimmedLine;
                        type = 'print';
                    } else if (keyword === 'return') {
                        label = trimmedLine;
                        type = 'return';
                    } else {
                        label = trimmedLine;
                        type = 'keyword';
                    }
                    break;
                }

                case /[a-zA-Z_]\w*\s*=\s*.+/.test(trimmedLine): {
                    label = `Assignment: ${trimmedLine}`;
                    type = 'assignment';
                    break;
                }

                default:
                    label = '';
                    break;
            }

            if (label) {
                nodes.push({
                    id: `node-${index}`,
                    position: { x: 0, y: index * 100 },
                    data: { label },
                    type,
                });
            }
        });

        return nodes;
    };

    const generateEdges = (nodes: Node[]): Edge[] => {
        const edges: Edge[] = [];

        nodes.forEach((node, index) => {
            // Если это не последний узел и он не является узлом с ключевым словом "return"
            if (index < nodes.length - 1 && node.type !== 'return') {
                edges.push({
                    id: `edge-${index}-${index + 1}`,
                    source: node.id,
                    target: nodes[index + 1].id,
                    type: 'default',
                });
            }
        });

        return edges;
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
            <button onClick={handleGenerateFlow}>Создать блок-схему</button>
            <div style={{ height: '400px', border: '1px solid #ddd', marginTop: '20px' }}>
                <ReactFlow nodes={nodes} edges={edges} style={{ width: '100%', height: '100%' }}>
                    <Background />
                    <Controls />
                </ReactFlow>
            </div>
        </div>
    );
};

export default FlowChart;
