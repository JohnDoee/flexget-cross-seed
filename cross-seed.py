from __future__ import unicode_literals, division, absolute_import
import logging

import glob
import os
import re

from six import string_types

from flexget import plugin
from flexget.event import event
from flexget.config_schema import one_or_more

log = logging.getLogger('cross-seed')


class FilterCrossSeed(object):
    """
        Accepts entries found in a given glob path
        Example::
          cross-seed: /storage/tvseries/*/*
    """

    schema = one_or_more({'type': 'string'})

    def prepare_config(self, config):
        # If only a single path is passed turn it into a 1 element list
        if isinstance(config, string_types):
            config = [config]
        return config

    def normalize_name(self, name):
        return re.sub(r'([._ -]+)', ' ', name.lower())

    @plugin.priority(-1)
    def on_task_filter(self, task, config):
        if not task.undecided:
            log.debug('No accepted entries, not scanning for cross seeds.')
            return
        log.verbose('Scanning path(s) for existing files and folders.')
        config = self.prepare_config(config)
        existing_entries = {}
        for folder in config:
            folder = os.path.expanduser(folder)
            for f in glob.glob(folder):
                normalized_name = self.normalize_name(os.path.split(f)[1])
                existing_entries[normalized_name] = f


        for entry in task.undecided:
            # priority is: filename, location (filename only), title
            names = [self.normalize_name(x) for x in [entry.get('filename'), entry.get('location'), entry.get('title')] if x]

            for name in names:
                if name in existing_entries:
                    log.debug('Found %s in %s' % (name, existing_entries[name]))
                    entry.accept('exists in %s' % existing_entries[name])
                    break


@event('plugin.register')
def register_plugin():
    plugin.register(FilterCrossSeed, 'cross-seed', api_ver=2)
