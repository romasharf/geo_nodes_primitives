bl_info = {
    "name": "GeoNodes Primitives (3dsmax style)",
    "author": "romasharf",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a procedural Cylinder (3dsmax style)",
    "warning": "",
    "doc_url": "https://docs.blender.org/api/current/",
    "category": "Add Mesh",
}


import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add

# Function adds a cylinder with GeoNodes modifier and the handles to change number of sides and other stuff at any moment
# Thanks to guys from blender.stackexchange.com for parts of code (especially to https://blender.stackexchange.com/users/109459/x-y)
def geo_nodes_cylinder():

    obj = bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    # add GeometryNodes modifier
    bpy.ops.object.modifier_add(type='NODES')
    bpy.ops.node.new_geometry_node_group_assign()
    # access active object node_group
    node_group = bpy.context.object.modifiers[0].node_group

    print(node_group.name)

    # add node
    nodes = node_group.nodes
    geo_cyl = nodes.new(type="GeometryNodeMeshCylinder")
    geo_cyl.inputs[0].default_value = 8

    #geo_cyl.location.x -= 50
    #geo_cyl.location.y -= 50

    # connect
    links = node_group.links
    links.remove(links[0])
    links.new(nodes["Group Input"].outputs[1], geo_cyl.inputs[0])
    links.new(geo_cyl.outputs[0], nodes["Group Output"].inputs[0])

    links.new(nodes["Group Input"].outputs[2], geo_cyl.inputs[1])
    links.new(nodes["Group Input"].outputs[3], geo_cyl.inputs[2])
    links.new(nodes["Group Input"].outputs[4], geo_cyl.inputs[3])
    links.new(nodes["Group Input"].outputs[5], geo_cyl.inputs[4])


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        geo_nodes_cylinder()

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="GeoNodes Cylinder",
        icon='MESH_CYLINDER')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
