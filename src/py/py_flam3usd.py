from platform import python_version
from datetime import datetime
import hou


#   Tested on PYTHON v3.7.13(H19) and PYTHON v3.9.10(H19.5)

#   Title:      SideFX Houdini FLAM3HUSD
#   Author:     Alessandro Nardini
#   date:       September 2023, Last revised September 2023
#
#   Name:       PY_FLAM3USD "PYTHON"
#
#   Comment:    Simple utility node to quickly setup
#               fractal flames point clouds in Solaris for previews.
#
#               Everything is then glued together inside Houdini.


FLAM3HUSD_VERSION = '0.0.2'

MSG_FLAM3HUSDABOUT = 'flam3husdabout_msg'



def autoSetRenderer_on_create(self: hou.Node) -> None:
    for view in getSceneViewers():
        cr = hou.SceneViewer.currentHydraRenderer(view)
        if "Houdini" in cr:
            self.setParms({"rndtype": 0}) # type: ignore
        elif "Karma" in cr:
            self.setParms({"rndtype": 1}) # type: ignore
        elif "Storm" in cr:
            self.setParms({"rndtype": 2}) # type: ignore
            

def flam3USD_on_create(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """
    # Set initial node color
    node = kwargs['node']
    node.setColor(hou.Color((0.165,0.165,0.165)))
    # Set renderer
    autoSetRenderer_on_create(node)
    # Set about box
    flam3USD_about_msg(node)

    # INITIALIZE ffx_CS
    try:
        hou.session.flam3_CS # type: ignore
    except:
        hou.session.flam3_CS = [] # type: ignore
    
    
def getSceneViewers() -> list:
    """
    Returns:
        list: [return a list of open scene viewers]
    """    
    views = hou.ui.paneTabs() # type: ignore
    viewers = []
    for v in views:
        if isinstance(v, hou.SceneViewer):
            viewers.append(v)
    return viewers


def colorSchemeDark(self: hou.Node) -> None:
    try:
        module_test = hou.session.flam3_CS # type: ignore
    except:
        hou.session.flam3_CS = [] # type: ignore

    count = 0
    viewers_col = []

    setprm = self.parm("setdark").eval()
    Light = hou.viewportColorScheme.Light # type: ignore
    Grey  = hou.viewportColorScheme.Grey # type: ignore
    Dark  = hou.viewportColorScheme.Dark # type: ignore

    for view in getSceneViewers():

        settings = view.curViewport().settings()
        col = settings.colorScheme()
        viewers_col.append(col)
        try:
            idx_test = hou.session.flam3_CS[count] # type: ignore
        except:
            if len(hou.session.flam3_CS) > 0: # type: ignore
                hou.session.flam3_CS.append(viewers_col) # type: ignore
            else:
                hou.session.flam3_CS = [] # type: ignore
                hou.session.flam3_CS.append(viewers_col) # type: ignore

        if setprm:
            if len(hou.session.flam3_CS) == 0: # type: ignore
                if col == Light or col == Grey:
                    settings.setColorScheme(Dark)
            else:
                if col == Light or col == Grey:
                    settings.setColorScheme(Dark)
                elif col == Dark and hou.session.flam3_CS[count] != Dark: # type: ignore
                    if hou.session.flam3_CS[count] == Light: # type: ignore
                        settings.setColorScheme(Light)
                    elif hou.session.flam3_CS[count] == Grey: # type: ignore
                        settings.setColorScheme(Grey)

        else:
            if col == Dark and hou.session.flam3_CS[count] != Dark: # type: ignore
                if hou.session.flam3_CS[count] == Light: # type: ignore
                    settings.setColorScheme(Light)
                elif hou.session.flam3_CS[count] == Grey: # type: ignore
                    settings.setColorScheme(Grey)
        count += 1
    
    # Update history
    hou.session.flam3_CS = [] # type: ignore
    hou.session.flam3_CS = viewers_col # type: ignore


def viewportParticleDisplay(self: hou.Node) -> None:
    pttype = self.parm("vptype").evalAsInt()
    Points = hou.viewportParticleDisplay.Points # type: ignore
    Pixels = hou.viewportParticleDisplay.Pixels # type: ignore

    for view in getSceneViewers():
        settings = view.curViewport().settings()
        if pttype == 0:
            settings.particleDisplayType(Points)
        elif pttype == 1:
            settings.particleDisplayType(Pixels)


def viewportParticleSize(self: hou.Node) -> None:
    Points = hou.viewportParticleDisplay.Points # type: ignore
    ptsize = self.parm("vpptsize").evalAsFloat()

    for view in getSceneViewers():
        settings = view.curViewport().settings()
        settings.particleDisplayType(Points)
        settings.particlePointSize(ptsize)
        
        
def setHydraRenderer(self: hou.Node) -> None:
    rndtype = self.parm("rndtype").evalAsInt()
    for view in getSceneViewers():
        if rndtype == 0:
            hou.SceneViewer.setHydraRenderer(view, 'Houdini GL')
        elif rndtype == 1:
            hou.SceneViewer.setHydraRenderer(view, 'Karma')
        elif rndtype == 2:
            hou.SceneViewer.setHydraRenderer(view, 'Storm')
            


def flam3USD_about_msg(self):
    
    nl = "\n"
    nnl = "\n\n"

    year = datetime.now().strftime("%Y")
    flam3husd_houdini_version = f"Version: {FLAM3HUSD_VERSION}"
    Implementation_years = f"2020/{year}"
    Implementation_build = f"Author: Alessandro Nardini ( Italy )\nCode language: VEX H19.x, Python 3.9.10\n{flam3husd_houdini_version}\n{Implementation_years}"

    h_version = '.'.join(str(x) for x in hou.applicationVersion())
    Houdini_version = f"Host:\nSideFX Houdini {h_version}"
    Python_version = f"Python: {python_version()}"
    license_type = str(hou.licenseCategory()).split(".")[-1]
    Houdini_license = f"License: {license_type}"
    Platform = f"Platform: {hou.applicationPlatformInfo()}"
    PC_name = f"Machine name: {hou.machineName()}"
    User = f"User: {hou.userName()}"
    
    build = (Implementation_build, nnl,
             Houdini_version, nl,
             Houdini_license, nl,
             Python_version, nl,
             Platform, nl,
             PC_name, nl,
             User
             )
    
    build_about_msg = "".join(build)

    self.setParms({MSG_FLAM3HUSDABOUT: build_about_msg})
