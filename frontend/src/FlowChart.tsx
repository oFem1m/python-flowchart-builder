import {useRef, useEffect} from 'react';
import {Text, configureTextBuilder, BatchedText} from 'troika-three-text'
import * as THREE from 'three';
import {
    Box3,
    Color,
    Mesh,
    Vector3,
    Group,
    CubicBezierCurve3,
    Object3DEventMap,
    Line,
    BufferGeometry,
    LineBasicMaterial
} from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';

interface FlowChartProps {
    parsedData: any;
}

const skipType = ["if", "while", "for", "continue", "break", "else", "else-loop"];
const skipOutput = ["continue", "break", "else", "else-loop"];
const nullType = ["null_else", "null"]
const a = 40;
const _vec3 = new Vector3()
const _box = new Box3()

enum perimLine {
    S = 0,
    RNL = 1,
    LSR = 2,
    RSL = 3,
    LNR = 4,
    LS = 5,
    RS = 6
}

interface BlockNodeEventMap extends Object3DEventMap {
    change: CustomEvent<BlockNode>;
}

interface Node {
    type: string;
    label: string;
    text_mesh?: Text;
    width?: number;
    height?: number;
    parent?: Node;
    next?: Node;
    blockNode?: BlockNode;
    children: Node[];
}

class BlockNode extends Group {
    isBlockNode: boolean = true;
    text_mesh: Text | undefined;
    nodeType: string | undefined;
    input!: Vector3;
    output!: Vector3;
    ai: number = 5;
    ao: number = 5;
    rect: THREE.Object3D | undefined;
    lines !: { arg0: BlockNode, arg1: CubicBezierCurve3, is_input: boolean, line: Line }[];

    constructor(node: Node, input: Vector3, output: Vector3, visible: boolean) {
        super();
        if (!node.text_mesh) return;
        const bbox = node.text_mesh.geometry.boundingBox;
        if (bbox) {
            if (visible) {

                const rect1 = generateShapeMesh(bbox.clone(), 2, new Color(0xf0f0f0), node.type)
                rect1.position.add(node.text_mesh.position).add(_vec3.set(0, 0, -1))
                const rect2 = generateShapeMesh(bbox.clone(), 0, new Color(0x555555), node.type)
                rect2.position.add(node.text_mesh.position)

                this.rect = rect1;
                this.add(rect1);
                this.add(rect2);
                if (node.type == "call") {
                    _box.copy(bbox);
                    _box.expandByVector(_vec3.set(4, 0, 0).clone());
                    const _rect1 = generateShapeMesh(_box.clone(), 2, new Color(0xf0f0f0), node.type)
                    _rect1.position.add(node.text_mesh.position).add(_vec3.set(0, 0, -3))
                    const _rect2 = generateShapeMesh(_box.clone(), 0, new Color(0x555555), node.type)
                    _rect2.position.add(node.text_mesh.position).add(_vec3.set(0, 0, -2))
                    this.add(_rect1);
                    this.add(_rect2);
                }
                this.add(node.text_mesh);

            } else {
                node.text_mesh.visible = false;
            }
            this.nodeType = node.type;
            this.input = new Vector3();
            this.output = new Vector3();
            this.text_mesh = node.text_mesh;
            this.input.copy(input);
            this.output.copy(output);
            this.lines = [];
        }
    }

