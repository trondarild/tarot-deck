/**
 * Tarot Helper - Pure XML/XSLT Approach
 * JS only handles URL routing, all data queries stay in XSLT
 */

console.log('[Tarot] helper.js active');

function setLanguage(lang) {
  // Redirect to appropriate XML entry point
  // Browser will handle native XSLT transformation
  if (lang === 'uk') {
    window.location.href = 'index-uk.xml';
  } else {
    window.location.href = 'index.xml';
  }
}

function initUI() {
  const cards = document.querySelectorAll('.tarot-card');
  console.log(`[Tarot] Found ${cards.length} cards`);

  initCards();
  initModal();
}

function initCards() {
  document.querySelectorAll('.tarot-card').forEach(card => {
    card.onclick = () => showCardDetails(card.id.replace('card-', ''));
  });
}

function initModal() {
  let overlay = document.querySelector('.modal-overlay');
  if (overlay) overlay.remove();

  overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.style.display = 'none';
  overlay.innerHTML = '<div class="modal-content"><button class="close-btn">&times;</button><div class="modal-body"></div></div>';
  document.body.appendChild(overlay);

  overlay.querySelector('.close-btn').onclick = () => overlay.style.display = 'none';
  overlay.onclick = (e) => { if (e.target === overlay) overlay.style.display = 'none'; };
}

function showCardDetails(cid) {
  const card = document.getElementById(`card-${cid}`);
  const modal = document.querySelector('.modal-overlay');
  if (!card || !modal) return;

  const modalBody = modal.querySelector('.modal-body');
  const getVal = (sel) => card.querySelector(sel)?.textContent || '';

  modalBody.innerHTML = `
        <div class="modal-layout">
            <div class="modal-image-container">
                <img src="${card.querySelector('img').src}" alt="${getVal('.card-title')}">
            </div>
            <div class="modal-text">
                <div class="modal-header-meta" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid #2e3440; padding-bottom: 0.75rem;">
                    <div>
                        <span class="card-number" style="font-size: 1.8rem; color: #d08770; font-weight: 700;">${getVal('.card-number')}</span>
                        ${getVal('.hebrew') ? `<span style="margin: 0 1rem; color: #4c566a">|</span><span class="hebrew" style="font-size: 2.2rem;">${getVal('.hebrew')}</span>` : ''}
                    </div>
                    <span class="tag">${getVal('.tag-mini')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                    <h2 style="font-size: 2.8rem; margin: 0; text-transform: uppercase;">${getVal('.card-title')}</h2>
                    <span class="sign-symbol" style="font-size: 3rem; color: #bf616a;">${getVal('.sign-symbol') || getVal('.tag-mini-suit')}</span>
                </div>
                <div class="full-description" style="font-size: 1.15rem; line-height: 1.7;">${card.querySelector('.card-description').innerHTML}</div>
            </div>
        </div>
    `;
  modal.style.display = 'flex';
}

window.onload = initUI;
