import { Player as _Player } from 'midi-player-js';
 
// Initialize player and register event handler
var Player = new _Player(function(event) {
    console.log(event);
});
 
function playMusic(){
    // Load a MIDI file
    Player.loadFile('./music.mid');
    Player.play();
}