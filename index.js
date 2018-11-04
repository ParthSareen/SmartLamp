const { spawn } = require('child_process');
let fs = require('fs');
//let demo = spawn('python', ['demo.py']);

let Leap = require('leapjs');
let CircularJSON = require('circular-json');

var controller = new Leap.Controller({frameEventName: "deviceFrame"});

let n = 0;
let safe = true;
controller.on('frame', function(frame) {
  if (frame.hands.length >= 1) {
    let hand = frame.hands[0];
    let data = {
      position: hand.palmPosition,
      pinch: hand.pinchStrength
    };
    console.log(data);
    if (safe) {
      safe = false;
      fs.writeFile('data.json', JSON.stringify(data), (err) => {
        if (err) console.log('ERROR: ' + err);
        else safe = true;
      });
    }
    process.stdout.write('.');

    //demo.stdin.write(JSON.stringify(data));
    //demo.stdin.flush();
  }
});

/*demo.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

///demo.stderr.on('data', (data) => {
  console.log(`stderr: ${data}`);
});
*/
controller.connect();

//demo.stdin.write('hello world!');
