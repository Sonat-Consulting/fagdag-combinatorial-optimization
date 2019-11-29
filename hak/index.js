
const fs = require('fs');
const readline = require('readline');

class Pref {

  constructor() {
    this.tracks = 3;
    this.times = 15;
  }

}

class Solution {

  constructor(pref) {
    this.data = []
  }

  calcScore() {

  }

  moveTime(offset) {

  }

  moveTrack(offset) {

  }

  print() {

  }
}

console.log(new Solution());

const input100 = {
  tracks: 3,
  times: 15,
  file: '../problem_generation/preferences-100-ppl.txt'
};

const input4000 = {
  tracks: 8,
  times: 15,
  file: '../problem_generation/preferences-4000-ppl.txt'
};

const input = input100;

async function processLineByLine() {
  const fileStream = fs.createReadStream(input.file);

  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });
  // Note: we use the crlfDelay option to recognize all instances of CR LF
  // ('\r\n') in input.txt as a single line break.

  let data = {};
  for await (const line of rl) {
    const reg = /^(\d+):(.*)$/;
    const matches = reg.exec(line);
    if (matches !== null) {
      const preferences = JSON.parse(matches[2]);
      data[matches[1]] = preferences;
    }
  }
  let count = {};

  const tracks = input.tracks;
  const times = input.times;
  const maxPref = tracks * times;
  for (let i = 1; i <= maxPref; i++) {
    count[i] = 0;
  }
  for (const p of Object.keys(data)) {
    for (const pref of data[p]) {
      count[pref] += 1;
    }
  }
  count = Object.entries(count).sort((a, b) => b[1] - a[1] );



  const res = [];
  for (let j = 0; j < times; j++) {
    res.push([]);
  }
  for (let pos = 0; pos < count.length; pos++) {
    res[pos % times].push(count[pos][0]);
  }
  console.log("[" + res.map(t => {
    return "{" + t.join(", ") + "}"
  }).join(", ") + "]");
//  console.log("Count", res);

}

processLineByLine();