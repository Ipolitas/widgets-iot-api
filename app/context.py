from .models import Widget, ConnectedRel


class WidgetContext:
    @classmethod
    async def get_widget(cls, serial_number: str) -> Widget:
        widget: Widget = Widget.nodes.get(serial_number=serial_number)
        return widget

    @classmethod
    async def add_widget(cls, name: str, ports: str) -> Widget:
        widget = Widget(
            name=name,
            ports=ports
        )
        widget.save()
        return widget

    @classmethod
    async def remove_widget(cls, serial_number: str) -> None:
        widget: Widget = cls.get_widget()
        widget.delete()

    @classmethod
    async def connect_widgets(cls, serial_number: str, target_serial_number: str, port: str) -> ConnectedRel:
        # TODO: await in paralell or merge to single query
        source: Widget = await cls.get_widget(serial_number)
        target: Widget = await cls.get_widget(target_serial_number)

        source.validate_on_connect(port=port)
        target.validate_on_connect(port=port)

        rel = source.conn_widgets.connect(target, {"port": port})
        return rel
