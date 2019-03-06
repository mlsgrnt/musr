const link = document.querySelector('a.logout');
const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]')
  .value;

const form = new FormData();
form.append('csrfmiddlewaretoken', csrftoken);

link.onclick = e => {
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
