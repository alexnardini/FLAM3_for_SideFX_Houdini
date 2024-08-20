from platform import python_version
from datetime import datetime
import hou


#   Tested on:  PYTHON v3.7.13  (H19)
#               PYTHON v3.9.10  (H19.5)
#               PYTHON v3.10.10 (H20)
#               PYTHON v3.11.7  (H20.5)
#
#   Title:      SideFX Houdini FLAM3HUSD
#   Author:     Alessandro Nardini
#   date:       September 2023, Last revised February 2024
#
#   Name:       PY_FLAM3USD "PYTHON"
#
#   Comment:    Simple utility node to quickly setup
#               fractal flames point clouds in Solaris for previews.
#               
#               Everything is then glued together inside Houdini.


FLAM3HUSD_VERSION = '0.0.6'

PREFS_PARTICLE_TYPE = 'vptype'
PREFS_PARTICLE_SIZE = 'vpptsize'
PREFS_VIEWPORT_DARK = 'setdark'

MSG_FLAM3HUSDABOUT = 'flam3husdabout_msg'


def houdini_version() -> int:
    return int(''.join(str(x) for x in hou.applicationVersion()[:1]))



def util_getSceneViewers() -> list:
    """
    Returns:
        list: [return a list of open scene viewers]
    """    
    views = hou.ui.paneTabs() # type: ignore
    return [v for v in views if isinstance(v, hou.SceneViewer)]



def autoSetRenderer_on_create(self: hou.LopNode) -> None:
    for view in util_getSceneViewers():
        cr = hou.SceneViewer.currentHydraRenderer(view)
        if "Houdini" in cr:
            hou.SceneViewer.setHydraRenderer(view, cr)
            # Sync FLAM3H nodes
            for n in self.type().instances():
                n.setParms({"rndtype": 0}) # type: ignore
        elif "Karma" in cr:
            hou.SceneViewer.setHydraRenderer(view, cr)
            # Sync FLAM3H nodes
            for n in self.type().instances():
                n.setParms({"rndtype": 1}) # type: ignore
        elif "Storm" in cr:
            hou.SceneViewer.setHydraRenderer(view, cr)
            # Sync FLAM3H nodes
            for n in self.type().instances():
                n.setParms({"rndtype": 2}) # type: ignore
            


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

    # INITIALIZE F3H_CS
    try:
        hou.session.flam3h_viewport_CS # type: ignore
    except:
        hou.session.flam3h_viewport_CS = [] # type: ignore



def colorSchemeDark(self: hou.LopNode) -> None:
    try:
        module_test = hou.session.flam3h_viewport_CS # type: ignore
    except:
        hou.session.flam3h_viewport_CS = [] # type: ignore

    count = 0
    viewers_col = []

    setprm = self.parm(PREFS_VIEWPORT_DARK).eval()
    
    Light = hou.viewportColorScheme.Light # type: ignore
    Grey  = hou.viewportColorScheme.Grey # type: ignore
    Dark  = hou.viewportColorScheme.Dark # type: ignore
    # The following is a lazy way to make this backward compatible with H19.x
    # as the DarkGrey color scheme has been introduced in H20.x first
    if houdini_version() < 20: DarkGrey = Grey
    else: DarkGrey = hou.viewportColorScheme.DarkGrey # type: ignore

    for view in util_getSceneViewers():

        settings = view.curViewport().settings()
        col = settings.colorScheme()
        viewers_col.append(col)
        try:
            idx_test = hou.session.flam3h_viewport_CS[count] # type: ignore
        except:
            if len(hou.session.flam3h_viewport_CS) > 0: # type: ignore
                hou.session.flam3h_viewport_CS.append(viewers_col) # type: ignore
            else:
                hou.session.flam3h_viewport_CS = [] # type: ignore
                hou.session.flam3h_viewport_CS.append(viewers_col) # type: ignore

        if setprm:
            if len(hou.session.flam3h_viewport_CS) == 0: # type: ignore
                if col == Light or col == Grey or col == DarkGrey:
                    settings.setColorScheme(Dark)
            else:
                if col == Light or col == Grey or col == DarkGrey:
                    settings.setColorScheme(Dark)
                elif col == Dark and hou.session.flam3h_viewport_CS[count] != Dark: # type: ignore
                    if hou.session.flam3h_viewport_CS[count] == Light: # type: ignore
                        settings.setColorScheme(Light)
                    elif hou.session.flam3h_viewport_CS[count] == Grey: # type: ignore
                        settings.setColorScheme(Grey)
                    elif hou.session.flam3h_viewport_CS[count] == DarkGrey: # type: ignore
                        settings.setColorScheme(DarkGrey)

        else:
            if col == Dark and hou.session.flam3h_viewport_CS[count] != Dark: # type: ignore
                if hou.session.flam3h_viewport_CS[count] == Light: # type: ignore
                    settings.setColorScheme(Light)
                elif hou.session.flam3h_viewport_CS[count] == Grey: # type: ignore
                    settings.setColorScheme(Grey)
                elif hou.session.flam3h_viewport_CS[count] == DarkGrey: # type: ignore
                    settings.setColorScheme(DarkGrey)
        count += 1
        
    # Sync FLAM3H nodes
    all_f3h = self.type().instances()
    if len(all_f3h) > 1:
        [f3h.setParms({PREFS_VIEWPORT_DARK: setprm}) for f3h in all_f3h if f3h != self if f3h.parm(PREFS_VIEWPORT_DARK).eval() != setprm]
    
    # Update history
    hou.session.flam3h_viewport_CS = [] # type: ignore
    hou.session.flam3h_viewport_CS = viewers_col # type: ignore



