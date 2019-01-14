import configparser
import importlib
import logging

LOGGER = logging.getLogger(__name__)


class App:
    ...


def construct(config_filename='app.cfg', resources_to_load=None):
    LOGGER.info('Reading config from %s', config_filename)
    config = configparser.ConfigParser()
    config.read(config_filename)

    if resources_to_load is None:
        LOGGER.info('Will load all resources')
        resources_to_load = config
    else:
        LOGGER.info('Will load the following resources:\n%s', '\n'.join((resources_to_load)))

    app = App()
    LOGGER.info('Loading resources')
    for resource_id in [id for id in resources_to_load if id not in {'DEFAULT', 'global'}]:
        __load__(app, resource_id, config)
    LOGGER.info('Resources loaded')

    return app

def __load__(app, resource_id, config):
    if not hasattr(app, resource_id):
        LOGGER.info('Loading resource "%s"', resource_id)
        params = {}
        module = importlib.import_module(config[resource_id].pop('module'))
        clz = getattr(module, config[resource_id].pop('class'))
        for param in config[resource_id]:
            value = config[resource_id][param]
            if value.startswith('global:'):
                reference = value[len('global:'):]
                LOGGER.debug('Loading global property "%s"', reference)
                params[param] = config['global'][reference]
            elif value.startswith('ref:'):
                dependency_id = value[len('ref:'):]
                LOGGER.debug('Resource "%s" does not exist, must load', dependency_id)
                if not hasattr(app, dependency_id):
                    __load__(app, dependency_id, config)
                else:
                    LOGGER.debug('Resource "%s" exists', dependency_id)
                params[param] = getattr(app, dependency_id)
            elif value.startswith('string:'):
                LOGGER.debug('Loading property "%s"', param)
                params[param] = value[len('string:'):]
            else:
                LOGGER.debug('Loading property "%s"', param)
                params[param] = value
        setattr(app, resource_id, clz(**params))
        LOGGER.info('Finished loading resource "%s"', resource_id)
