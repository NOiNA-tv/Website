// Minimal image-slot: swaps a static image for an animated one on hover.
class ImageSlot extends HTMLElement {
  connectedCallback() {
    const staticSrc = this.getAttribute('static-src');
    const animSrc = this.getAttribute('anim-src') || staticSrc;
    const alt = this.getAttribute('alt') || '';

    const img = document.createElement('img');
    img.src = staticSrc;
    img.alt = alt;
    img.style.maxWidth = '100%';
    img.style.display = 'block';

    this.appendChild(img);

    this.addEventListener('mouseenter', () => { img.src = animSrc; });
    this.addEventListener('mouseleave', () => { img.src = staticSrc; });
  }
}

customElements.define('image-slot', ImageSlot);