    addNode(node: BlockNode, box: Box3, perimType: perimLine, scene: THREE.Scene, baseColor: number = 0x000000) {
        const output = new Vector3(this.output.x, 0, this.output.z);
        const points = []
        const curve = new CubicBezierCurve3();
        const _baseColor = 0x000000;
        const randomColor = new Color(baseColor);
        if (baseColor == 0x000000) {
            randomColor.r = (Math.random());
            randomColor.g = (Math.random());
            if (randomColor.b < 0.1) randomColor.b = 1 - randomColor.b
            randomColor.b = (Math.random());
        }
        const size = 1 + Math.random() * 0.5 - 0.05
        switch (perimType) {
            case perimLine.S:
                if (box.min.y != Infinity) {
                    output.add(_vec3.set(0, box.min.y, 0));
                } else {
                    output.add(_vec3.set(0, this.output.y, 0));
                }
                points.push(this.output.clone());
                points.push(output.clone());
                points.push(_vec3.set(output.x, (output.y + node.input.y) / 2, 0).clone());
                points.push(_vec3.set(node.input.x, (output.y + node.input.y) / 2, 0).clone());
                points.push(node.input.clone());
                //curve.copy(new CubicBezierCurve3(output, output.clone().add(_vec3.set(0, -this.ao, 0)), node.input.clone().add(_vec3.set(0, node.ai, 0)), node.input))
                break;
            case perimLine.RS:
                randomColor.set(1, 0, 0)
                if (box.min.y != Infinity) {
                    output.set(box.max.x + this.ao, this.output.y, 0);
                } else {
                    output.add(_vec3.set(0, this.output.y, 0));
                }
                points.push(this.output.clone());
                points.push(output.clone());
                points.push(_vec3.set(output.x, (output.y + node.input.y) / 2, 0).clone());
                points.push(_vec3.set(node.input.x, (output.y + node.input.y) / 2, 0).clone());
                points.push(node.input.clone());
                //curve.copy(new CubicBezierCurve3(output, output.clone().add(_vec3.set(0, -this.ao, 0)), node.input.clone().add(_vec3.set(0, node.ai, 0)), node.input))
                break;
            case perimLine.LS:
                randomColor.set(0, 1, 0)
                if (box.min.y != Infinity) {
                    output.set(box.min.x - this.ai, this.output.y, 0);
                } else {
                    output.add(_vec3.set(0, this.output.y, 0));
                }
                points.push(this.input.clone());
                points.push(output.clone());
                points.push(_vec3.set(output.x, (output.y + node.input.y) / 2, 0).clone());
                points.push(_vec3.set(node.input.x, (output.y + node.input.y) / 2, 0).clone());
                points.push(node.input.clone());
                //curve.copy(new CubicBezierCurve3(output, output.clone().add(_vec3.set(0, -this.ao, 0)), node.input.clone().add(_vec3.set(0, node.ai, 0)), node.input))
                break;
            case perimLine.LNR:
                if (box.min.y != Infinity) {
                    output.set(box.min.x - this.ao, node.input.y, 0);
                } else {
                    output.add(_vec3.set(0, this.output.y, 0));
                }
                points.push(this.output.clone(),
                    _vec3.set(this.output.x, box.min.y - this.ao * 2 * size, 0).clone(),
                    _vec3.set(box.min.x - this.ao * 2 * size, box.min.y - this.ao * 2 * size, 0).clone(),
                    _vec3.set(box.min.x - this.ao * 2 * size, node.input.y, 0).clone(),
                );
                points.push(output.clone());
                //points.push(_vec3.set(output.x, (output.y+node.input.y)/2, 0).clone());
                //points.push(_vec3.set(node.input.x, (output.y+node.input.y)/2, 0).clone());
                points.push(node.input.clone());
                //curve.copy(new CubicBezierCurve3(output, output.clone().add(_vec3.set(+this.ao, 0, 0)), node.input.clone().add(_vec3.set(0, node.ai, 0)), node.input))
                //points.push(...curve.getPoints(50));
                break;
            case perimLine.RSL:
                if (box.min.y != Infinity) {
                    output.set(Math.max(this.output.x, node.input.x), box.min.y - this.ao + size, 0);
                } else {
                    output.add(_vec3.set(0, this.output.y, 0));
                }
                points.push(this.output.clone(),
                    _vec3.set(this.output.x, this.output.y - this.ao + size, 0).clone(),
                    _vec3.set(box.max.x + this.ao, this.output.y - this.ao + size, 0).clone(),
                    _vec3.set(box.max.x + this.ao, box.min.y - this.ao, 0).clone(),
                );
                points.push(output.clone());
                points.push(_vec3.set(output.x, (output.y + node.input.y) / 2, 0).clone());
                points.push(_vec3.set(node.input.x, (output.y + node.input.y) / 2, 0).clone());
                points.push(node.input.clone());
                break;
        }

        // Создайте линию
        const geometry = new BufferGeometry().setFromPoints(points);

        const material = new LineBasicMaterial({color: randomColor});
        const line = new Line(geometry, material);
        line.position.add(_vec3.set(0, 0, -3).clone())
        scene.add(line);

        this.lines.push({arg0: node, arg1: curve, is_input: true, line});
        node.lines.push({arg0: this, arg1: curve, is_input: false, line});
    }

