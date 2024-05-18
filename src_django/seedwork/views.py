# noinspection PyUnresolvedReferences
class ListSerializerMixin:
    """
    Add specific serializer for `List` action
    """
    serializer_list_class = None

    def get_serializer_list_class(self):
        assert self.serializer_list_class, (
            '{} must contain `serializer_list_class` attribute'.format(self.__class__.__name__)
        )

        return self.serializer_list_class

    def get_serializer_class(self):
        if self.action == 'list':
            return self.get_serializer_list_class()

        return super().get_serializer_class()


# noinspection PyUnresolvedReferences
class RetrieveSerializerMixin:
    """
    Add specific serializer for `Retrieve` action
    """
    serializer_retrieve_class = None

    def get_serializer_retrieve_class(self):
        assert self.serializer_retrieve_class, (
            '{} must contain `serializer_retrieve_class` attribute'.format(self.__class__.__name__)
        )

        return self.serializer_retrieve_class

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.get_serializer_retrieve_class()

        return super().get_serializer_class()


# noinspection PyUnresolvedReferences
class CreateSerializerMixin:
    """
    Add specific serializer for `Create` action
    """
    serializer_create_class = None

    def get_serializer_create_class(self):
        assert self.serializer_create_class, (
            '{} must contain `serializer_create_class` attribute'.format(self.__class__.__name__)
        )

        return self.serializer_create_class

    def get_serializer_class(self):
        if self.action == 'create':
            return self.get_serializer_create_class()

        return super().get_serializer_class()


# noinspection PyUnresolvedReferences
class UpdateSerializerMixin:
    """
    Add specific serializer for `Update` action
    """
    serializer_update_class = None

    def get_serializer_update_class(self):
        assert self.serializer_update_class, (
            '{} must contain `serializer_update_class` attribute'.format(self.__class__.__name__)
        )

        return self.serializer_update_class

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return self.get_serializer_update_class()

        return super().get_serializer_class()


# noinspection PyUnresolvedReferences
class ChangePermissionMixin:
    """
    Add specific permission_classes for `['create', 'update', 'destroy']` actions
    """
    change_permission_classes = None

    def get_change_permission_classes(self):
        assert self.change_permission_classes, (
            '{} must contain `change_permission_classes` attribute'.format(self.__class__.__name__)
        )
        return [permission() for permission in self.change_permission_classes]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return self.get_change_permission_classes()
        return super().get_permissions()


# noinspection PyUnresolvedReferences
class ViewPermissionMixin:
    """
    Add specific permission_classes for `list and retrieve` actions
    """
    view_permission_classes = None

    def get_view_permission_classes(self):
        assert self.view_permission_classes, (
            '{} must contain `view_permission_classes` attribute'.format(self.__class__.__name__)
        )
        return [permission() for permission in self.view_permission_classes]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return self.get_view_permission_classes()
        return super().get_permissions()


# noinspection PyUnresolvedReferences
class DestroyPermissionMixin:
    """
    Add specific permission_classes for `destroy` actions
    """
    destroy_permission_classes = None

    def get_destroy_permission_classes(self):
        assert self.destroy_permission_classes, (
            '{} must contain `destroy_permission_classes` attribute'.format(self.__class__.__name__)
        )
        return [permission() for permission in self.destroy_permission_classes]

    def get_permissions(self):
        if self.action == 'destroy':
            return self.get_destroy_permission_classes()
        return super().get_permissions()
