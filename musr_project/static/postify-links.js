const logoutLink = document.querySelector('a.logout');
const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]')
  .value;

// Universal form which is submitted in all methods
const form = new FormData();
form.append('csrfmiddlewaretoken', csrftoken);

// Logout link
logoutLink.onclick = e => {
  e.preventDefault();
  logout();
};

const logout = () => {
  fetch('/account/logout/', {
    method: 'POST',
    body: form
  }).then(() => {
    window.location.href = '/';
  });
};

// Delete buttons
const deletePost = e => {
  form.append('post_id', e.target.id);
  fetch('/delete-post', {
    method: 'POST',
    body: form
  }).then(() => {
    window.location.reload();
    // Potential feature: remove the relevant div here
    // TODO
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