    addNodeloop(node: BlockNode, box1: Box3, box2: Box3, _size: number, perimType: perimLine, scene: THREE.Scene) {
        const output = new Vector3(this.output.x, 0, this.output.z);
        const points = []
        const curve = new CubicBezierCurve3();
        const curve2 = new CubicBezierCurve3();
        const size = _size + Math.random() * 0.1 - 0.05
        points.push(this.output.clone(),
            _vec3.set(box1.max.x + this.ao, this.output.y, 0).clone(),
            _vec3.set(box1.max.x + this.ao, box1.min.y - this.ao * size, 0).clone(),
            _vec3.set(this.output.x, box1.min.y - this.ao * size, 0).clone(),
        );
        switch (perimType) {
            case perimLine.S:
                if (box2.min.y != Infinity) {
                    output.add(_vec3.set(0, box2.min.y - this.ao * size, 0));
                } else {
                    output.add(_vec3.set(0, this.output.y, 0));
                }
                //points.push(this.output.clone());
                points.push(output.clone());
                points.push(_vec3.set(output.x, (output.y + node.input.y) / 2, 0).clone());
                points.push(_vec3.set(node.input.x, (output.y + node.input.y) / 2, 0).clone());
                points.push(node.input.clone());
                //curve.copy(new CubicBezierCurve3(output, output.clone().add(_vec3.set(0, -this.ao, 0)), node.input.clone().add(_vec3.set(0, node.ai, 0)), node.input))
                break;
            case perimLine.LNR:
                if (box2.min.y != Infinity) {
                    output.set(box2.min.x - this.ao, node.input.y, 0);
                } else {
                    output.add(_vec3.set(0, this.output.y, 0));
                }
                points.push(
                    _vec3.set(this.output.x, box2.min.y - this.ao * 2 * size, 0).clone(),
                    _vec3.set(box2.min.x - this.ao * 2 * size, box2.min.y - this.ao * 2 * size, 0).clone(),
                    _vec3.set(box2.min.x - this.ao * 2 * size, node.input.y, 0).clone(),
                );
                points.push(output.clone());
                //points.push(_vec3.set(output.x, (output.y+node.input.y)/2, 0).clone());
                //points.push(_vec3.set(node.input.x, (output.y+node.input.y)/2, 0).clone());
                points.push(node.input.clone());
                //curve.copy(new CubicBezierCurve3(output, output.clone().add(_vec3.set(+this.ao, 0, 0)), node.input.clone().add(_vec3.set(0, node.ai, 0)), node.input))
                //points.push(...curve.getPoints(50));
                break;
        }


        // Создайте линию
        const geometry = new BufferGeometry().setFromPoints(points);
        const baseColor = 0xff0000;
        const randomColor = new Color(baseColor);
        randomColor.r = (Math.random());
        randomColor.g = (Math.random());
        randomColor.b = (Math.random());
        const material = new LineBasicMaterial({color: randomColor});
        const line = new Line(geometry, material);
        line.position.add(_vec3.set(0, 0, -3).clone())
        scene.add(line);

        this.lines.push({arg0: node, arg1: curve, is_input: true, line});
        node.lines.push({arg0: this, arg1: curve, is_input: false, line});

    }

