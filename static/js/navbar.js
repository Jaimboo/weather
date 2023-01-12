document.addEventListener('DOMContentLoaded', () => {
    [...document.querySelectorAll('.navbar .nav-link')].every( link => {
        if (link.getAttribute('href') == window.location.href.toString().split(window.location.host)[1]){
            link.classList.add('active')
            link.setAttribute('aria-current', 'page')
            return false
        }
        return true
    })
})