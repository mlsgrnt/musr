let audioElementCurrentlyPlaying;

// use function syntax so this binds to the button
function handleClick(e) {
  const songId = e.target.id;

  // If currently playing song is this buttons song
  if (
    audioElementCurrentlyPlaying &&
    audioElementCurrentlyPlaying.id == `audio-${songId}`
  ) {
    audioElementCurrentlyPlaying.paused
      ? audioElementCurrentlyPlaying.play()
      : audioElementCurrentlyPlaying.pause();
  } else {
    audioElementCurrentlyPlaying
      ? audioElementCurrentlyPlaying.pause()
      : undefined; // Pause other song if playing

    audioElementCurrentlyPlaying = document.getElementById(`audio-${songId}`);
    audioElementCurrentlyPlaying.addEventListener('play', () => {
      this.innerHTML = '❚❚';
    });
    audioElementCurrentlyPlaying.addEventListener('pause', () => {
      this.innerHTML = '▶';
    });

    // After set up, actually play
    audioElementCurrentlyPlaying.play();
  }

  // TODO: add event listeners for reacting to other playback events (buffering etc)
}

// Hook all buttons
const playButtons = Array.from(document.querySelectorAll('.play'));
playButtons.forEach(button => button.addEventListener('click', handleClick));
