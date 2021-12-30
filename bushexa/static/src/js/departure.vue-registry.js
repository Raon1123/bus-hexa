import { createApp } from 'https://unpkg.com/petite-vue?module'

createApp({
    $delimiters: ['${', '}'],
    /**
     * 
     * @type {boolean}
     * @description 시간 변경 버튼을 누를 때 변경되는 상태입니다
     */
    onEditTime: false,
    /**
     * 
     * @type {[number, number] | null}
     * @description 시간이 선택되지 않았을 경우 @type {null}, 
     *              선택되었을 경우 @type {[number, number]}입니다.
     *              후자일시에 0번 인덱스의 요소는 시(Hours), 1번 인덱스의 요소는 분(Minutes)입니다.
     */
    selectedTime: null,
    /**
     * 
     * @type {[number, number] | null}
     * @description @property {[number, number] | null} selectedTime 의 setter입니다.
     */
    setSelectedTime(time) {
        this.selectedTime = time;
    },
    /**
     * 
     * @param {HTMLElement} el 
     * @description 시간을 변경할 때는 폼을 보여주고, 그렇지 않으면 보여주지 않는 로직을 담당합니다
     */
    decideFormVisibility(el) {
        if (this.onEditTime) {
            el.removeAttribute('style')
        } else {
            el.style.display = 'none'
        }
    },
    /**
     * 
     * @param {HTMLElement} el
     * @description @property {[number, number] | null} selectedTime 의 값보다 항목의 버스 도착 시간이 더 늦으면 
     *              그 행을 표시합니다
     */
    decideRowVisibility(el) {
        if (!this.selectedTime) return;
        const [currentHrs, currentMin] = this.selectedTime;
        const [hrs, min] = el.querySelector('td').innerText.replace(' ', '').split(':')
        const shouldVisible = hrs > currentHrs || (hrs === currentHrs && min > currentMin)
        if (shouldVisible) {
            el.removeAttribute('style')
        } else {
            el.style.display = 'none'
        }
    },
    filterRows() {
        const [currentHrs, currentMin] = ['hours', 'minutes'].map(id => document.getElementById(id).value)
        const rows = document.querySelectorAll('.table .row')
        console.log('filtering')
        rows.map(
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
                if (hrs > currentHrs || (hrs === currentHrs && min > currentMin)) {
                    row.removeAttribute('style')
                } else {
                    row.style.display = 'none'
                }
            }
        )
        this.onEditTime = !this.onEditTime;
    }
}).mount()

