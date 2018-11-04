// spawn_python.js

var spawn = require("child_process").spawn;
var proc = spawn('python',["python_launched_from_nodejs.py"]);

//util.log('readingin')
/*
setInterval(() => {
  proc.stdin.write('this is data');
  console.log('exec');
}, 1000);
*/

process.stdin.pipe(proc.stdin)


proc.stdout.on('data',function(chunk){
    var textChunk = chunk.toString('utf8');// buffer to string
    console.log(textChunk);
});
