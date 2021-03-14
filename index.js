const Timidity = require("timidity");
const p5 = require("p5");

p5.getAudioContext().resume();
const player = new Timidity();
player.load("./music.mid");
player.play();

// player.on("playing", () => {
//   console.log(player.duration); // => 351.521
// });
