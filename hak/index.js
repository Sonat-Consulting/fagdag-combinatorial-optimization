
const fs = require('fs');

// Parse the data file
fs.readFile('../problem_generation/preferences-100-ppl.txt', 'utf-8', (err, data) => {
  if (err) throw err;
  console.log(data);
});


var data = {"1": [1,2,3]};

// TODO: count pref by person