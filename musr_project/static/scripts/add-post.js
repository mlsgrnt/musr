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
  // Make the form dissapear if the escape key was pressed or no key was
  // pressed, suggesting the close button was clicked
  if (!e.keyCode || e.keyCode == 27) {
    document.querySelector('.container').classList.remove('addingPost');
  }
};

const addPostButtonClickHandler = e => {
  // Make the add post interface appear, and focus the input field
  // so typing can begin right away
  document.querySelector('.container').classList.add('addingPost');
  document.querySelector('.songSearch').focus();
};

const searchFieldChangeHandler = e => {
  // A new search is ready to fire, so abort the old one
  controller.abort();
  // Fire off new search
  updateResults(e.target.value);
};

const selectSong = e => {
  window.scrollTo(0, 0);

  // Browser compatibility
  const path = e.path || (e.composedPath && e.composedPath());

  // Traverse tree of clicked elements to find the li so we can grab the ID
  const songId = path.find(element => {
    // Find LI element and check it has an id just to be safe
    return element.nodeName == 'LI' && element.id;
  }).id;

  // Populate hidden form with song id
  const input = document.querySelector('.songIdInput');
  input.value = songId;

  // Grab url to POST to from hidden form
  const form = document.querySelector('.addPostForm');
  const url = form.action;

  fetch(url, {
    method: 'POST',
    body: new FormData(form)
  }).then(async response => {
    const body = await response;
    const responseText = await body.text();

    // Get ready for next song
    form.reset();
    document.querySelector('.songSearch').value = '';

    // Replace song list with message
    document.querySelector('.songSearchResults').innerHTML =
      responseText == 'OK'
        ? 'Song added!'
        : 'Failed to add song! Please try again.';

    // Remove ourselves
    window.setTimeout(() => {
      document.querySelector('.container').classList.remove('addingPost');
    }, 1000);
  });
};

const updateResults = query => {
  const songSearchResults = document.querySelector('.songSearchResults');
  // Move up search box in anticipation
  songSearchResults.classList.add('loaded');

  // Give user feedback
  songSearchResults.innerHTML = 'Loading...';

  // Initiate request
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
