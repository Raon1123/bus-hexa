
/**
 * @description 템플릿 정의
 */
const template = document.createElement('template')
template.innerHTML = `
    <style>
        @import url(https://fonts.googleapis.com/css?family=Roboto);

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

    <form>
        <div>
            <input id="hours" type="number" name="min" min="0" max="24" placeholder="Hours" required />
            <label for="hours">Hours</label>
        </div>
        <div>
            <input id="minutes" type="number" name="min" min="0" max="59" placeholder="Minutes" required />
            <label for="minutes">Minutes</label>
        </div>
        <button @click="onEditTime=!onEditTime">시간 변경</button>
    </form>
`
class EditTimeForm extends HTMLElement {
    constructor() {
        super();

        /**
         * @description 쉐도우 루트 사용 -> 글로벌 CSS 영향 X
         */
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.appendChild(template.content.cloneNode(true));
        this.shadowRoot.querySelector('form').addEventListener('submit', (e) => {
            // 이걸 가능케 해야함
            e.target.closest('edit-time-form').submit(e);
        });
    }
}
/**
 * @description 커스텀 웹 컴포넌트 정의
 */
window.customElements.define('edit-time-form', EditTimeForm);