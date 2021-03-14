const Timidity = require("timidity");

getAudioContext().resume();
const player = new Timidity();
player.load("./music.mid");
player.play();

// player.on("playing", () => {
//   console.log(player.duration); // => 351.521
// });