def viewportParticleDisplay(self: hou.LopNode) -> None:
    pttype = self.parm("vptype").evalAsInt()
    Points = hou.viewportParticleDisplay.Points # type: ignore
    Pixels = hou.viewportParticleDisplay.Pixels # type: ignore

    for view in util_getSceneViewers():
        settings = view.curViewport().settings()
        if pttype == 0:
            settings.particleDisplayType(Points)
        elif pttype == 1:
            settings.particleDisplayType(Pixels)
            
    # Sync FLAM3H nodes
    all_f3h = self.type().instances()
    if len(all_f3h) > 1:
        [f3h.setParms({PREFS_PARTICLE_TYPE: pttype}) for f3h in all_f3h if f3h != self if f3h.parm(PREFS_PARTICLE_TYPE).eval() != pttype]



def viewportParticleSize(self: hou.LopNode) -> None:
    Points = hou.viewportParticleDisplay.Points # type: ignore
    ptsize = self.parm("vpptsize").evalAsFloat()

    for view in util_getSceneViewers():
        settings = view.curViewport().settings()
        settings.particleDisplayType(Points)
        settings.particlePointSize(ptsize)
        
    # Sync FLAM3H nodes
    all_f3h = self.type().instances()
    if len(all_f3h) > 1:
        [f3h.setParms({PREFS_PARTICLE_SIZE: ptsize}) for f3h in all_f3h if f3h != self if f3h.parm(PREFS_PARTICLE_SIZE).eval() != ptsize]
        
        
        
def setHydraRenderer(self: hou.LopNode) -> None:
    rndtype = self.parm("rndtype").evalAsInt()
    for view in util_getSceneViewers():
        if rndtype == 0:
            hou.SceneViewer.setHydraRenderer(view, 'Houdini GL')
            # Sync FLAM3H nodes
            for n in self.type().instances():
                if n != self:
                    n.setParms({"rndtype": 0}) # type: ignore
        elif rndtype == 1:
            if houdini_version() < 20:
                hou.SceneViewer.setHydraRenderer(view, 'Karma')
            else:
                # H20 changed this name so let use the new one
                hou.SceneViewer.setHydraRenderer(view, 'Karma CPU')
            # Sync FLAM3H nodes
            for n in self.type().instances():
                if n != self:
                    n.setParms({"rndtype": 1}) # type: ignore
        elif rndtype == 2:
            hou.SceneViewer.setHydraRenderer(view, 'Storm')
            # Sync FLAM3H nodes
            for n in self.type().instances():
                if n != self:
                    n.setParms({"rndtype": 2}) # type: ignore
            


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
