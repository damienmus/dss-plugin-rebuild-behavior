def del_rebuild_tag(sourceTags):
    tags = sourceTags[:]
    [tags.remove(tag) for tag in tags if tag[:8] == 'rebuild:']
    return tags

def set_rebuild_tag(sourceTags, mode):
    tags = sourceTags[:]
    tags = del_rebuild_tag(tags)
    rebuildTag = "rebuild:{}".format(mode.lower())
    tags.append(rebuildTag)
    return tags

def enable_rebuild_tag(project, strat="ALL", progress=False):
    i = 0
    for ds in project.list_datasets('objects'):
        ds_setting = ds.get_settings()
        metadata = ds.get_metadata()
        metadataSource = metadata.copy()
        
        if (strat == "LOCK") and (ds_setting.settings['flowOptions']['rebuildBehavior'] == 'NORMAL'):
            metadata['tags'] = del_rebuild_tag(metadata['tags'])
        else:
            metadata['tags'] = set_rebuild_tag(metadata['tags'], ds_setting.settings['flowOptions']['rebuildBehavior'])

        if metadata["tags"] != metadataSource['tags']:
            ds.set_metadata(metadata)
        i += 1
        if progress:
            progress(i)
            
    return 'Done'
            
def disable_rebuild_tag(project, progress=False):
    i = 0
    for ds in project.list_datasets('objects'):
        metadata = ds.get_metadata()
        metadataSource = metadata.copy() 
        metadata['tags'] = del_rebuild_tag(metadata['tags'])
        if metadata["tags"] != metadataSource['tags']:
            ds.set_metadata(metadata)
        i += 1
        if progress:
            progress(i)
    return 'Done'