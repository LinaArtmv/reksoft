from reksoft.request import Request
from reksoft.response import Response
from reksoft.view import View


class ResourceType(View):
    """Методы List, Create для типов ресурса."""

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = self.get_all_type()
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        name = request.POST.get('name')
        max_speed = request.POST.get('max_speed')
        body = self.create_resource_type(name, max_speed)
        return Response(request, body=body)


class Resourse(View):
    """Методы List, Create для ресурсов."""

    def get(self, request: Request, *args, **kwargs) -> Response:
        if request.GET_QUERY.get('type'):
            type = request.GET_QUERY.get('type')
            body = self.get_all_resources_type(type)
            return Response(request, body=body)
        body = self.get_all_resources()
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        name = request.POST.get('name')
        current_speed = request.POST.get('current_speed')
        type_id = request.POST.get('type_id')
        body = self.create_resource(name, current_speed, type_id)
        return Response(request, body=body)


class ResourceTypeDetail(View):
    """Методы Retrieve, Update, Delete для типов ресурсов.."""

    def get(self, request: Request, *args, **kwargs) -> Response:
        type_id = request.GET.get('id')
        body = self.get_id_type(id=type_id)
        return Response(request, body=body)

    def put(self, request: Request, *args, **kwargs) -> Response:
        type_id = request.GET.get('id')
        name = request.POST.get('name')
        max_speed = request.POST.get('max_speed')
        body = self.update_resource_type(id=type_id,
                                         name=name,
                                         max_speed=max_speed)
        return Response(request, body=body)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        type_id = request.GET.get('id')
        body = self.delete_resource_type(id=type_id)
        return Response(request, body=body)


class ResourceDetail(View):
    """Методы Retrieve, Update, Delete для ресурсов."""

    def get(self, request: Request, *args, **kwargs) -> Response:
        resource_id = request.GET.get('id')
        body = self.get_id_resource(id=resource_id)
        return Response(request, body=body)

    def put(self, request: Request, *args, **kwargs) -> Response:
        id = request.GET.get('id')
        name = request.POST.get('name')
        current_speed = request.POST.get('current_speed')
        type_id = request.POST.get('type_id')
        body = self.update_resource(id=id,
                                    name=name,
                                    current_speed=current_speed,
                                    type_id=type_id)
        return Response(request, body=body)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        type_id = request.GET.get('id')
        body = self.delete_resource(id=type_id)
        return Response(request, body=body)


class MassDelete(View):
    """Массовое удаление для типов и ресурсов.."""

    def delete(self, request: Request, *args, **kwargs) -> Response:
        if request.POST.get('resources'):
            id_list: list = request.POST.get('resources')
            self.mass_delete_resources(id_list)
        elif request.POST.get('types'):
            id_list: list = request.POST.get('types')
            self.mass_delete_types(id_list)
        return Response(request, body='Успешное удаление')
