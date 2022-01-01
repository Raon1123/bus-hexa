
/**
 * @description 템플릿 정의
 */
const plainFormTemplate = document.createElement('template')
plainFormTemplate.innerHTML = `
    <form>
        <slot />
    </form>
`
class PlainForm extends HTMLElement {
    constructor() {
        super();

        /**
         * @description 쉐도우 루트 사용 -> 글로벌 CSS 영향 X
         */
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.appendChild(plainFormTemplate.content.cloneNode(true));
    }

    /**
     * 
     * @returns {HTMLFormElement}
     */
    getForm() {
        return this.shadowRoot.querySelector('form');
    }

    get onsubmit() {
        return this.getForm().getAttribute('onsubmit');
    }

    set onsubmit(newValue) {
        this.getForm().setAttribute('onsubmit', newValue);
    }

    static get observedAttributes() {
        return ['onsubmit']
    }

    attributeChangedCallback(name, oldValue, newValue) {
        switch (name) {
            case 'onsubmit':
                this.onsubmit = newValue;
                break;
        }
    }
}
/**
 * @description 커스텀 웹 컴포넌트 정의
 */
window.customElements.define('plain-form', PlainForm);