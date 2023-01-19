document.addEventListener('DOMContentLoaded', () => {

    // setting navbar link to active
    [...document.querySelectorAll('.navbar .nav-link')].every( link => {
        if (link.getAttribute('href') == window.location.href.toString().split(window.location.host)[1]){
            link.classList.add('active')
            link.setAttribute('aria-current', 'page')
            return false
        }
        return true
    })
    
    let flash_container = document.querySelector('.flash-container');
    if (flash_container != null){
        flash_container.classList.toggle('fade')
        setTimeout(() => {flash_container.classList.toggle('fade')}, 3000)
    }
})