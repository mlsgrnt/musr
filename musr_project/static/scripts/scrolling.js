const postFeed = document.querySelector('.horizontal');

postFeed.addEventListener('wheel', e => {
  // Don't affect horizontal scrolls
  if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
    return;
  }

  if (
    (window.innerWidth + postFeed.scrollLeft != postFeed.scrollWidth &&
      e.deltaY > 0) ||
    (postFeed.scrollLeft != 0 && e.deltaY < 0)
  ) {
    e.preventDefault();
  }

  postFeed.scrollLeft += e.deltaY; // Scroll the feed
});
