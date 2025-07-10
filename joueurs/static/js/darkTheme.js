document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('toggleThemeBtn');
  const html = document.documentElement;

  const savedTheme = localStorage.getItem('theme') || 'light';
  html.setAttribute('data-bs-theme', savedTheme);

  function updateIcon(theme) {
    if (theme === 'dark') {
      toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
      toggleBtn.classList.remove('btn-outline-light');
      toggleBtn.classList.add('btn-outline-warning');
    } else {
      toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
      toggleBtn.classList.remove('btn-outline-warning');
      toggleBtn.classList.add('btn-outline-light');
    }
  }

  updateIcon(savedTheme);

  toggleBtn.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateIcon(newTheme);
  });
});
