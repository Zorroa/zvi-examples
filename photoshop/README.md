# Photoshop search panel

This example demonstrates the integration between Adobe Photoshop and Zorroa's ZMLP API.

## Requirements

This extension was written for MacOS. It utilizes a shell script to activate a python virtual environment before executing ZMLP API scripts.

- [zmlp client](https://pypi.org/project/zorroclient/)
- Adobe Photoshop 19+
- Python3
- ZVI Visualizer API Key
- Assumes images were already processed through ZVI's Visualizer application

Open _config.json_:

- apiKeyPath - full path to your apikey.json
- pyVirtualPath - optional path to pyenv bin/activate command.

Place the _photoshop_ folder in /Users/`USERNAME`/Library/Application Support/Adobe/CEP/extensions/

Open Photoshop and navigate to Window > Extensions > ZVI Panel to open the interface.