    updateLines() {
        this.lines.forEach((line) => {
            if (line.is_input) {
                line.arg1.v0.copy(this.output);
                line.arg1.v1.copy(this.output.clone().add(_vec3.set(0, -this.ao, 0)));
            } else {
                line.arg1.v2.copy(this.input);
                line.arg1.v3.copy(this.input.clone().add(_vec3.set(0, -this.ao, 0)));
            }
            line.arg1.updateArcLengths();
        });
    }

    inputClone(node: BlockNode) {
        this.input = node.input.clone();
        this.output = node.input.clone();
        this.ao = 0;
        node.ai = 0;
    }

    outputClone(node: BlockNode) {
        this.input = node.output.clone();
        this.output = node.output.clone();
        this.ai = 0;
        node.ao = 0;
    }
}

function addText_mesh(obj: Node, batch: BatchedText) {
    if (obj === null || obj === undefined) {
        return;
    }
    obj.text_mesh = new Text();
    obj.text_mesh.text = obj.label;
    obj.text_mesh.fontSize = 10;
    obj.text_mesh.color = 0xffffff;
    batch.add(obj.text_mesh);
    //obj.text_mesh.position.add(_vec3.set(0,0,2))
    if (Array.isArray(obj.children)) {
        for (const child of obj.children) {
            child.parent = obj;
            addText_mesh(child, batch);
        }
    }
}

function addSize(obj: Node) {
    if (obj === null || obj === undefined) {
        return;
    }


    const bbox = new Box3();

    obj.width = 0;
    obj.height = 0;
    let is_skip = false;
    if (!skipType.includes(obj.type)) is_skip = true;

    if (obj.text_mesh?.geometry.boundingBox) bbox.copy(obj.text_mesh?.geometry.boundingBox);
    if (bbox && bbox.min.x != Infinity && is_skip) {
        _box.setFromObject(generateShapeMesh(bbox.clone(),2,new Color(),obj.type));
        obj.width = (_box.max.x - _box.min.x)
        obj.height = (_box.max.y - _box.min.y)
    }

    if (Array.isArray(obj.children)) {
        if (obj.children.length == 0) {
            return;
        }
        for (const child of obj.children) {
            addSize(child);
        }
        let width = 0;
        let height = 0;

        switch (obj.type) {
            case "loop":
            case "branch":

                for (const child of obj.children) {
                    if (child.width) {
                        width += child.width;
                    }
                    if (child.height) {
                        height = Math.max(child.height, height);
                    }
                }

                if (obj.width || obj.width === 0) {
                    obj.width = Math.max(width, obj.width)
                }
                if (obj.height || obj.width === 0) {
                    obj.height += height + a
                }
                break;
            default:
                for (const child of obj.children) {
                    if (child.height) {
                        height += child.height + a;
                    }
                    if (child.width) {
                        width = Math.max(child.width, width);
                    }
                }

                if (obj.width || obj.width === 0) {
                    obj.width = Math.max(width, obj.width)
                }
                if (obj.height || obj.height === 0) {
                    obj.height += height
                }

                break;
        }

    }
    obj.width = obj.width * 1.01
    obj.height = obj.height * 1.01

}

function textMove(obj: Node, x: number, y: number) {
    if (obj === null || obj === undefined) {
        return;
    }
    obj.text_mesh?.position.add(_vec3.set(x, y, 0));

    const bbox = obj.text_mesh?.geometry.boundingBox;
    let width, height;
    if (bbox) {
        width = bbox.max.x - bbox.min.x
    }
    if (bbox) {
        height = bbox.max.y - bbox.min.y
    }
    if (Array.isArray(obj.children)) {
        if (obj.children.length == 0) {
            return;
        }
        let dy = 0;
        let dx = 0;

        switch (obj.type) {
            case "loop":
            case "branch":
                if (height) dy += a + height;
                if (width && obj.children.length == 2 && obj.children[1].width) dx = -(obj.children[1].width) / 2
                else dx = 0
                for (const child of obj.children) {
                    textMove(child, x + dx, y - dy)
                    if (child.width && obj.children.length == 2 && obj.children[1].width) dx += child.width + (obj.children[1].width) / 2;
                    else if (child.width) dx += child.width + a;

                }
                break;
            default:
                if (!skipType.includes(obj.type)) dy += a + height;
                for (const child of obj.children) {
                    textMove(child, x, y - dy)
                    if (child.height) dy += a + child.height;
                }
                break;
        }
    }

}

