/**
 * Tarot Helper - Pure XML/XSLT Approach
 * JS only handles URL routing, all data queries stay in XSLT
 */

console.log('[Tarot] helper.js active');

function setLanguage(lang) {
  // Redirect to appropriate XML entry point
  // Browser will handle native XSLT transformation
  // Keep ?deck= so the chosen deck survives the switch
  const page = lang === 'uk' ? 'index-uk.xml' : 'index.xml';
  window.location.href = page + window.location.search;
}

function setDeck(id) {
  // XSLT renders every deck; show the chosen one and hide the rest
  const deck = document.getElementById(`deck-${id}`);
  if (!deck) return;

  document.querySelectorAll('.deck, .deck-nav').forEach(el => {
    el.hidden = el.dataset.deck !== id;
  });
  document.querySelectorAll('.deck-switcher button').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.deck === id);
  });

  const name = document.querySelector(`.deck-switcher button[data-deck="${id}"]`).textContent.trim();
  document.title = `${name} - ${document.querySelector('h1').textContent.trim()}`;

  const url = new URL(window.location.href);
  url.searchParams.set('deck', id);
  history.replaceState(null, '', url);

  resetPlay();
}

function initDeck() {
  document.querySelectorAll('.deck-switcher button').forEach(btn => {
    btn.onclick = () => setDeck(btn.dataset.deck);
  });

  const id = new URLSearchParams(window.location.search).get('deck');
  if (id) setDeck(id);
}

function initUI() {
  const cards = document.querySelectorAll('.tarot-card');
  console.log(`[Tarot] Found ${cards.length} cards`);

  initCards();
  initModal();
  initPlay();
  initDeck();
}

// Draw pile of card ids; filled by shuffleDeck(), emptied by pullCard()
let drawPile = [];
let shuffled = false;

function initPlay() {
  const shuffleBtn = document.getElementById('shuffle-btn');
  const pullBtn = document.getElementById('pull-btn');
  if (!shuffleBtn || !pullBtn) return;

  shuffleBtn.onclick = shuffleDeck;
  pullBtn.onclick = pullCard;
  updatePile();
}

// Uniform random integer in [0, n), from the operating system's entropy pool.
// Math.random() has too little state to reach every ordering of a 78-card deck.
// Rejection sampling avoids the bias of taking a plain remainder.
function randomBelow(n) {
  const limit = Math.floor(0x100000000 / n) * n;
  const buf = new Uint32Array(1);
  do {
    crypto.getRandomValues(buf);
  } while (buf[0] >= limit);
  return buf[0] % n;
}

function shuffleDeck() {
  const ids = Array.from(document.querySelectorAll('#deck-main .deck:not([hidden]) .tarot-card'), card => card.id.replace('card-', ''));

  // Fisher-Yates
  for (let i = ids.length - 1; i > 0; i--) {
    const j = randomBelow(i + 1);
    [ids[i], ids[j]] = [ids[j], ids[i]];
  }

  drawPile = ids;
  shuffled = true;
  document.getElementById('spread').replaceChildren();
  updatePile();
}

function resetPlay() {
  drawPile = [];
  shuffled = false;
  document.getElementById('spread').replaceChildren();
  updatePile();
}

function pullCard() {
  const cid = drawPile.shift();
  if (cid === undefined) return;

  const source = document.getElementById(`card-${cid}`);
  const spread = document.getElementById('spread');

  const pulled = document.createElement('div');
  pulled.className = 'pulled-card';
  pulled.onclick = () => showCardDetails(cid);

  const position = document.createElement('span');
  position.className = 'pulled-position';
  position.textContent = spread.children.length + 1;

  const img = source.querySelector('img').cloneNode();
  img.removeAttribute('loading');

  const title = document.createElement('span');
  title.className = 'pulled-title';
  title.textContent = source.querySelector('.card-title')?.textContent.trim() || cid;

  pulled.append(position, img, title);
  spread.appendChild(pulled);
  updatePile();
}

function updatePile() {
  const pullBtn = document.getElementById('pull-btn');
  const count = document.getElementById('pile-count');

  pullBtn.disabled = drawPile.length === 0;
  count.textContent = shuffled ? `${count.dataset.label}: ${drawPile.length}` : '';
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

  const hebrew = getVal('.hebrew');
  const symbolism = card.querySelector('.card-symbolism')?.innerHTML;
  const description = card.querySelector('.card-description')?.innerHTML;

  modalBody.innerHTML = `
        <div class="modal-layout">
            <div class="modal-image-container">
                <img src="${card.querySelector('img').src}" alt="${getVal('.card-title')}">
            </div>
            <div class="modal-text">
                <div class="modal-header-meta">
                    <div>
                        <span class="card-number">${getVal('.card-number')}</span>
                        ${hebrew ? `<span class="hebrew">${hebrew}</span>` : ''}
                    </div>
                    <span class="tag">${getVal('.tag-mini')}</span>
                </div>
                <div class="modal-title-row">
                    <h2>${getVal('.card-title')}</h2>
                    <span class="sign-symbol">${card.querySelector('.sign-symbol')?.innerHTML.trim() || getVal('.tag-mini-suit')}</span>
                </div>
                ${description || !symbolism ? `<div class="full-description">${description || 'No description available.'}</div>` : ''}
                ${symbolism ? `<div class="modal-symbolism">${symbolism}</div>` : ''}
            </div>
        </div>
    `;
  modal.querySelector('.modal-content').scrollTop = 0;
  modal.style.display = 'flex';
}

window.onload = initUI;
