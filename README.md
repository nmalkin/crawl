website archiver & wpull crawl helper
=====================================

This is a tool meant to simplify archiving websites using
[wpull](https://github.com/chfoo/wpull). In essence, it's a script that calls
wpull with some opinionated settings, which you can find in the `run` file.

It also provides the following extra functionality:

- a domain whitelist
- a regex-based URL blacklist
- completion notification

All of these extra features are optional.


#### Domain whitelist

The crawler will only visit and archive domains whose hostnames appear in the whitelist. The whitelist should be a text file, with each domain on a new file.

Example:

    www.cs.berkeley.edu
    www.berkeley.edu


#### URL blacklist

If you want to avoid archiving certain web content, you can specify the URLs to
skip using regular expressions in a text file, one per line.

Example:

    \.pdf
    \.ppt


#### Completion notification

If you'd like the program to do something once the archival is finished, you can
create a file called `complete.py` with a Python function called
`on_complete` that looks like this:

```python
def on_complete(start_time, end_time, num_urls, bytes_downloaded):
    send_some_sort_of_notification("Your crawl is done, let's celebrate!")
```


Running the program
-------------------

You can run the crawl with [Docker](https://docker.com/) as follows:

```sh
export START_URL="http://example.com" # the URL where your crawl will start
make
```

If you follow this method, you should name your files `whitelist.txt`,
`blacklist.txt`, and `complete.py` and put them in the root of the repository.
If you don't want to use one of these features, or use a different location, you
can modify the command from the Makefile as needed.


### Output and results

The crawled websites are archived into gzipped [WARC
files](https://en.wikipedia.org/wiki/Web_ARChive). The archive is broken up into
files 100 megabytes each. (If you want a different file size, you can change
this easily using the `--warc-max-size` flag.)

If you use the supplied Makefile, the files will be created in a subdirectory
named `out` of the working directory.
