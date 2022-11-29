import dataiku
from dataiku.runnables import Runnable
from buildbehavior.utils import enable_rebuild_tag, disable_rebuild_tag

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
        return (len(dataiku.api_client().get_project(self.project_key).list_datasets('objects')), 'NONE')

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        client = dataiku.api_client()
        project = client.get_project(self.project_key)
        project_meta = project.get_metadata()
        
        if self.config['rebuild_tag'] != project_meta['customFields'].get('enable_rebuild_tag'):
            project_meta['customFields']['enable_rebuild_tag'] = self.config['rebuild_tag']
            project_meta['customFields']['strat_rebuild_tag'] = self.config['strat_tag']
            project.set_metadata(project_meta)
            
        if self.config['rebuild_tag'] == True:
            status = enable_rebuild_tag(project, strat=self.config['strat_tag'], progress=progress_callback)
        else:
            status = disable_rebuild_tag(project, progress=progress_callback)
        
        return 'Done'
        