function generateShapeMesh(box: Box3, side: number, color: Color, type: string) {
    const x = box.min.x - side;
    const y = box.min.y - side;
    const _x = box.min.x;
    const _y = box.min.y;
    const width = box.max.x - box.min.x + 2 * side;
    const height = box.max.y - box.min.y + 2 * side;
    const _width = box.max.x - box.min.x;
    const _height = box.max.y - box.min.y;
    let shape;
    switch (type) {
        case 'return':
        case 'function':
            shape = new THREE.Shape();
            shape.ellipse(x + width / 2, y + height / 2, width, height, 0, 2 * Math.PI, false, 0);
            break;
        case 'branch':
            shape = new THREE.Shape();
            shape.moveTo(_x - _width / 2 - side, _y + _height / 2);
            shape.lineTo(_x + _width / 2, _y - _height / 2 - side);
            shape.lineTo(_x + _width + _width / 2 + side, _y + _height / 2);
            shape.lineTo(_x + _width / 2, _y + _height + _height / 2 + side);
            shape.lineTo(_x - _width / 2 - side, _y + _height / 2);
            break;

        case 'loop':
            shape = new THREE.Shape();
            shape.moveTo(x, y);
            shape.lineTo(x + width, y);
            shape.lineTo(x + width + height / 2, y + height / 2);
            shape.lineTo(x + width, y + height);
            shape.lineTo(x, y + height);
            shape.lineTo(x - height / 2, y + height / 2);
            shape.lineTo(x, y);
            break;
        case 'rectangle':
        default:
            shape = new THREE.Shape();
            shape.moveTo(x, y);
            shape.lineTo(x + width, y);
            shape.lineTo(x + width, y + height);
            shape.lineTo(x, y + height);
            shape.lineTo(x, y);
            break;
    }

    const geometry = new THREE.ShapeGeometry(shape);
    const material = new THREE.MeshBasicMaterial({color: color});
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.add(_vec3.set(0, 0, -0.1).clone())
    return mesh;
}

function addBox(obj: Node, bantbatch: BatchedText) {
    if (obj === null || obj === undefined) {
        return;
    }
    if (obj.text_mesh && obj.text_mesh.geometry.boundingBox) {
        const bbox = obj.text_mesh.geometry.boundingBox;
        const rect1 = generateShapeMesh(bbox.clone(), 2, new Color(0xf0f0f0), obj.type)
        rect1.position.add(obj.text_mesh.position).add(_vec3.set(0, 0, 1))
        const rect2 = generateShapeMesh(bbox.clone(), 0, new Color(0x555555), obj.type)
        rect2.position.add(obj.text_mesh.position).add(_vec3.set(0, 0, 0.5))
        bantbatch.add(rect1);
        bantbatch.add(rect2);
    }
    if (Array.isArray(obj.children)) {
        for (const child of obj.children) {
            addBox(child, bantbatch);
        }
    }
}

