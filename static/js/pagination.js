document.addEventListener('DOMContentLoaded', () => {

    let pager_btn = document.querySelectorAll('.page-item button')
    let page = document.querySelectorAll('#pagination tbody')
    
    page[0].classList.add('show')
    pager_btn[0].classList.add('act')

    pager_btn.forEach(btn => {

        btn.addEventListener('click', () => {

            document.querySelector('.page-item .act').classList.remove('act')
            btn.classList.add('act')
            document.querySelector('tbody.show').classList.remove('show')
            let index = btn.value - 1
            page[index].classList.add('show')
        })
    })


})