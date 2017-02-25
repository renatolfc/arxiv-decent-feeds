# arXiv decent feeds

Ever wanted to follow arXiv feeds on Slack, but try as you might slackbot was
unable to show arXiv updates?

Wonder no more! arXiv decent feeds reads and converts arXiv RSS feeds to valid
RSS 2.0 feeds that slackbot will (hopefully) read!

## Installation

```
pip install https://github.com/trovao/arxiv-decent-feeds/zipball/master
```

## Usage

### Adding a feed

```
usage: arxivdf add [-h] url target_file

positional arguments:
  url
  target_file

optional arguments:
  -h, --help   show this help message and exit
```

For example, to add the `cs.LG` (Computer Science Learning) feed, one could do:

```
arxivdf add http://export.arxiv.org/rss/cs.LG\?version\=2.0 cs.LG.rss
```

### Fetching updates

```
arxivdf update
```

### Generating feeds

If you added `cs.LG` as show above, after you can call the command `arxivdf
generate` your feed will be saved to the file `cs.LG.rss` in the current
directory.

### Periodically updating and generating feeds

Just set up a cron job with to do that.