function toBlockNode(obj: Node, prev: Node | undefined, next: Node | undefined, scene: THREE.Scene) {
    if (obj === null || obj === undefined) {
        return;
    }
    if (next !== undefined){
        obj.next = next;
    }
    const firstNode = obj;
    if (prev !== undefined && prev.blockNode && obj.blockNode && obj.parent && obj.text_mesh?.geometry.boundingBox !== undefined
        && obj.text_mesh?.geometry.boundingBox?.min !== undefined
        && obj.text_mesh?.geometry.boundingBox?.max !== undefined) {

        const bbox = new Box3();
        switch (prev.type) {
            case "loop":
                if (prev != obj.parent) {
                    bbox.setFromObject(prev.blockNode);
                    // prev.blockNode.addNode(obj.blockNode, bbox, perimLine.RSL, scene);
                } else {
                    prev.blockNode.addNode(obj.blockNode, bbox, perimLine.S, scene);
                }
                break;
            case "return":
                break
            case "break":
                break
            case "continue":
                break
            case "branch":
                if (prev?.blockNode != undefined && prev.blockNode.rect) bbox.setFromObject(prev.blockNode.rect);
                if (obj.type == "null_else") prev.blockNode.addNode(obj.blockNode, bbox, perimLine.RS, scene);
                else prev.blockNode.addNode(obj.blockNode, bbox, perimLine.S, scene, 0x00ff00);
                break;
            // case "if":
            //   if (prev.parent?.blockNode !=undefined  && prev.parent.blockNode.rect) bbox.setFromObject(prev.parent.blockNode.rect);
            //   prev.blockNode.addNode(obj.blockNode, bbox, perimLine.LS, scene);
            //   break;
            case "else-loop":
            case "else":
                if (prev.parent?.blockNode != undefined && prev.parent.blockNode.rect) bbox.setFromObject(prev.parent.blockNode.rect);
                prev.blockNode.addNode(obj.blockNode, bbox, perimLine.RS, scene);
                break;

            default:
                prev.blockNode.addNode(obj.blockNode, _box.makeEmpty(), perimLine.S, scene);
                break;
        }

    }
    let parent = obj.parent;
    const box = new Box3();
    let is_skip_loop = false
    switch (obj.type) {

        case "continue":

            let boxParent = obj;

            while (parent?.parent && parent.type != "while" && parent.type != "for") {
                boxParent = parent;
                parent = parent.parent;

            }
            parent = parent.parent;
            if (parent == undefined || !parent.blockNode || !boxParent?.blockNode) {
                console.log("continue error")
                return
            }

            _box.setFromObject(boxParent.blockNode);
            if (parent.blockNode) box.setFromObject(parent.blockNode);
            box.min.y = _box.min.y
            obj.blockNode?.addNode(parent.blockNode, box, perimLine.LNR, scene);
            break;
        case "break":
            let _boxParent = obj;
            while (parent?.parent && parent.type != "while" && parent.type != "for") {
                _boxParent = parent;
                parent = parent.parent;
            }
            if (parent?.parent) parent = parent.parent;
            if (parent == undefined || !parent.blockNode || parent.next == undefined || !_boxParent?.blockNode || !parent.next?.blockNode) {
                console.log("continue error")
                return
            }
            _box.setFromObject(_boxParent.blockNode);
            if (parent.blockNode) box.setFromObject(parent.blockNode);
            box.min.y = _box.min.y
            obj.blockNode?.addNode(parent.next?.blockNode, box, perimLine.S, scene);
            break;
        case "return":
            break;
        case "while":
            break;
        case "for":
            break;
        case "loop":
            let size = 0;
            if (parent == undefined || !parent.blockNode || next == undefined || !next.blockNode || next.parent == obj.parent) {
                break;
            }
            is_skip_loop = false
            while (parent?.parent && parent.parent != next.parent && (parent.type != "loop" || is_skip_loop)) {
                if (parent.type == "else-loop") is_skip_loop = true
                if (parent.type == "loop") is_skip_loop = false;
                size += 1;
                parent = parent.parent;

            }
            if (parent == undefined || obj == undefined || !obj.blockNode || !parent.blockNode || next == undefined || !next.blockNode || next.parent == obj.parent) {
                console.log("default error")
                break;
            }
            if (parent.blockNode) box.setFromObject(parent.blockNode);
            _box.setFromObject(obj.blockNode);
            if (parent.type != "loop") obj.blockNode?.addNodeloop(next.blockNode, _box, box, size, perimLine.S, scene);
            else obj.blockNode?.addNodeloop(parent.blockNode, _box, box, size, perimLine.LNR, scene);
            break;
        default:
            if (parent == undefined || !parent.blockNode || next == undefined || !next.blockNode || next.parent == obj.parent || obj.children.length !== 0) {
                break;
            }

            is_skip_loop = (parent.type == "else-loop")
            while (parent?.parent && parent.parent != next.parent && (parent.type != "loop" || is_skip_loop)) {
                if (parent.type == "else-loop") is_skip_loop = true
                if (parent.type == "loop") is_skip_loop = false;
                parent = parent.parent;
                ;
            }
            if (parent == undefined || !parent.blockNode || next == undefined || !next.blockNode || next.parent == obj.parent || obj.children.length !== 0) {
                console.log("default error")
                break;
            }
            if (parent.blockNode) box.setFromObject(parent.blockNode);
            if (obj.type != "null_else") {
                if (parent.type != "loop" || is_skip_loop) obj.blockNode?.addNode(next.blockNode, box, perimLine.S, scene);
                else obj.blockNode?.addNode(parent.blockNode, box, perimLine.LNR, scene);
            } else {
                if (parent.type != "loop" || is_skip_loop) obj.blockNode?.addNode(next.blockNode, box, perimLine.S, scene, 0xff0000);
                else obj.blockNode?.addNode(parent.blockNode, box, perimLine.LNR, scene, 0xff0000);
            }

            break;
    }


    switch (obj.type) {
        case "loop":
        case "branch":
            if (Array.isArray(obj.children)) {
                for (const child of obj.children) {
                    toBlockNode(child, obj, next, scene);
                }
            }
            break;
        default:
            if (Array.isArray(obj.children)) {
                let _prev: Node | undefined = firstNode;
                for (let i = 0; i < obj.children.length - 1; i++) {
                    const child = obj.children[i];
                    const _next = obj.children[i + 1];
                    if (_prev && (_prev?.type != "branch")) _prev = toBlockNode(child, _prev, _next, scene);
                    else _prev = toBlockNode(child, undefined, _next, scene);
                }
                if (obj.children.length >= 1) {
                    const child = obj.children[obj.children.length - 1];
                    if (_prev && (_prev?.type != "branch")) _prev = toBlockNode(child, _prev, next, scene);
                    else _prev = toBlockNode(child, undefined, next, scene);
                    //toBlockNode(child,_prev, next, scene);
                }
            }
            break;
    }
    return firstNode;
}

