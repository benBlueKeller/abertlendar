

var script = require("path").join(__dirname, "alberlendar.py")
var child = require("child_process").spawn('python', [script]);

function uint8ToString(data) {
  return String.fromCharCode.apply(null, data);
}

child.stdout.on('data', function(data) {
  data = uint8ToString(data);
  try {
    JSON.parse(data);
    console.log(data)
  } catch(e) {
    console.log("ho")
  }
})

child.on('error', function(error) {
  console.log(error);
})
