const postFeed = document.querySelector('.horizontal');

postFeed.addEventListener('wheel', e => {
  // Don't affect horizontal scrolls, don't do anything if we're not at the bottom of the page
  if (
    Math.abs(e.deltaX) > Math.abs(e.deltaY) ||
    window.innerHeight +
      document.documentElement.scrollTop -
      postFeed.offsetHeight <
      0
  ) {
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
