
/**
 * @description 템플릿 정의
 */
const textButtonTemplate = document.createElement('template')
textButtonTemplate.innerHTML = `
    <style>
        @import url(https://fonts.googleapis.com/css?family=Roboto);

        html {
            font-family: 'Roboto', sans-serif;
        }
        
        button {
            cursor: pointer;
            display: inline-block;
            background-color: transparent;
            border: none;
        }
        
        button span {
            font-size: 1.1rem;
            font-weight: bold;
            text-decoration: none;
            color: #0097fc;
        }

        button:hover span {
            color: #009788;
            text-decoration: underline;
        }
    </style>

    <button>
        <span></span>
    </button>
`
class TextButton extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({ mode: 'open' });
        this.shadowRoot.appendChild(textButtonTemplate.content.cloneNode(true));
    }

    /**
     * 
     * @returns {HTMLButtonElement}
     */
    getButton() {
        return this.shadowRoot.querySelector('button');
    }

    /**
     * 
     * @returns {HTMLSpanElement}
     */
    getSpan() {
        return this.shadowRoot.querySelector('span');
    }

    get label() {
        return this.getSpan().innerText;
    }

    set label(newValue) {
        this.getSpan().innerText = newValue;
    }

    get onclick() {
        return this.getButton().getAttribute('onclick');
    }

    set onclick(newValue) {
        this.getButton().setAttribute('onclick', newValue);
    }

    static get observedAttributes() {
        return ['label', 'onclick']
    }

    attributeChangedCallback(name, oldValue, newValue) {
        switch (name) {
            case 'label':
                this.label = newValue;
                break;
            case 'onclick':
                this.onclick = newValue;
                break;
        }
    }
}
/**
 * @description 커스텀 웹 컴포넌트 정의
 */
window.customElements.define('text-button', TextButton);