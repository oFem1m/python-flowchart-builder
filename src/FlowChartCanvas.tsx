import React, { useEffect, useRef, useState } from 'react';

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

const FlowChartCanvas: React.FC<{ code: string }> = ({ code }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [parsedGraph, setParsedGraph] = useState<ParsedGraph>({ nodes: [], edges: [] });

    useEffect(() => {
        const graph = parsePythonCodeToGraph(code);
        setParsedGraph(graph);
        drawFlowChart(graph);
    }, [code]);

    const parsePythonCodeToGraph = (code: string): ParsedGraph => {
        const lines = code.split('\n');
        const nodes: FlowChartNode[] = [];
        const edges: FlowChartEdge[] = [];
        let y = 50;
        let nodeId = 0;

        lines.forEach((line) => {
            const trimmedLine = line.trim();
            if (!trimmedLine) return;

            let label = trimmedLine;
            let type: NodeType = 'operation';

            if (trimmedLine.startsWith('def')) {
                type = 'start';
            } else if (trimmedLine.startsWith('if') || trimmedLine.startsWith('elif')) {
                type = 'decision';
            } else if (trimmedLine.startsWith('else')) {
                type = 'decision';
            } else if (trimmedLine.startsWith('for') || trimmedLine.startsWith('while')) {
                type = 'loop';
            } else if (trimmedLine.startsWith('print')) {
                type = 'output';
            } else if (trimmedLine.startsWith('return')) {
                type = 'return';
            } else if (/[a-zA-Z_]\w*\s*=\s*.+/.test(trimmedLine)) {
                type = 'operation';
            }

            const node = {
                id: `node-${nodeId}`,
                type,
                label,
                x: 50,
                y: y,
            };
            nodes.push(node);

            if (nodes.length > 1) {
                edges.push({
                    source: nodes[nodes.length - 2].id,
                    target: node.id,
                });
            }

            y += 80;
            nodeId += 1;
        });

        return { nodes, edges };
    };

    const drawFlowChart = (graph: ParsedGraph) => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        graph.nodes.forEach((node) => {
            drawNode(ctx, node);
        });

        graph.edges.forEach((edge) => {
            const sourceNode = graph.nodes.find((n) => n.id === edge.source);
            const targetNode = graph.nodes.find((n) => n.id === edge.target);
            if (sourceNode && targetNode) {
                drawEdge(ctx, sourceNode, targetNode);
            }
        });
    };

    const drawNode = (ctx: CanvasRenderingContext2D, node: FlowChartNode) => {
        ctx.beginPath();
        ctx.rect(node.x, node.y, 120, 40);
        ctx.fillStyle = '#ADD8E6';
        ctx.fill();
        ctx.strokeStyle = '#000';
        ctx.stroke();

        ctx.fillStyle = '#000';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(node.label, node.x + 60, node.y + 25);
    };

    const drawEdge = (ctx: CanvasRenderingContext2D, source: FlowChartNode, target: FlowChartNode) => {
        ctx.beginPath();
        ctx.moveTo(source.x + 60, source.y + 40);
        ctx.lineTo(target.x + 60, target.y);
        ctx.strokeStyle = '#000';
        ctx.stroke();
    };

    return (
        <canvas ref={canvasRef} width={800} height={600} style={{ border: '1px solid black' }} />
    );
};

export default FlowChartCanvas;
