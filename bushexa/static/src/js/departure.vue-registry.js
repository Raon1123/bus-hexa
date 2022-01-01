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
     * @type {string | null}
     * @description 시간이 선택되지 않았을 경우 @type {null}, 
     *              선택되었을 경우 @type {string}입니다.
     *              후자일시에 0번 인덱스의 요소는 시(Hours), 1번 인덱스의 요소는 분(Minutes)입니다.
     */
    selectedTime: null,
    /**
     * 
     * @param {[number, number] | null} time
     * @description @property {[number, number] | null} selectedTime 의 setter입니다.
     */
    setSelectedTime(time) {
        if (time) {
            const [hrs, min] = time.map(value => value < 10 ? `0${value}` : value.toString());
            this.selectedTime = `${hrs}:${min}`
        } else {
            this.selectedTime = time;
        }
    },
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
                    .map(time => Number(time))
                console.log({hrs, min, currentHrs, currentMin})
                if (hrs > currentHrs || (hrs === currentHrs && min >= currentMin)) {
                    row.removeAttribute('style')
                } else {
                    row.style.display = 'none'
                }
            }
        )
        this.setSelectedTime([currentHrs, currentMin]);
        this.onEditTime = !this.onEditTime;
    }
}).mount()

