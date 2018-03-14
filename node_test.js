

// var script = require("path").join(__dirname, 'con.py --scooper "Ben" --schedule_id "1yGlxV9xSY6vk_d-WHoE9k18P06zfc7r8j975y5uvlJU"')
var script = require("path").join('python')
var salendar = require("child_process").spawn('python -u', [script]);

function uint8ToString(data) {
  return String.fromCharCode.apply(null, data);
}

salendar.stdout.on('data', function(data) {
  data = uint8ToString(data);
  try {
    JSON.parse(data);
    console.log("\nYAY")
    console.log(data)
  } catch(e) {
    console.log("\nHO")
    console.log(data)
  }
})

salendar.on('error', function(error) {
  console.log(error);
})