function setBlockNode(obj: Node) {
    if (obj === null || obj === undefined) {
        return;
    }


    if (obj.text_mesh?.geometry.boundingBox === undefined
        || obj.text_mesh?.geometry.boundingBox?.min === undefined
        || obj.text_mesh?.geometry.boundingBox?.max === undefined) return
    const position = obj.text_mesh?.position;
    const bbox = obj.text_mesh?.geometry.boundingBox?.clone();
    const input = _vec3.addVectors(bbox?.min, bbox?.max).clone().multiplyScalar(0.5);
    input.set(input.x, bbox?.max.y + 2, input.z).add(position)
    const output = _vec3.addVectors(bbox?.min, bbox?.max).clone().multiplyScalar(0.5);
    output.set(output.x, bbox?.min.y - 2, output.z).add(position)

    const center = _vec3.addVectors(bbox?.min, bbox?.max).clone().multiplyScalar(0.5)
    center.add(position);

    if (skipType.includes(obj.type) || nullType.includes(obj.type)) obj.blockNode = new BlockNode(obj, center, center, false);
    else obj.blockNode = new BlockNode(obj, center, center, true);


    if (Array.isArray(obj.children)) {
        for (let i = 0; i < obj.children.length; i++) {
            const child = obj.children[i];
            setBlockNode(child);
            if (child.blockNode) {
                obj.blockNode.add(child.blockNode)
            }
        }
    }


}

