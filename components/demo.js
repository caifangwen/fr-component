/**
 * 个人组件库 - 交互逻辑
 * 原生 JS，零依赖
 */

/* ========================================
   主题切换 (Multi-theme)
   ======================================== */
const html = document.documentElement;
const themeSelect = document.getElementById('themeSelect');

function applyTheme(theme) {
    if (theme && theme !== 'light') {
        html.setAttribute('data-theme', theme);
    } else {
        html.removeAttribute('data-theme');
    }
    if (themeSelect) themeSelect.value = theme || '';
}

function changeTheme(theme) {
    applyTheme(theme);
    localStorage.setItem('theme', theme);
}

// 初始化主题
(function initTheme() {
    const saved = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(saved || (prefersDark ? 'dark' : ''));
})();

/* ========================================
   弹窗增强
   ======================================== */
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-backdrop.is-open').forEach(m => {
            m.classList.remove('is-open');
        });
    }
});

/* ========================================
   导航高亮（根据滚动位置）
   ======================================== */
(function initNavHighlight() {
    const navLinks = document.querySelectorAll('.nav__link[href^="#"]');
    const sections = [];
    navLinks.forEach(link => {
        const id = link.getAttribute('href').slice(1);
        const sec = document.getElementById(id);
        if (sec) sections.push({ link, sec });
    });

    function update() {
        const scrollPos = window.scrollY + 100;
        let active = null;
        sections.forEach(({ link, sec }) => {
            if (sec.offsetTop <= scrollPos) active = link;
            link.classList.remove('is-active');
        });
        if (active) active.classList.add('is-active');
    }

    window.addEventListener('scroll', update);
    update();
})();

/* ========================================
   表单交互增强
   ======================================== */
document.querySelectorAll('.form-input, .form-textarea').forEach(input => {
    // 简单的字符计数示例
    const maxLength = input.getAttribute('maxlength');
    if (maxLength && input.parentElement) {
        const hint = document.createElement('p');
        hint.className = 'form-hint';
        input.parentElement.appendChild(hint);

        input.addEventListener('input', () => {
            const remaining = maxLength - input.value.length;
            hint.textContent = `${remaining} 字剩余`;
            hint.style.color = remaining < 20 ? 'var(--color-warning)' : 'var(--color-text-light)';
        });
    }
});

/* ========================================
   Alert 关闭按钮（动态生成）
   ======================================== */
document.querySelectorAll('.alert').forEach(alert => {
    const closeBtn = alert.querySelector('.alert__close');
    if (!closeBtn) return;
    closeBtn.addEventListener('click', () => {
        alert.style.transition = 'opacity 250ms ease, transform 250ms ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-8px)';
        setTimeout(() => alert.remove(), 250);
    });
});

/* ========================================
   通用工具函数（暴露到全局供 HTML 调用）
   ======================================== */
window.ComponentUtils = {
    /**
     * 打开弹窗
     * @param {string} id - modal-backdrop 的 id
     */
    openModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.classList.add('is-open');
    },

    /**
     * 关闭弹窗
     * @param {string} id - modal-backdrop 的 id
     */
    closeModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.classList.remove('is-open');
    },

    /**
     * 防抖函数
     */
    debounce(fn, delay = 300) {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    },

    /**
     * 节流函数
     */
    throttle(fn, limit = 300) {
        let inThrottle;
        return (...args) => {
            if (!inThrottle) {
                fn.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};
