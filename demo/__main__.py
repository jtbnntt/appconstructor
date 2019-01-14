import os
import logging

from appconstructor import construct

logging.basicConfig(level=logging.DEBUG)

config_filename = os.path.join(os.path.dirname(__file__), 'app.sample.cfg')

# Construct all resources (default)
app1 = construct(config_filename=config_filename)
print('service exists: ', hasattr(app1, 'service'))
print('service.dependency:', app1.service.dependency)
print('service.value:', app1.service.value)
print('service.global_value:', app1.service.global_value)
print('other service exists: ', hasattr(app1, 'other_service'))
print('other_service.value:', app1.other_service.value)
print('another_service exists:', hasattr(app1, 'another_service'))
print('another_service.value:', app1.another_service.value)
print()

# Construct only requested resources and dependencies
app2 = construct(config_filename=config_filename, resources_to_load={'service'})
print('service exists: ', hasattr(app2, 'service'))
print('service.dependency:', app2.service.dependency)
print('service.value:', app2.service.value)
print('service.global_value:', app2.service.global_value)
print('other service exists: ', hasattr(app2, 'other_service'))
print('other_service.value:', app2.other_service.value)
print('another_service exists:', hasattr(app2, 'another_service'))
print()

# Construct only requested resource without dependencies
app3 = construct(config_filename=config_filename, resources_to_load={'other_service'})
print('service exists: ', hasattr(app3, 'service'))
print('other service exists: ', hasattr(app3, 'other_service'))
print('other_service.value:', app3.other_service.value)
print('another_service exists:', hasattr(app3, 'another_service'))
