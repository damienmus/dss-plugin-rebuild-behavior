import dataiku
from dataiku.runnables import Runnable
from buildbehavior.utils import set_rebuild_tag, del_rebuild_tag, enable_rebuild_tag

class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return (len(self.config['input_datasets']), 'NONE')

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        client = dataiku.api_client()
        project = client.get_project(self.project_key)
        project_meta = project.get_metadata()
        
        i = 0
        for ds_name in self.config['input_datasets']:
            ds = project.get_dataset(ds_name)
            ds_setting = ds.get_settings()
            if ds_setting.settings['flowOptions']['rebuildBehavior'] != self.config['rebuild_behavior']:
                ds_setting.settings['flowOptions']['rebuildBehavior'] = self.config['rebuild_behavior']
                ds_setting.save()
            i += 1
            progress_callback(i)
        
        if project_meta['customFields'].get('enable_rebuild_tag'):
            status = enable_rebuild_tag(project, project_meta['customFields'].get('strat_rebuild_tag'))
        return 'Done'