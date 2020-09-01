/* 1) Create an instance of CSInterface. */
const { exec } = require("child_process");
const fs = require("fs");

let rawData = fs.readFileSync(__dirname + "/config.json");
let config = JSON.parse(rawData);

const API_SERVER = config.apiServer;
// const EXT_ROOT = config.extRoot;
const API_KEY_PATH = config.apiKeyPath;
const PY_VIRTUAL_ENV = config.pyVirtualPath;
var csInterface = new CSInterface();

var zvi = {
  createAssetRow: function (file) {
    let id = file.split(".")[0];
    return $(
      '<div class="mb-3 pics animation all 2">' +
        '<button id="sim' +
        id +
        '"type="button" class="similar-button">' +
        '<svg viewBox="0 0 20 20" height="20" color="#ffffff"><path fill="currentColor" d="M12 0a8 8 0 013.293 15.293A8 8 0 114.708 4.707 8 8 0 0112 0zM4.014 7.516l-.106.096a6 6 0 108.577 8.374 8 8 0 01-8.47-8.47zM8 6a6 6 0 00-1.743.257 6 6 0 007.486 7.486A6 6 0 008 6zm4-4a5.985 5.985 0 00-4.485 2.014 8 8 0 018.47 8.47A6 6 0 0012 2z"></path></svg></button>' +
        '<img class="img-fluid"' +
        'src="./assets/' +
        file +
        '"' +
        'alt="Missing Image"' +
        "/></div>"
    );
  },
  updateView: function (data) {
    $("#gallery").empty();
    let gallery = $("#gallery");
    count = 0;
    // var row;
    data["assets"].forEach((elem) => {
      let assetDiv = zvi.createAssetRow(elem.file_ref);
      $(assetDiv)
        .find("img")
        .on("click", function (e) {
          zvi.openDocument(elem.file_ref);
        });
      $(assetDiv)
        .find(".similar-button")
        .on("click", function (e) {
          zvi.searchSimilarity(elem.file_ref.split(".")[0]);
        });
      gallery.prepend(assetDiv);
    });
  },
  parseAssets: async function (path) {
    return await new Promise((resolve, reject) => {
      fs.readFile(path, (err, data) => {
        if (!err) {
          data = JSON.parse(data);
          resolve(data);
        } else {
          reject(err);
        }
      });
    });
  },
  searchAsset: function (term) {
    let query =
      "sh '" +
      __dirname +
      "/host/get_files.sh' -k '" +
      API_KEY_PATH +
      "' -s " +
      API_SERVER +
      " -e '" +
      __dirname +
      "' -v '" +
      PY_VIRTUAL_ENV +
      "' -t '" +
      term +
      "'";
    exec(query, (err, stdout, stderr) => {
      zvi.parseAssets(__dirname + "/host/assets.json").then((data) => {
        zvi.updateView(data);
      });
    });
  },
  searchSimilarity: function (id) {
    let query =
      "sh '" +
      __dirname +
      "/host/get_files.sh' -k '" +
      API_KEY_PATH +
      "' -s " +
      API_SERVER +
      " -e '" +
      __dirname +
      "' -v '" +
      PY_VIRTUAL_ENV +
      "' -m " +
      id +
      "";
    exec(query, (err, stdout, stderr) => {
      zvi.parseAssets(__dirname + "/host/assets.json").then((data) => {
        zvi.updateView(data);
      });
    });
  },
  openDocument: function (elem) {
    csInterface.evalScript("openDocument('" + __dirname + "', '" + elem + "')");
  },
};
