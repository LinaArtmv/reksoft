from reksoft.urls import Url
from views import (MassDelete, ResourceDetail, ResourceType,
                   ResourceTypeDetail, Resourse)

urlpatterns = [
    Url('^/resources$', Resourse),
    Url('^/types$', ResourceType),
    Url('^/type/(?P<type_id>\d+)$', ResourceTypeDetail),
    Url('^/resource/(?P<resource_id>\d+)$', ResourceDetail),
    Url('^/delete$', MassDelete)
]