function senSkipNode(obj: Node, prev: Node | undefined,) {
    if (obj === null || obj === undefined) {
        return;
    }

    if (skipType.includes(obj.type)
        && !skipOutput.includes(obj.type)
        && obj.blockNode !== undefined) obj.blockNode.inputClone(obj.children[0].blockNode);
    if (skipOutput.includes(obj.type) && obj.blockNode !== undefined) obj.blockNode.outputClone(prev.blockNode);

    switch (obj.type) {
        case "loop":
        case "branch":
            if (Array.isArray(obj.children)) {
                for (const child of obj.children) {
                    senSkipNode(child, obj);
                }
            }
            break;
        default:
            if (Array.isArray(obj.children)) {
                for (let i = 1; i < obj.children.length; i++) {
                    const child = obj.children[i];
                    const _prev = obj.children[i - 1];
                    senSkipNode(child, _prev)
                }
                if (obj.children.length >= 1) {
                    const child = obj.children[0];
                    senSkipNode(child, prev);
                    //toBlockNode(child,_prev, next, scene);
                }
            }
            return
            break;
    }


}

function FlowChart({parsedData}: FlowChartProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const sceneRef = useRef<THREE.Scene | null>(null);
    const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
    const controlsRef = useRef<OrbitControls | null>(null);

    useEffect(() => {
        if (!parsedData) return; // Не перерисовываем, если данных нет

        // Инициализация сцены и рендерера
        const initScene = () => {
            const q = 1;
            const camera = new THREE.OrthographicCamera(
                window.innerWidth / -2 * q,  // левый край камеры
                window.innerWidth / 2 * q,   // правый край камеры
                window.innerHeight / 2 * q,  // верхний край камеры
                window.innerHeight / -2 * q, // нижний край камеры
            );
            camera.position.z = 100;
            const scene = new THREE.Scene();
            scene.background = new Color(0x444444);

            const renderer = new THREE.WebGLRenderer({antialias: true, canvas: canvasRef.current!});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(window.devicePixelRatio);

            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableZoom = true;
            controls.rotateSpeed = 0;

            sceneRef.current = scene;
            rendererRef.current = renderer;
            controlsRef.current = controls;

            return {camera, scene, renderer};
        };

        // Очистка предыдущей сцены перед отрисовкой новой
        const clearScene = () => {
            if (sceneRef.current) {
                while (sceneRef.current.children.length > 0) {
                    sceneRef.current.remove(sceneRef.current.children[0]);
                }
            }
        };

        const renderFlowChart = (data: any) => {
            const {scene, renderer, camera} = initScene();
            const bantch = new BatchedText();

            configureTextBuilder({useWorker: false});

            addText_mesh(data, bantch);
            bantch.sync(() => {
                addSize(data);
                textMove(data, -100, 100);
                addBox(data, bantch);
                setBlockNode(data);
                senSkipNode(data);
                if (data.blockNode) scene.add(data.blockNode);

                toBlockNode(data, undefined, undefined, scene);

                const animate = () => {
                    requestAnimationFrame(animate);
                    controlsRef.current?.update();
                    renderer.render(scene, camera);
                };
                animate();
            });
        };

        clearScene();
        renderFlowChart(parsedData);
    }, [parsedData]); // Запускаем эффект при изменении parsedData

    return (
        <div style={{width: '100%', height: '100%', overflow: 'hidden'}}>
            <canvas
                ref={canvasRef}
                style={{
                    width: '100%',
                    height: '100%',
                    display: 'block',
                    backgroundColor: '#444444',
                }}
            />
        </div>
    )
}

export default FlowChart;

function rectangleShape(arg0: number, arg1: number, arg2: number, arg3: number) {
    throw new Error('Function not implemented.');
}

