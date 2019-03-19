let audioElementCurrentlyPlaying;

// Use function syntax so "this" binds to the button
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
    // Pause other song if it's playing
    audioElementCurrentlyPlaying
      ? audioElementCurrentlyPlaying.pause()
      : undefined;

    audioElementCurrentlyPlaying = document.getElementById(`audio-${songId}`);
    audioElementCurrentlyPlaying.addEventListener('play', () => {
      this.innerHTML = '❚❚';
    });
    audioElementCurrentlyPlaying.addEventListener('pause', () => {
      this.innerHTML = '▶';
    });

    // After set up, actually play
    audioElementCurrentlyPlaying.play().catch(error => {
      this.classList.add('textSize-s'); // Make the error a little more appealing
      this.innerHTML = 'Preview not available';
    });
  }

  // Potentially add event listeners for reacting to other playback events (buffering etc)
}

// Hook all buttons
const playButtons = Array.from(document.querySelectorAll('.play'));
playButtons.forEach(button => button.addEventListener('click', handleClick));
