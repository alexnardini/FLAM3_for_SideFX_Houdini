
# ███████╗██╗░░░░░░█████╗░███╗░░░███╗██████╗░██╗░░██╗██╗░░░██╗░██████╗██████╗░
# ██╔════╝██║░░░░░██╔══██╗████╗░████║╚════██╗██║░░██║██║░░░██║██╔════╝██╔══██╗
# █████╗░░██║░░░░░███████║██╔████╔██║░█████╔╝███████║██║░░░██║╚█████╗░██║░░██║
# ██╔══╝░░██║░░░░░██╔══██║██║╚██╔╝██║░╚═══██╗██╔══██║██║░░░██║░╚═══██╗██║░░██║
# ██║░░░░░███████╗██║░░██║██║░╚═╝░██║██████╔╝██║░░██║╚██████╔╝██████╔╝██████╔╝
# ╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═════╝░
#
#   Title:      FLAM3H™USD Custom node info
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

from hou import nodeType as hou_nodeType

# Get some HDA infos from the HDA module
FLAM3HUSD_NODE_TYPE_NAME_CATEGORY = 'alexnardini::Lop/FLAM3HUSD'
nodetype = hou_nodeType(FLAM3HUSD_NODE_TYPE_NAME_CATEGORY)
__version__ = nodetype.hdaModule().__version__
__status__  = nodetype.hdaModule().__status__
__license__ = nodetype.hdaModule().flam3usd.__license__
__copyright__ = nodetype.hdaModule().flam3usd.__copyright__

# Build custom node info
addLabeledText("Description", "Render FLAM3H™ fractal Flames in Solaris using Karma")
addLabeledText("Copyright", f"{__copyright__} (made in Italy)")
addLabeledText("Version", f"{__version__} - {__status__}")
addLabeledText("Lic", __license__)
