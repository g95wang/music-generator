const Timidity = require("timidity");

const player = new Timidity();
function playMusic() {
  player.load("music.mid");
  // getAudioContext().resume();
  player.play();

  player.on("playing", () => {
    console.log(player.duration); // => 351.521
  });
}

module.exports = { playMusic: playMusic };
