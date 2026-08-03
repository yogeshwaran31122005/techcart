document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }, 3000);
    });

    const heroCard = document.getElementById('hero-3d-card');
    if (heroCard) {
        heroCard.addEventListener('mousemove', (event) => {
            const rect = heroCard.getBoundingClientRect();
            const x = ((event.clientX - rect.left) / rect.width - 0.5) * 20;
            const y = ((event.clientY - rect.top) / rect.height - 0.5) * -20;
            heroCard.style.transform = `perspective(1400px) rotateX(${y}deg) rotateY(${x}deg)`;
        });

        heroCard.addEventListener('mouseleave', () => {
            heroCard.style.transform = 'perspective(1400px) rotateX(0deg) rotateY(0deg)';
        });
    }
});
