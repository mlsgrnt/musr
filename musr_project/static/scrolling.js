const postFeed = document.querySelector('.horizontal');

postFeed.addEventListener('mousewheel', e => {
  if (
    window.innerWidth + postFeed.scrollLeft != postFeed.scrollWidth &&
    e.deltaY > 0
  ) {
    e.preventDefault();
  }
  if (postFeed.scrollLeft != 0 && e.deltaY < 0) {
    e.preventDefault();
  }

  postFeed.scrollLeft += e.deltaY; // Scroll the feed
});
