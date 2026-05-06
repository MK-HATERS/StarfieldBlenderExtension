import bpy

#initialize sf_shadernode node group
def sf_shadernode_node_group():
    sf_shadernode= bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "SF_ShaderNode")

    #initialize sf_shadernode interface
    #output BSDF
    bsdf_socket = sf_shadernode.interface.new_socket(name="BSDF", socket_type='NodeSocketShader', in_out='OUTPUT', description="")
    bsdf_socket.attribute_domain = 'POINT'

    #output Displacement
    displacement_socket = sf_shadernode.interface.new_socket(name="Displacement", socket_type='NodeSocketVector', in_out='OUTPUT', description="")
    displacement_socket.attribute_domain = 'POINT'

    #input COLOR
    color_socket = sf_shadernode.interface.new_socket(name="COLOR", socket_type='NodeSocketColor', in_out='INPUT', description="")
    color_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    color_socket.attribute_domain = 'POINT'

    #input NORMAL
    normal_socket = sf_shadernode.interface.new_socket(name="NORMAL", socket_type='NodeSocketVector', in_out='INPUT', description="")
    normal_socket.default_value = (0.0, 0.0, 0.0)
    normal_socket.min_value = -3.4028234663852886e+38
    normal_socket.max_value = 3.4028234663852886e+38
    normal_socket.attribute_domain = 'POINT'
    normal_socket.hide_value = True

    #input OPACITY
    opacity_socket = sf_shadernode.interface.new_socket(name="OPACITY", socket_type='NodeSocketFloat', in_out='INPUT', description="")
    opacity_socket.default_value = 1.0
    opacity_socket.min_value = 0.0
    opacity_socket.max_value = 1.0
    opacity_socket.attribute_domain = 'POINT'

    #input METAL
    metal_socket = sf_shadernode.interface.new_socket(name="METAL", socket_type='NodeSocketFloat', in_out='INPUT', description="")
    metal_socket.default_value = 0.0
    metal_socket.min_value = 0.0
    metal_socket.max_value = 1.0
    metal_socket.attribute_domain = 'POINT'

    #input ROUGH
    rough_socket = sf_shadernode.interface.new_socket(name="ROUGH", socket_type='NodeSocketFloat', in_out='INPUT', description="")
    rough_socket.default_value = 0.5
    rough_socket.min_value = 0.0
    rough_socket.max_value = 1.0
    rough_socket.attribute_domain = 'POINT'

    #input AO
    ao_socket = sf_shadernode.interface.new_socket(name="AO", socket_type='NodeSocketFloat', in_out='INPUT', description="")
    ao_socket.default_value = 0.0
    ao_socket.min_value = 0.0
    ao_socket.max_value = 1.0
    ao_socket.attribute_domain = 'POINT'

    #input EMISSIVE
    emissive_socket = sf_shadernode.interface.new_socket(name="EMISSIVE", socket_type='NodeSocketColor', in_out='INPUT', description="")
    emissive_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    emissive_socket.attribute_domain = 'POINT'

    #input HEIGHT
    height_socket = sf_shadernode.interface.new_socket(name="HEIGHT", socket_type='NodeSocketVector', in_out='INPUT', description="")
    height_socket.default_value = (0.0, 0.0, 0.0)
    height_socket.min_value = -3.4028234663852886e+38
    height_socket.max_value = 3.4028234663852886e+38
    height_socket.attribute_domain = 'POINT'

    #input A_TEST_THRESH
    a_test_thresh_socket = sf_shadernode.interface.new_socket(name="A_TEST_THRESH", socket_type='NodeSocketFloat', in_out='INPUT', description="")
    a_test_thresh_socket.default_value = 0.0
    a_test_thresh_socket.min_value = 0.0
    a_test_thresh_socket.max_value = 1.0
    a_test_thresh_socket.attribute_domain = 'POINT'

    #input A_BLEND_CHANNEL
    a_blend_channel_socket = sf_shadernode.interface.new_socket(name="A_BLEND_CHANNEL", socket_type='NodeSocketFloat', in_out='INPUT', description="")
    a_blend_channel_socket.default_value = 0.0
    a_blend_channel_socket.min_value = 0.0
    a_blend_channel_socket.max_value = 4.0
    a_blend_channel_socket.attribute_domain = 'POINT'



    #node Principled BSDF
    principled_bsdf = sf_shadernode.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.distribution = 'GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.2, 0.1)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.0
    # Subsurface IOR
    principled_bsdf.inputs[11].default_value = 1.4
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.0
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (0.0, 0.0, 0.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.03
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.0
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (0.0, 0.0, 0.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 1.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.33

    #node Group Input.001
    group_input_001 = sf_shadernode.nodes.new("NodeGroupInput")

    #node Math
    math = sf_shadernode.nodes.new("ShaderNodeMath")
    math.operation = 'LESS_THAN'
    math.use_clamp = True
    #Value_002
    math.inputs[2].default_value = 0.5

    #node Math.001
    math_001 = sf_shadernode.nodes.new("ShaderNodeMath")
    math_001.operation = 'SUBTRACT'
    #Value
    math_001.inputs[0].default_value = 1.0
    #Value_002
    math_001.inputs[2].default_value = 0.5

    #node Math.002
    math_002 = sf_shadernode.nodes.new("ShaderNodeMath")
    math_002.operation = 'MULTIPLY'
    #Value_002
    math_002.inputs[2].default_value = 0.5

    #node Group Input.002
    group_input_002 = sf_shadernode.nodes.new("NodeGroupInput")

    #node Group Input
    group_input = sf_shadernode.nodes.new("NodeGroupInput")

    #node Mix Shader
    mix = sf_shadernode.nodes.new("ShaderNodeMix")

    #node Invert
    invert = sf_shadernode.nodes.new("ShaderNodeInvert")

    #node Group Output
    group_output = sf_shadernode.nodes.new("NodeGroupOutput")


    #Set locations
    group_output.location = (290.0, 0.0)
    mix.location = (-300.0, 180.0)
    invert.location = (-620.0, 20.0)
    group_input.location = (-860.0, 180.0)
    principled_bsdf.location = (0.0, 0.0)
    group_input_001.location = (-500.0, -80.0)
    math.location = (-780.0, -520.0)
    math_001.location = (-600.0, -520.0)
    math_002.location = (-300.0, -520.0)
    group_input_002.location = (-1220.0, -460.0)

    #Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    mix.width, mix.height = 140.0, 100.0
    invert.width, invert.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    math_002.width, math_002.height = 140.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0

    #initialize sf_shadernode links
    #principled_bsdf.BSDF -> group_output.BSDF
    sf_shadernode.links.new(principled_bsdf.outputs[0], group_output.inputs[0])
    #group_input_001.METAL -> principled_bsdf.Metallic
    sf_shadernode.links.new(group_input_001.outputs[3], principled_bsdf.inputs[6])
    #group_input_001.ROUGH -> principled_bsdf.Roughness
    sf_shadernode.links.new(group_input_001.outputs[4], principled_bsdf.inputs[9])
    #group_input_001.NORMAL -> principled_bsdf.Normal
    sf_shadernode.links.new(group_input_001.outputs[1], principled_bsdf.inputs[22])
    #group_input_001.HEIGHT -> group_output.Displacement
    sf_shadernode.links.new(group_input_001.outputs[7], group_output.inputs[1])
    #group_input.COLOR -> mix.A
    sf_shadernode.links.new(group_input.outputs[0], mix.inputs[1])
    #group_input.AO -> invert.Color
    sf_shadernode.links.new(group_input.outputs[5], invert.inputs[1])
    #invert.Color -> mix.B
    sf_shadernode.links.new(invert.outputs[0], mix.inputs[2])
    #group_input_001.COLOR -> principled_bsdf.Base Color
    sf_shadernode.links.new(group_input_001.outputs[0], principled_bsdf.inputs[0])
    #group_input_002.OPACITY -> math.Value
    sf_shadernode.links.new(group_input_002.outputs[2], math.inputs[0])
    #group_input_002.A_TEST_THRESH -> math.Value
    sf_shadernode.links.new(group_input_002.outputs[8], math.inputs[1])
    #math.Value -> math_001.Value
    sf_shadernode.links.new(math.outputs[0], math_001.inputs[1])
    #math_001.Value -> math_002.Value
    sf_shadernode.links.new(math_001.outputs[0], math_002.inputs[0])
    #group_input_002.OPACITY -> math_002.Value
    sf_shadernode.links.new(group_input_002.outputs[2], math_002.inputs[1])
    #math_002.Value -> principled_bsdf.Alpha
    sf_shadernode.links.new(math_002.outputs[0], principled_bsdf.inputs[21])
    #group_input_001.EMISSIVE -> principled_bsdf.Emission
    sf_shadernode.links.new(group_input_001.outputs[6], principled_bsdf.inputs[19])

def GetMatNode():
	if "SF_ShaderNode" in bpy.data.node_groups:
		return bpy.data.node_groups["SF_ShaderNode"]
	else:
		return sf_shadernode_node_group()

#initialize material node group
def new_mat(mat_name:str):
    mat = bpy.data.materials.new(name = mat_name)
    mat.use_nodes = True
    material = mat.node_tree
    #start with a clean node tree
    for node in material.nodes:
        material.nodes.remove(node)
    #initialize material nodes
    #node Material Output
    material_output = material.nodes.new("ShaderNodeOutputMaterial")
    material_output.target = 'ALL'
    #Thickness
    material_output.inputs[3].default_value = 0.0

    GetMatNode()

    #node OPACITY
    opacity = material.nodes.new("ShaderNodeTexImage")
    opacity.mute = True
    opacity.name = "OPACITY"
    opacity.interpolation = 'Linear'
    opacity.projection = 'FLAT'
    opacity.extension = 'REPEAT'
    #Vector
    opacity.inputs[0].default_value = (0.0, 0.0, 0.0)

    #node METAL
    metal = material.nodes.new("ShaderNodeTexImage")
    metal.mute = True
    metal.name = "METAL"
    metal.interpolation = 'Linear'
    metal.projection = 'FLAT'
    metal.extension = 'REPEAT'
    #Vector
    metal.inputs[0].default_value = (0.0, 0.0, 0.0)

    #node EMISSIVE
    emissive = material.nodes.new("ShaderNodeTexImage")
    emissive.mute = True
    emissive.name = "EMISSIVE"
    emissive.interpolation = 'Linear'
    emissive.projection = 'FLAT'
    emissive.extension = 'REPEAT'
    #Vector
    emissive.inputs[0].default_value = (0.0, 0.0, 0.0)

    #node AO
    ao = material.nodes.new("ShaderNodeTexImage")
    ao.mute = True
    ao.name = "AO"
    ao.interpolation = 'Linear'
    ao.projection = 'FLAT'
    ao.extension = 'REPEAT'
    #Vector
    ao.inputs[0].default_value = (0.0, 0.0, 0.0)

    #node ROUGH
    rough = material.nodes.new("ShaderNodeTexImage")
    rough.mute = True
    rough.name = "ROUGH"
    rough.interpolation = 'Linear'
    rough.projection = 'FLAT'
    rough.extension = 'REPEAT'
    #Vector
    rough.inputs[0].default_value = (0.0, 0.0, 0.0)

    #node COLOR
    color = material.nodes.new("ShaderNodeTexImage")
    color.mute = True
    color.name = "COLOR"
    color.interpolation = 'Linear'
    color.projection = 'FLAT'
    color.extension = 'REPEAT'
    #Vector
    color.inputs[0].default_value = (0.0, 0.0, 0.0)

    #node HEIGHT
    height = material.nodes.new("ShaderNodeTexImage")
    height.mute = True
    height.name = "HEIGHT"
    height.interpolation = 'Linear'
    height.projection = 'FLAT'
    height.extension = 'REPEAT'
    #Vector
    height.inputs[0].default_value = (0.0, 0.0, 0.0)

    #node NORMAL
    normal = material.nodes.new("ShaderNodeTexImage")
    normal.mute = True
    normal.name = "NORMAL"
    normal.interpolation = 'Linear'
    normal.projection = 'FLAT'
    normal.extension = 'REPEAT'
    #Vector
    normal.inputs[0].default_value = (0.0, 0.0, 0.0)

    #node Normal Map
    normal_map = material.nodes.new("ShaderNodeNormalMap")
    normal_map.space = 'TANGENT'
    #Strength
    normal_map.inputs[0].default_value = 1.0

    #node Group
    group = material.nodes.new("ShaderNodeGroup")
    group.node_tree = bpy.data.node_groups["SF_ShaderNode"]
    #Input_8
    group.inputs[7].default_value = (0.0, 0.0, 0.0)
    #Input_9
    group.inputs[8].default_value = 0.0
    #Input_10
    group.inputs[9].default_value = 0.0


    #Set locations
    material_output.location = (300.0, 300.0)
    opacity.location = (-820.0, -100.0)
    metal.location = (-820.0, -300.0)
    emissive.location = (-820.0, -900.0)
    ao.location = (-820.0, -700.0)
    rough.location = (-820.0, -500.0)
    color.location = (-820.0, 300.0)
    height.location = (-820.0, -1100.0)
    normal.location = (-820.0, 100.0)
    normal_map.location = (-340.0, 160.0)
    group.location = (-20.0, 300.0)

    #Set dimensions
    material_output.width, material_output.height = 140.0, 100.0
    opacity.width, opacity.height = 240.0, 100.0
    metal.width, metal.height = 240.0, 100.0
    emissive.width, emissive.height = 240.0, 100.0
    ao.width, ao.height = 240.0, 100.0
    rough.width, rough.height = 240.0, 100.0
    color.width, color.height = 240.0, 100.0
    height.width, height.height = 240.0, 100.0
    normal.width, normal.height = 240.0, 100.0
    normal_map.width, normal_map.height = 150.0, 100.0
    group.width, group.height = 237.6750030517578, 100.0

    #initialize material links
    #group.BSDF -> material_output.Surface
    material.links.new(group.outputs[0], material_output.inputs[0])
    #group.Displacement -> material_output.Displacement
    material.links.new(group.outputs[1], material_output.inputs[2])
    #color.Color -> group.COLOR
    material.links.new(color.outputs[0], group.inputs[0])
    #normal.Color -> normal_map.Color
    material.links.new(normal.outputs[0], normal_map.inputs[1])
    #normal_map.Normal -> group.NORMAL
    material.links.new(normal_map.outputs[0], group.inputs[1])
    #opacity.Color -> group.OPACITY
    material.links.new(opacity.outputs[0], group.inputs[2])
    #ao.Color -> group.AO
    material.links.new(ao.outputs[0], group.inputs[5])
    #rough.Color -> group.ROUGH
    material.links.new(rough.outputs[0], group.inputs[4])
    #metal.Color -> group.METAL
    material.links.new(metal.outputs[0], group.inputs[3])
    #emissive.Color -> group.EMISSIVE
    material.links.new(emissive.outputs[0], group.inputs[6])

    mat.blend_method = 'HASHED'
    mat.use_backface_culling = True

    return mat

