from dataclasses import dataclass
from typing import List

from dcs.drawing.drawing import Drawing, LineStyle, Rgba
from dcs.drawing.icon import Icon
from dcs.drawing.line import LineDrawing, LineMode
from dcs.drawing.polygon import PolygonMode, Circle, Rectangle, Oval, FreeFormPolygon, Arrow
from dcs.drawing.text_box import TextBox
from dcs.mapping import Point

@dataclass()
class Layer():
    visible: bool
    name: str
    objects: List[Drawing]

    def load_from_dict(self, data):
        self.visible = data["visible"]
        self.name = data["name"]

        for object_index in sorted(data["objects"].keys()):
            object_data = data["objects"][object_index]
            #print("drawing data", object_data)
            object = self.load_drawing_from_data(object_data)
            #print("OBJECT IS", object)
            self.objects.append(object)

    def dict(self):
        d = {}
        d["visible"] = self.visible
        d["name"] = self.name

        d["objects"] = {}
        i = 1
        for object in self.objects:
            d["objects"][i] = object.dict()
            i += 1

        return d

    def load_drawing_from_data(self, object_data: dict) -> Drawing:
        # TODO: Maybe move this stuff into the classes and load_from_dict?

        prim_type = object_data["primitiveType"]
        visible = object_data["visible"]
        color = Rgba.from_color_string(object_data["colorString"])
        layer_name = object_data["layerName"]
        name = object_data["name"]
        mapX: float = object_data["mapX"]
        mapY: float = object_data["mapY"]
        position = Point(mapX, mapY)

        if prim_type == "Line":
            closed = object_data["closed"]
            line_thickness = object_data["thickness"]
            line_style = LineStyle(object_data["style"])
            line_mode = LineMode(object_data["lineMode"])
            points = self.load_points_from_data(object_data["points"])
            return LineDrawing(visible, position, name, color, layer_name, closed, line_thickness, line_style, line_mode, points)
        elif prim_type == "Icon":
            file = object_data["file"]
            scale = object_data["scale"]
            angle = object_data["angle"]
            return Icon(visible, position, name, color, layer_name, file, scale, angle)
        elif prim_type == "Polygon":
            polygon_mode = PolygonMode(object_data["polygonMode"])
            fill = Rgba.from_color_string(object_data["fillColorString"])
            line_thickness = object_data["thickness"]
            line_style = LineStyle(object_data["style"])

            if polygon_mode == PolygonMode.Circle:
                radius = object_data["radius"]
                return Circle(visible, position, name, color, layer_name, fill, line_thickness, line_style, radius)
            elif polygon_mode == PolygonMode.Oval:
                radius1 = object_data["r1"]
                radius2 = object_data["r2"]
                angle = object_data["angle"]
                return Oval(visible, position, name, color, layer_name, fill, line_thickness, line_style, radius1, radius2, angle)
            elif polygon_mode == PolygonMode.Rectangle:
                width = object_data["width"]
                height = object_data["height"]
                angle = object_data["angle"]
                return Rectangle(visible, position, name, color, layer_name, fill, line_thickness, line_style, width, height, angle)
            elif polygon_mode == PolygonMode.Free:
                points = self.load_points_from_data(object_data["points"])
                return FreeFormPolygon(visible, position, name, color, layer_name, fill, line_thickness, line_style, points)
            elif polygon_mode == PolygonMode.Arrow:
                angle = object_data["angle"]
                length = object_data["length"]
                points = self.load_points_from_data(object_data["points"])
                return Arrow(visible, position, name, color, layer_name, fill, line_thickness, line_style, length, angle, points)
        elif prim_type == "TextBox":
            text = object_data["text"]
            font_size = object_data["fontSize"]
            font = object_data["font"]
            border_thickness = object_data["borderThickness"]
            fill = Rgba.from_color_string(object_data["fillColorString"])
            angle = object_data["angle"]
            return TextBox(visible, position, name, color, layer_name, text, font_size, font, border_thickness, fill, angle)

    def load_points_from_data(self, points_data) -> List[Point]:
        points: List[Point] = []
        for point_index in sorted(points_data.keys()):
            x = points_data[point_index]["x"]
            y = points_data[point_index]["y"]
            points.append(Point(x, y))
        return points


    def add_drawing(self, drawing: Drawing):
        self.objects.append(drawing)

    def remove_drawing(name: str):
        raise NotImplementedError()