const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]')
  .value;

// Universal form which is submitted in all methods
const form = new FormData();
form.append('csrfmiddlewaretoken', csrftoken);

// Logout link
const logout = () => {
  logoutLink.innerHTML = 'Logging out...';

  fetch('/account/logout/', {
    method: 'POST',
    body: form
  }).then(() => {
    window.location.href = '/';
  });
};

const logoutLink = document.querySelector('a.logout');
logoutLink.onclick = e => {
  e.preventDefault();
  logout();
};

// Delete buttons
const deletePost = e => {
  form.append('post_id', e.target.id);
  fetch('/delete-post', {
    method: 'POST',
    body: form
  }).then(() => {
    // This is very coupled with the structure of the document
    const postElement = e.target.parentNode.parentNode;
    postElement.remove();
  });
};
Array.from(document.querySelectorAll('.deleteButton')).forEach(
  button => (button.onclick = deletePost)
);

// Repost buttons
const repostPost = e => {
  form.append('post_id', e.target.id);
  fetch('/repost-post', {
    method: 'POST',
    body: form
  }).then(() => {
    e.target.innerHTML = 'Reposted!';
    e.target.classList.add('reposted');
  });
};
Array.from(document.querySelectorAll('.repostButton')).forEach(
  button => (button.onclick = repostPost)
);

// Follow/Unfollow button
const followButtonHandler = e => {
  form.append('username', e.target.id);
  // This is quite unsafe -- a malicious extension could manipulate this to do some nasty things.
  // That being said, a malicious extension will always be able to do nasty things, so given that
  // no sensitive user input is presented on this page we should be alright for now
  fetch(`/${e.target.innerHTML.toLowerCase()}`, {
    method: 'POST',
    body: form
  }).then(() => {
    e.target.innerHTML += 'ed!';
    window.location.reload();
  });
};
const followButton = document.querySelector('.profile--buttons--followButton');
if (followButton) {
  followButton.onclick = followButtonHandler;
}
