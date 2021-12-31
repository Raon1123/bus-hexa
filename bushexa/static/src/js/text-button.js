
/**
 * @description 템플릿 정의
 */
const template = document.createElement('template')
template.innerHTML = `
    <style>
        @import url(https://fonts.googleapis.com/css?family=Roboto);

        html {
            font-family: 'Roboto', sans-serif;
        }
        
        button {
            cursor: pointer;
            display: inline-block;
            font-weight: bold;
            text-decoration: none;
            color: #0097fc;
            background-color: transparent;
            font-size: 1.1rem;
            border: none;
        }

        button:hover {
            color: #009788;
            text-decoration: underline;
        }
    </style>

    <button></button>
`
class TextButton extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({ mode: 'open' });
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }

    /**
     * 
     * @returns {HTMLButtonElement}
     */
    getButton() {
        return this.shadowRoot.querySelector('button');
    }

    get label() {
        return this.getButton().innerHTML;
    }

    set label(newValue) {
        return this.getButton().innerHTML = newValue;
    }
}
/**
 * @description 커스텀 웹 컴포넌트 정의
 */
window.customElements.define('text-button', TextButton);