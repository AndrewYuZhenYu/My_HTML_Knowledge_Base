/* Copy the exact fenced-code text, including indentation and line breaks. */
(() => {
  const timers = new WeakMap();

  const fallbackCopy = (value) => {
    const field = document.createElement('textarea');
    field.value = value;
    field.setAttribute('readonly', '');
    field.style.cssText = 'position:fixed;left:-9999px;top:0;opacity:0';
    document.body.append(field);
    field.select();
    let copied = false;
    try { copied = document.execCommand('copy'); } catch (_) { /* try modern API next */ }
    field.remove();
    return copied;
  };

  const feedback = (button, message) => {
    const label = button.querySelector('.code-copy-label');
    if (!label) return;
    label.textContent = message;
    button.setAttribute('aria-label', message);
    button.classList.toggle('copied', message === '已复制');
    clearTimeout(timers.get(button));
    timers.set(button, setTimeout(() => {
      label.textContent = '复制代码';
      button.setAttribute('aria-label', '复制代码');
      button.classList.remove('copied');
    }, 2200));
  };

  document.addEventListener('click', async (event) => {
    const button = event.target.closest('[data-copy-code]');
    if (!button) return;
    const code = button.closest('.code-panel')?.querySelector('pre code');
    if (!code) return;
    const value = code.textContent;
    let copied = false;
    if (navigator.clipboard?.writeText) {
      try { await navigator.clipboard.writeText(value); copied = true; } catch (_) { /* local file fallback */ }
    }
    if (!copied) copied = fallbackCopy(value);
    if (copied) {
      feedback(button, '已复制');
    } else {
      const selection = window.getSelection?.();
      if (selection && document.createRange) {
        const range = document.createRange();
        range.selectNodeContents(code);
        selection.removeAllRanges();
        selection.addRange(range);
        feedback(button, '已选中，请手动复制');
      } else {
        feedback(button, '复制失败');
      }
    }
  });
})();
