// REORGANIZE THIS FILE! TODO TODO TODO
// AbortController for the fetch
const controller = new AbortController();
const singal = controller.signal;

function hookForm() {
  const input = document.querySelector('.songSearch');
  input.onkeyup = _.debounce(onChangeHandler, 50);

  const songSearchResults = document.querySelector('.songSearchResults');
  songSearchResults.onclick = selectSong;

  document.querySelector('.addPostButton').onclick = addPostButtonClickHandler;

  // Handle escape key
  document.onkeyup = e => {
    if (e.keyCode == 27) {
      document.querySelector('.container').classList.remove('addingPost');
    }
  };
}

const addPostButtonClickHandler = e => {
  document.querySelector('.songSearch').focus();
  document.querySelector('.container').classList.add('addingPost');
};

const onChangeHandler = e => {
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

    // reload the window in case we are on profile page
    window.setTimeout(() => {
      location.reload();
    }, 300);
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
              <div class="song textSize-m">
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

window.onload = hookForm;
