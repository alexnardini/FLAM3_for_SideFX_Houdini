#   Title:      FLAM3HUSD Custom node info
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2021 F stands for liFe

import hou

# Get some HDA infos from the HDA module
FLAM3H_NODE_TYPE_NAME_CATEGORY = 'alexnardini::Lop/FLAM3HUSD'
nodetype = hou.nodeType(FLAM3H_NODE_TYPE_NAME_CATEGORY)
__version__ = nodetype.hdaModule().__version__

addLabeledText("Description", "Render FLAM3H™ fractal Flames in Solaris using Karma")
addLabeledText("Version", __version__)
addLabeledText("Copyright", "© 2023 F stands for liFe (made in Italy)")
addLabeledText("License", "GPL")