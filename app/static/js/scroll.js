document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.navbar');
    const placeholder = document.createElement('div');
    placeholder.style.display = 'none';
    navbar.parentNode.insertBefore(placeholder, navbar);

    const updateNavbarMetrics = () => {
        placeholder.style.height = `${navbar.offsetHeight}px`;
    };

    const handleScroll = () => {
        const offsetTop = navbar.offsetTop;
        if (window.scrollY > offsetTop) {
            navbar.classList.add('navbar-fixed');
            placeholder.style.display = 'block';
        } else {
            navbar.classList.remove('navbar-fixed');
            placeholder.style.display = 'none';
        }
    };

    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', () => {
        updateNavbarMetrics();
        handleScroll();
    });

    updateNavbarMetrics();
    handleScroll();
});
