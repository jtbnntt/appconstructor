import configparser
import importlib
import logging

LOGGER = logging.getLogger(__name__)
SECTIONS_TO_SKIP = {
    'DEFAULT',
    'global'
}
CONFIG_KEYWORDS = {
    'class',
    'constructor',
    'module'
}


class BadConfigError(Exception):
    pass


class App:
    pass


def construct(config_filename='app.cfg', resources_to_load=None):
    LOGGER.info('Reading config from %s', config_filename)
    config = configparser.ConfigParser()
    config.read(config_filename)

    if resources_to_load is None:
        LOGGER.info('Will load all resources')
        resources_to_load = config
    else:
        LOGGER.info('Will load the following resources:\n%s', '\n'.join(
            resources_to_load))

    app = App()

    LOGGER.info('Loading resources')
    for resource_id in [
            id for id in resources_to_load
            if id not in SECTIONS_TO_SKIP]:
        __load__(app, resource_id, config)
    LOGGER.info('Resources loaded')

    return app


def __load__(app, resource_id, config):
    if not hasattr(app, resource_id):
        LOGGER.info('Loading resource "%s"', resource_id)

        if resource_id not in config:
            raise BadConfigError(
                'Could not find configuration for resource "{}"'.format(
                    resource_id))

        resource_config = config[resource_id]

        if 'constructor' in resource_config:
            constructor_name = resource_config['constructor']
            module_name = constructor_name[:constructor_name.rfind('.')]
            class_name = constructor_name[constructor_name.rfind('.') + 1:]
        elif 'module' in resource_config and 'class' in resource_config:
            module_name = resource_config['module']
            class_name = resource_config['class']
        else:
            raise BadConfigError(
                'Resource "{}" must specify either "constructor" '
                'or "module" and "class"'.format(resource_id))

        module = importlib.import_module(module_name)
        constructor = getattr(module, class_name)

        params = {}

        for param in resource_config:
            if param in CONFIG_KEYWORDS:
                continue

            value = resource_config[param]

            if value.startswith('global:'):
                reference = value[len('global:'):]
                LOGGER.debug('Loading global property "%s"', reference)

                if reference not in config['global']:
                    raise BadConfigError(
                        'Could not find global property "{}" '
                        'required by resource "{}"'.format(
                            reference, resource_id))

                params[param] = config['global'][reference]
            elif value.startswith('ref:'):
                dependency_id = value[len('ref:'):]
                LOGGER.debug(
                    'Resource "%s" does not exist, must load',
                    dependency_id)
                if not hasattr(app, dependency_id):
                    __load__(app, dependency_id, config)
                else:
                    LOGGER.debug('Resource "%s" exists', dependency_id)

                if not hasattr(app, dependency_id):
                    raise BadConfigError(
                        'Could not find referenced resource "{}" required '
                        'by resource "{}"'.format(dependency_id, resource_id))

                params[param] = getattr(app, dependency_id)
            elif value.startswith('string:'):
                LOGGER.debug('Loading property "%s"', param)
                params[param] = value[len('string:'):]
            else:
                LOGGER.debug('Loading property "%s"', param)
                params[param] = value

        setattr(app, resource_id, constructor(**params))
        LOGGER.info('Finished loading resource "%s"', resource_id)
