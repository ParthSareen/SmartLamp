let Leap = require('leapjs');
let CircularJSON = require('circular-json');

var controller = new Leap.Controller({frameEventName: "deviceFrame"});

let n = 0;
controller.on('frame', function(frame) {
  if (frame.hands.length >= 1) {
    let hand = frame.hands[0];
    /*
    console.log(
      frame.hands
    );
    */
    console.log({
      position: hand.palmPosition,
      pinch: hand.pinchStrength
    });
  }
});

controller.connect();
