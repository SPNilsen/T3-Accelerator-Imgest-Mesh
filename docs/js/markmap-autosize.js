(function () {
  function attachAutoSize(root = document) {
    // Each rendered Markmap gets an <svg> inside a wrapper with class "markmap"
    root.querySelectorAll('.markmap').forEach(wrapper => {
      const svg = wrapper.querySelector('svg');
      if (!svg) return;

      const setHeight = () => {
        try {
          // Compute actual content bbox and add a little padding
          const box = svg.getBBox();
          const pad = 24;
          wrapper.style.height = `${Math.ceil(box.height + pad)}px`;
        } catch (_) {
          // getBBox can throw if SVG not ready yet; ignore
        }
      };

      // Initial pass (after a tick so Markmap has rendered)
      setTimeout(setHeight, 0);

      // Recompute when SVG changes (nodes open/close) or on window resizes
      const ro = new ResizeObserver(setHeight);
      ro.observe(svg);
      window.addEventListener('resize', setHeight, { passive: true });

      // Keep a handle so we could disconnect later if needed
      wrapper._mmResizeObserver = ro;
    });
  }

  // Material for MkDocs SPA hook + normal load
  if (window.document$) window.document$.subscribe(() => attachAutoSize());
  document.addEventListener('DOMContentLoaded', () => attachAutoSize());
})();
