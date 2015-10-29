# This file contains custom hooks for wpull with the following functionality:
# - a domain whitelist
# - completion notification

### WHITELIST ###
# Only allow the crawling of URLs matching a specified whitelist

import os
WHITELIST_LOCATION = os.environ.get('DOMAIN_WHITELIST', '/data/whitelist.txt')

# Load whitelist
whitelist = {}
if os.path.isfile(WHITELIST_LOCATION):
    with open(WHITELIST_LOCATION, 'r') as f:
        lines = f.readlines()
        whitelist = {line.rstrip() for line in lines}

# Allow through only URLs whose hostnames are found in the whitelist
def accept_url(url_info, record_info, verdict, reasons):
    if url_info['hostname'] in whitelist:
        return True
    else:
        return verdict

# Only validate URLs if our whitelist isn't empty
if len(whitelist) > 0:
    print('Running with whitelist: %s' % whitelist)
    wpull_hook.callbacks.accept_url = accept_url
else:
    print('Running without a whitelist')


### NOTIFICATION ###
# Provide a notification once the program completes
if os.path.isfile('../complete.py'):
    print('Registered completion hook')

    import sys
    sys.path.append('..')
    import complete

    # on_complete will be called with the following arguments:
    #   on_complete(start_time, end_time, num_urls, bytes_downloaded)
    wpull_hook.callbacks.finishing_statistics = complete.on_complete

