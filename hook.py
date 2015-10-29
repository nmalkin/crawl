# This file contains custom hooks for wpull with the following functionality:
# - a domain whitelist
# - a regex-based URL blacklist
# - completion notification

import os
import re

WHITELIST_LOCATION = os.environ.get('WHITELIST', '/data/whitelist.txt')
BLACKLIST_LOCATION = os.environ.get('BLACKLIST', '/data/blacklist.txt')

def load_whitelist():
    """
    Load whitelist of allowed domains
    """
    whitelist = {}
    if os.path.isfile(WHITELIST_LOCATION):
        with open(WHITELIST_LOCATION, 'r') as f:
            lines = f.readlines()
            whitelist = {line.rstrip() for line in lines}
    print('Registered whitelist with %d entries' % len(whitelist))
    return whitelist

def load_blacklist():
    """
    Load regular expressions to exclude URLs
    """
    blacklist = {}
    if os.path.isfile(BLACKLIST_LOCATION):
        with open(BLACKLIST_LOCATION, 'r') as f:
            lines = f.readlines()
            blacklist = {re.compile(line.rstrip()) for line in lines}
    print('Registered blacklist with %d entries' % len(blacklist))
    return blacklist

def validate_urls():
    """
    Apply rules for URL inclusion/exclusion
    """
    whitelist = load_whitelist()
    blacklist = load_blacklist()

    def accept_url(url_info, record_info, verdict, reasons):
        # If our whitelist isn't empty, only allow domains it includes
        if len(whitelist) > 0 and url_info['hostname'] not in whitelist:
            return False

        # Exclude any URL that matches the pattern in the blacklist
        for rule in blacklist:
            if rule.search(url_info['url']):
                return False

        # Otherwise, defer to wpull's decision
        return verdict

    wpull_hook.callbacks.accept_url = accept_url

def completion_hook():
    """
    Trigger an optional hook when the crawl completes

    For the hook to be triggered, the script's original working directory must
    contain a file named "complete.py" (or a module of the same name) with a
    function named "on_complete" defined.

    on_complete must have the following signature:
        on_complete(start_time, end_time, num_urls, bytes_downloaded)
    """
    if os.path.isfile('../complete.py'):
        import sys
        sys.path.append('..')
        import complete

        wpull_hook.callbacks.finishing_statistics = complete.on_complete

        print('Registered completion hook')


validate_urls()
completion_hook()
