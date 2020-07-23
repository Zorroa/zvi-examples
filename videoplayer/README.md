# Generate WEBVTT caption files for web video players.

## Prerequisites:

- HTML5
- Javascript
- Python
- Video Processed through ZVI

Download the contents in https://github.com/Zorroa/zvi-examples/tree/master/videoplayer

This example demonstrates how we can generate WEBVTT caption files to play alongside an HTML5 video player. After processing video assets with `Google's Video Intelligence` and `Google Speech-To-Text`, a file is generated for each module we've selected. In this example, we'll generate a WEBVTT for the module `gcp-video-text-detection`.

This assumes a video was already processed through ZVI. If you haven't already done so, please follow these [instructions](https://github.com/link).

In visualizer, find the video asset you want to generate WEBVTT files on and select it. Open it's info pane and navigate down to the Files panel. Navigate to the section for `gcp-video-text-detection` and copy the ID.
For example:

> `assets/l5azb3Pp-lWU7F3J4yIgokvnSbGBH5pc/timeline/gcp-video-text-detection-timeline.json.gz`

Generate an APIKey with Assets Read scope.

With both our APIKey and the ID to the file we're basing our WEBVTT on we're now ready to generate it.

In terminal, navigate to the /videoplayer folder. Replace the command with your ID and APIKey path and execute it.

```shell
$ python main.py -f <REPLACE WITH FILE ID> -s https://api.zvi.zorroa.com -k <REPLACE WITH APIKEY PATH>
```

This will generate the file gcp-video-text-detection.webvtt or will be called MODULE-NAME.webvtt if using another module.

Now that we have our WEBVTT file, we can now add it as a track for our video element.

```html
<video
  id="video"
  controls
  preload="metadata"
  style="width: 100%; margin-top: 30px;"
>
  <track
    id="textDetection"
    label="gcp-video-text-detection"
    kind="metadata"
    srclang="en"
    src="gcp-video-text-detection.webvtt"
    default
  />
</video>
```

The `index.html` file includes a video player with the `gcp-video-text-detection.webvtt` track. During video playback, it will trigger our javascript `textDetection.oncuechange` function each time it passes a start point in our `gcp-video-text-detection.webvtt` file. From here we can use data from the file however we choose.

In the `index.html` file, information is displayed in the Text Detection panel and each text generate from ZVI's analysis is made clickable and will navigate you to that portion of the video.

You can try it out by navigating to the videoplayer folder and excuting this command in terminal and then open a browser to http://localhost:8000

```shell
$ python -m SimpleHTTPServer 8000
```

Processing video assets through ZVI makes it easy to generate contextual metadata for each frame of our video. This can be expanded upon by generating audio transcriptions for `caption files`, tracks for `logos`, `objects`, `explicit content` and even `face detection`. We can then use tracks to notify us when these elements appear on our video and even skip to a section of the video using search terms.
