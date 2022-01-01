import { createApp } from 'https://unpkg.com/petite-vue?module'

createApp({
    $delimiters: ['${', '}'],
    /**
     * 
     * @type {boolean}
     * @description 시간 변경 버튼을 누를 때 변경되는 상태입니다
     */
    onEditTime: false,
    toggleOnEditTime() {
        this.onEditTime = !this.onEditTime;
    },
    /**
     * 
     * @type {string}
     * @description 'loading...'은 initializing value입니다
     *              @type {string}은 시간을 의미합니다.
     */
    selectedTime: 'Loading...',
    /**
     * 
     * @param {[number, number] | string} time
     * @description @type {[number, number]}일 경우에는 [0]을 시, [1]을 분으로 가정하고 이를 ':'로 구분하여 문자화합니다.
     */
    setSelectedTime(time) {
        if (typeof time === 'string') {
            this.selectedTime = time;
        } else {
            const [hrs, min] = time.map(value => value < 10 ? `0${value}` : value);
            this.selectedTime = `${hrs}:${min}`
        }
    },
    /**
     * 
     * @description 유저가 #edit-time-form에서 입력한 시간 (시, 분)의 값을 읽고,
     *              각 배차시간 행들의 출발시간을 읽은 뒤,
     *              이를 유저가 입력한 시간과 비교합니다.
     *              입력한 시간보다 출발시간이 빠르지 않은 행만 표시합니다.
     */
    filterRows() {
        const getInputValueById = (id) => 
            document
            .querySelector('#edit-time-form')
            .querySelector(`#${id}`) // material-input
            .shadowRoot
            .querySelector('input')
            .value;
        const [currentHrs, currentMin] = ['hours', 'minutes']
            .map(getInputValueById)
            .map(value => Number(value));
        const rows = document.querySelectorAll('.table .row')
        rows.forEach(
            /** 
             * @param {HTMLElement} row
             */
            row => {
                const [hrs, min] = row
                    .querySelector('td')
                    .innerText
                    .replace(' ', '')
                    .split(':')
                    .map(time => time.charAt(0) === '0' ? time.charAt(1) : time)
                    .map(time => Number(time));
                if (hrs > currentHrs || (hrs === currentHrs && min >= currentMin)) {
                    row.removeAttribute('style')
                } else {
                    row.style.display = 'none'
                }
            }
        )
        this.setSelectedTime([currentHrs, currentMin]);
        this.toggleOnEditTime();
    }
}).mount()

