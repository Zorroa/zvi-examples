# Generate WEBVTT caption files for web video players.

### Prerequisites:

- HTML5
- Javascript
- Python
- Video Processed through ZVI

Download the contents in https://github.com/Zorroa/zvi-examples/tree/master/videoplayer

This example demonstrates how we can generate WEBVTT caption files to play alongside an HTML5 video player. After processing video assets with Google's Video Intelligence and Google Speech-To-Text, a file is generated for each module we've selected. In this example, we'll generate a WEBVTT for the module gcp-video-text-detection.

This assumes a video was already processed through ZVI. If you haven't already done so, please follow these [instructions](https://github.com/link).

In visualizer, find the video asset you want to generate WEBVTT files on and select it. Open it's info pane and navigate down to the Files panel. Navigate to the section for gcp-video-text-detection and copy the ID.
For example:

> assets/l5azb3Pp-lWU7F3J4yIgokvnSbGBH5pc/timeline/gcp-video-text-detection-timeline.json.gz

Generate an APIKey with Assets Read scope.

With both our APIKey and the ID to the file we're basing our WEBVTT on we're now ready to generate it.

In terminal, navigate to the /videoplayer folder. Replace the command with your ID and APIKey path and execute it.

```shell
$ python main.py -f <REPLACE WITH ID> -s https://api.zvi.zorroa.com -k <REPLACE WITH APIKEY PATH>
```

This will generate the file gcp-video-text-detection.webvtt or will be called MODULE-NAME.webvtt if using another module.

Now that we have our WEBVTT file, we can now add it as a track for our video element.
