// AbortController for the fetch
const controller = new AbortController();
const singal = controller.signal;

function hookForm() {
  // Hook input that appears after click
  const input = document.querySelector('.songSearch');
  input.onkeyup = _.debounce(searchFieldChangeHandler, 250);

  // Hook song search results
  const songSearchResults = document.querySelector('.songSearchResults');
  songSearchResults.onclick = selectSong;

  // Hook add post button
  document.querySelector('.addPostButton').onclick = addPostButtonClickHandler;

  // Handle escape key
  document.onkeyup = closeAddPostForm;

  // Handle cancel button next to input
  document.querySelector('.closeSongSearchButton').onclick = closeAddPostForm;
}

window.onload = hookForm;

const closeAddPostForm = e => {
  if (!e.keyCode || e.keyCode == 27) {
    document.querySelector('.container').classList.remove('addingPost');
  }
};

const addPostButtonClickHandler = e => {
  document.querySelector('.songSearch').focus();
  document.querySelector('.container').classList.add('addingPost');
};

const searchFieldChangeHandler = e => {
  controller.abort();
  updateResults(e.target.value);
};

const selectSong = e => {
  // Browser compatibility
  const path = e.path || (e.composedPath && e.composedPath());
  // traverse tree of clicked elements to find the li so we can grab the ID
  const songId = path.find(element => {
    // Find LI element and check it has an id just to be safe
    return element.nodeName == 'LI' && element.id;
  }).id;

  const input = document.querySelector('.songIdInput');
  input.value = songId;

  const form = document.querySelector('.addPostForm');
  const url = form.action;

  fetch(url, {
    method: 'POST',
    body: new FormData(form)
  }).then(() => {
    // Success!
    form.reset();

    document.querySelector('.songSearchResults').innerHTML = 'Song added!';
    document.querySelector('.songSearch').value = '';

    // Remove ourselves -- and reload if we're on the profile page
    window.setTimeout(() => {
      document.querySelector('.container').classList.remove('addingPost');
    }, 500);
  });
};

const updateResults = query => {
  const songSearchResults = document.querySelector('.songSearchResults');
  // Move up search box in anticipation
  songSearchResults.classList.add('loaded');

  fetch(`https://deezer-proxy.glitch.me/search?q="${query}"`, {
    singal
  }).then(async result => {
    const json = await result.json();
    const html = json.data
      .map(song => {
        return `
            <li id="${song.id}">
              <div class="songSearchResult textSize-m spaceframe-m">
                <img src="${song.album.cover_small}" />
                <div class="songInfo minHeight-xl c-grey-1">
                  <strong>${song.title}</strong>
                  <div class="songInfo--artistAlbum textSize-s spacerBottom-s">
                    <div class="">${song.artist.name}</div>
                    <div>${song.album.title}</div>
                  </div>
                </div>
              </div>
            </li>
        `;
      })
      .join('');
    songSearchResults.innerHTML = html;
  });
};
