
/**
 * @description 템플릿 정의
 */
const materialInputTemplate = document.createElement('template')
materialInputTemplate.innerHTML = `
    <style>
        input::-webkit-outer-spin-button,
        input::-webkit-inner-spin-button {
            /* display: none; <- Crashes Chrome on hover */
            -webkit-appearance: none;
            margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
        }

        input[type=number] {
            -moz-appearance:textfield; /* Firefox */
        }

        html {
            font-family: 'Roboto', sans-serif;
        }

        div {
            position: relative;
            padding: 15px 10px;
            margin-top: 10px;
            display: inline-block;
        }
        
    input {
            font-family: inherit;
            min-width: 3rem;
            border: 0;
            border-bottom: 1px solid #d2d2d2;
            outline: 0;
            font-size: 16px;
            color: whitesmoke;
            padding: 7px 0;
            background: transparent;
            transition: border-color 0.2s;
        }
        
        input::placeholder {
            color: transparent;
        }
        
        input:placeholder-shown ~ label {
            font-size: 16px;
            cursor: text;
            top: 20px;
        }
        
        label,
        input:focus ~ label {
            position: absolute;
            top: 0;
            display: block;
            transition: 0.2s;
            font-size: 12px;
            color: #whitegray;
        }
        
        input:focus ~ label {
            color: #009788;
        }
        
        input:focus {
            padding-bottom: 6px;
            border-bottom: 2px solid #009788;
        }
    </style>

<div>
    <input />
    <label></label>
</div>
`
class MaterialInput extends HTMLElement {
    constructor() {
        super();

        /**
         * @description 쉐도우 루트 사용 -> 글로벌 CSS 영향 X
         */
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.appendChild(materialInputTemplate.content.cloneNode(true));

    }

    /**
     * 
     * @returns {HTMLInputElement}
     */
    getInput() {
        return this.shadowRoot.querySelector('input');
    }

    /**
     * 
     * @returns {HTMLLabelElement}
     */
    getLabel() {
        return this.shadowRoot.querySelector('label');
    }

    get name() {
        return this.getInput().getAttribute('name');
    }

    set name(newValue) {
        this.getInput().setAttribute('name', newValue);
        this.getLabel().setAttribute('for', newValue);
    }

    get id() {
        return this.getInput().getAttribute('id');
    }

    set id(newValue) {
        this.getInput().setAttribute('id', newValue);
    }

    get type() {
        return this.getInput().getAttribute('type');
    }

    set type(newValue) {
        this.getInput().setAttribute('type', newValue);
    }

    get label() {
        return this.getInput().getAttribute('placeholder');
    }

    set label(newValue) {
        this.getInput().setAttribute('placeholder', newValue);
        this.getLabel().innerText = newValue;
    }

    get required() {
        return this.getInput().getAttribute('required');
    }

    set required(newValue) {
        this.getInput().setAttribute('required', newValue);
    }

    get min() {
        return this.getInput().getAttribute('min');
    }

    set min(newValue) {
        this.getInput().setAttribute('min', newValue);
    }

    get max() {
        return this.getInput().getAttribute('max');
    }

    set max(newValue) {
        this.getInput().setAttribute('max', newValue);
    }

    static get observedAttributes() {
        return ['name', 'id', 'type', 'label', 'required', 'min', 'max'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        switch (name) {
            case 'name':
                this.name = newValue;
                break;
            case 'id':
                this.id = newValue;
                break;
            case 'type':
                this.type = newValue;
                break;
            case 'label':
                this.label = newValue;
                break;
            case 'required':
                this.required = newValue;
                break;
            case 'min':
                this.min = newValue;
                break;
            case 'max':
                this.max = newValue;
                break;
        }
    }
}
/**
 * @description 커스텀 웹 컴포넌트 정의
 */
window.customElements.define('material-input', MaterialInput);