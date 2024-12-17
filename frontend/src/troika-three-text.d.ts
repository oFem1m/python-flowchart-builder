declare module 'troika-three-text' {
    import {Mesh, ColorRepresentation} from 'three';

    export interface PreloadFontOptions {
        font?: string;
        characters?: string | string[];
        sdfGlyphSize?: number;
    }

    export function configureTextBuilder(config: Object): void;

    export function preloadFont(options: PreloadFontOptions, onComplete?: () => void): void;

    class Text extends Mesh {
        constructor();

        text: string;
        anchorX: number | string;
        anchorY: number | string;
        clipRect: [number, number, number, number];
        color: ColorRepresentation;
        curveRadius: number;
        depthOffset: number;
        direction: 'auto' | 'ltr' | 'rtl';
        fillOpacity: number;
        font: string;
        fontSize: number;
        fontStyle: 'normal' | 'italic';
        fontWeight: 'normal' | 'bold';
        glyphGeometryDetail: number;
        gpuAccelerateSDF: boolean;
        letterSpacing: number;
        lineHeight: number | 'normal';
        maxWidth: number;
        outlineBlur: number | string;
        outlineColor: ColorRepresentation;
        outlineOffsetX: number | string;
        outlineOffsetY: number | string;
        outlineOpacity: number;
        outlineWidth: number | string;
        overflowWrap: 'normal' | 'break-word';
        sdfGlyphSize: number;
        strokeColor: ColorRepresentation;
        strokeOpacity: number;
        strokeWidth: number | string;
        textAlign: 'left' | 'right' | 'center' | 'justify';
        textIndent: number;
        unicodeFontsUrl: string;
        whiteSpace: 'normal' | 'nowrap';
        textRenderInfo: object;

        sync(onSync?: () => void): void;

        getCaretAtPoint(textRenderInfo: object, x: number, y: number): {
            x: number;
            y: number;
            height: number;
            charIndex: number
        };

        getSelectionRects(textRenderInfo: object, start: number, end: number): {
            left: number;
            top: number;
            right: number;
            bottom: number
        }[];
    }


    declare class BatchedText extends Text {
        /**
         * @typedef {Object} PackingInfo
         * @property {number} index - the packing order index when last packed, or -1
         * @property {boolean} dirty - whether it has synced since last pack
         */

        /**
         * @type {Map<Text, PackingInfo>}
         */
        _members: Map<Text, PackingInfo>;

        /**
         * @type {Object}
         */
        _dataTextures: Object;

        /**
         * @param {Event} e
         */
        _onMemberSynced(e: Event): void;

        /**
         * @override
         * Batch any Text objects added as children
         */
        add(...objects: any[]): BatchedText;

        /**
         * @override
         */
        remove(...objects: any[]): BatchedText;

        /**
         * @param {Text} text
         */
        addText(text: Text): void;

        /**
         * @param {Text} text
         */
        removeText(text: Text): void;

        /**
         * Use the custom derivation with extra batching logic
         */
        createDerivedMaterial(baseMaterial: any): any;

        /**
         * @param {boolean} force
         */
        updateMatrixWorld(force: boolean): void;

        /**
         * Update the batched geometry bounds to hold all members
         */
        updateBounds(): void;

        /** @override */
        hasOutline(): boolean;

        /**
         * @override
         * Copy member matrices and uniform values into the data texture
         */
        _prepareForRender(material: any): void;

        /**
         * @param {Function} callback
         */
        sync(callback: Function): void;

        /**
         * @param {BatchedText} source
         */
        copy(source: BatchedText): BatchedText;

        dispose(): void;

        constructor(): BatchedText;
    }

    export {BatchedText, Text};

}
