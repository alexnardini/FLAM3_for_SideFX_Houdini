#   Title:      FLAM3H™ Custom node info
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2021 F stands for liFe

from hou import nodeType as hou_nodeType

# Get some HDA infos from the HDA module
FLAM3H_NODE_TYPE_NAME_CATEGORY = 'alexnardini::Sop/FLAM3H'
nodetype = hou_nodeType(FLAM3H_NODE_TYPE_NAME_CATEGORY)
__version__ = nodetype.hdaModule().__version__
__status__  = nodetype.hdaModule().__status__
__license__ = nodetype.hdaModule().flam3.__license__
__copyright__ = nodetype.hdaModule().flam3.__copyright__

# Build custom node info
addLabeledText("Description", "The Fractal Flame Algorithm: FLAM3 - Create fractal art in Houdini")
addLabeledText("Copyright", f"{__copyright__} (made in Italy)")
addLabeledText("Version", f"{__version__} - {__status__}")
addLabeledText("Lic", __license__)

