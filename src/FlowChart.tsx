import React, { useState } from 'react';
import FlowChartCanvas from './FlowChartCanvas';

type NodeType = 'start' | 'end' | 'operation' | 'decision' | 'input' | 'output' | 'loop' | 'return';

interface FlowChartNode {
    id: string;
    type: NodeType;
    label: string;
    x: number;
    y: number;
    next?: string[];
}

interface FlowChartEdge {
    source: string;
    target: string;
}

interface ParsedGraph {
    nodes: FlowChartNode[];
    edges: FlowChartEdge[];
}

class FlowchartBuilder {
    private nodeIdCounter = 0;
    private nodes: FlowChartNode[] = [];
    private edges: FlowChartEdge[] = [];

    constructor(private code: string) {}

    public buildGraph(): ParsedGraph {
        const lines = this.code.split('\n').map(line => line.trim());
        let previousNode: FlowChartNode | null = null;

        lines.forEach(line => {
            if (!line) return;

            const node = this.createNodeFromLine(line);
            if (node) {
                this.nodes.push(node);

                if (previousNode) {
                    this.edges.push({ source: previousNode.id, target: node.id });
                }
                previousNode = node;
            }
        });

        return { nodes: this.nodes, edges: this.edges };
    }

    private createNodeFromLine(line: string): FlowChartNode | null {
        let type: NodeType = 'operation';
        let label = line;

        if (line.startsWith('def')) {
            type = 'start';
        } else if (line.startsWith('if') || line.startsWith('elif')) {
            type = 'decision';
        } else if (line.startsWith('else')) {
            type = 'decision';
        } else if (line.startsWith('for') || line.startsWith('while')) {
            type = 'loop';
        } else if (line.startsWith('print')) {
            type = 'output';
        } else if (line.startsWith('return')) {
            type = 'return';
        } else if (/[a-zA-Z_]\w*\s*=\s*.+/.test(line)) {
            type = 'operation';
        }

        return {
            id: `node-${this.nodeIdCounter++}`,
            type,
            label,
            x: 50,
            y: this.nodeIdCounter * 80,
        };
    }
}

const FlowChart: React.FC = () => {
    const [inputCode, setInputCode] = useState<string>('');
    const [parsedGraph, setParsedGraph] = useState<ParsedGraph>({ nodes: [], edges: [] });

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInputCode(e.target.value);
    };

    const handleGenerateGraph = () => {
        const builder = new FlowchartBuilder(inputCode);
        setParsedGraph(builder.buildGraph());
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
            <button onClick={handleGenerateGraph}>Создать блок-схему</button>
            <FlowChartCanvas parsedGraph={parsedGraph} />
        </div>
    );
};

export default FlowChart;
