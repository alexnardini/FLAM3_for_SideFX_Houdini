from platform import python_version
from datetime import datetime
from typing import Union
import hou


#   Tested on:  PYTHON v3.7.13  (H19)
#               PYTHON v3.9.10  (H19.5)
#               PYTHON v3.10.10 (H20)
#               PYTHON v3.11.7  (H20.5)
#
#   Title:      SideFX Houdini FLAM3HUSD
#   Author:     Alessandro Nardini
#   date:       September 2023, Last revised March 2025
#
#   Name:       PY_FLAM3USD "PYTHON"
#
#   Comment:    Simple utility node to quickly setup
#               fractal flames point clouds in Solaris for previews.
#
#               This is basic and its the start of something.
#               
#               Everything is then glued together inside Houdini.


FLAM3HUSD_VERSION = '0.1.35'


'''
LIST OF CLASSES:

    flam3husd_scripts
    flam3husd_general_utils
    flam3husd_about_utils
    
    _NOTE:
        - Class @properties are always defined inbetween the @staticmethods and the class methods.
        - Global variables are all upper cases. Every upper case variable's name created inside any definition always start with an underscore (_)

'''


PREFS_FLAM3H_PATH = 'flam3hpath'
PREFS_VIEWPORT_PT_TYPE = 'vptype'
PREFS_VIEWPORT_PT_SIZE = 'vpptsize'
PREFS_VIEWPORT_DARK = 'setdark'
PREFS_KARMA_PIXEL_SAMPLES = 'pxsamples'
PREFS_KARMA_F3H_SHADER_GAMMA = 'f3h_gamma'
PREFS_KARMA_F3H_SHADER_HUE = 'f3h_hsv_h'
PREFS_KARMA_F3H_SHADER_SATURATION = 'f3h_hsv_s'
PREFS_KARMA_F3H_SHADER_VALUE = 'f3h_hsv_v'

# DATA
PREFS_PVT_FLAM3HUSD_DATA_DISABLED = 'disabled'
PREFS_PVT_FLAM3HUSD_DATA_F3H_VALID = 'f3h_valid'
PREFS_PVT_FLAM3HUSD_DATA_H190 = 'h_19_0'

# Messages
MSG_FLAM3HUSDABOUT = 'flam3husdabout_msg'

# Flash messages timer
FLAM3H_FLASH_MESSAGE_TIMER: float = 2 # Note that for this FLAM3HUSD OTL the flash messages only run in netowrk editors belonging to the Lop context.

# The full path will be the string inside the parameter: PREFS_FLAM3H_PATH
# plus this one
FLAM3H_TO_FLAM3HUSD_NODE_PATH = '/TAGS/OUT_TO_FLAM3HUSD'




# FLAM3HUSD SCRIPTS start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class flam3husd_scripts:
    """
class flam3husd_scripts

@STATICMETHODS

@METHODS
* flam3husd_is_valid_flam3h_node(self) -> None:
* flam3husd_h190_check(self) -> None:
* flam3husd_on_create_set_prefs_viewport(self, default_value_pt: float=1) -> None:
* flam3husd_on_create(self) -> None:
* autoSetRenderer_on_create(self) -> None:
* flam3h_on_deleted(self) -> None:

    """


    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3HUSD node houdini kwargs.
            
        Returns:
            (None):
        """  
        self._kwargs = kwargs
        self._node = kwargs['node']






    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def kwargs(self):
        return self._kwargs
    
    @property
    def node(self):
        return self._node



    def flam3husd_is_valid_flam3h_node(self) -> None:
        """Check if the imported FLAM3H node is valid or not
        
        Args:
            (self): 
            
        Returns:
            (None): 
        """  
        node = self.node
        f3h_path = node.parm(PREFS_FLAM3H_PATH).eval()
        f3h_to_f3husd_node = hou.node(f"{f3h_path}{FLAM3H_TO_FLAM3HUSD_NODE_PATH}")
        try:
            type = f3h_to_f3husd_node.type()
            if type.name() == 'null': flam3husd_general_utils.set_private_prm(node, PREFS_PVT_FLAM3HUSD_DATA_F3H_VALID, 1)
            else: flam3husd_general_utils.set_private_prm(node, PREFS_PVT_FLAM3HUSD_DATA_F3H_VALID, 0)
        except:
            flam3husd_general_utils.set_private_prm(node, PREFS_PVT_FLAM3HUSD_DATA_F3H_VALID, 0)
        

    
    
    
    def flam3husd_h190_check(self) -> None:
        """Karma CPU has a bug in Houdini version 19.0.x and it crashes if it find a null primitive.
        Since the xform handls viz may generate one, this is used to hide the UI Karma handles import tab.
        
        Args:
            (self): 
            
        Returns:
            (None): 
        """  

        node = self.node
        if flam3husd_general_utils.houdini_version(2) == 190:
            flam3husd_general_utils.set_private_prm(node, PREFS_PVT_FLAM3HUSD_DATA_H190, 1)
        else:
            flam3husd_general_utils.set_private_prm(node, PREFS_PVT_FLAM3HUSD_DATA_H190, 0)
    
    
    
    def flam3husd_on_create_set_prefs_viewport(self, default_value_pt: float=1) -> None:
        """Initialize the necessary data for the viewport display preference's option on creation.
        This need some work as it is a little rough, I'll be back to this at some point. Good enough for now.
        
        Args:
            (self):
            default_value_pt(float): A default value to compare to for the point setting. This must always be the same as the FLAM3HUSD UI parameter's default values.
            
        Returns:
            (None):
        """
        
        node = self.node
        
        # Update dark history
        flam3husd_general_utils.util_store_all_viewers_color_scheme_onCreate() # init Dark viewers data, needed for the next definition to run
        flam3husd_general_utils(self.kwargs).colorSchemeDark(False) # type: ignore
        # Set other FLAM3HUSD instances to dark if any
        all_f3h = node.type().instances()
        all_f3h_vpptsize = []
        all_f3h_vptype = []
        
        if len(all_f3h) > 1:

            for f3h in all_f3h:
                if f3h != node:
                    all_f3h_vpptsize.append(f3h.parm(PREFS_VIEWPORT_PT_SIZE).eval())
                    all_f3h_vptype.append(f3h.parm(PREFS_VIEWPORT_PT_TYPE).eval())
                    if f3h.parm(PREFS_VIEWPORT_DARK).eval():
                        node.setParms({PREFS_VIEWPORT_DARK: 1})
                        flam3husd_general_utils(self.kwargs).colorSchemeDark(False)
                        break
                    else:
                        break
        else:
            node.setParms({PREFS_VIEWPORT_DARK: 1})
            flam3husd_general_utils(self.kwargs).colorSchemeDark(False) # type: ignore
    
        # If we collected some data, set
        if all_f3h_vpptsize:
            node.setParms({PREFS_VIEWPORT_PT_SIZE: all_f3h_vpptsize[0]})
            node.setParms({PREFS_VIEWPORT_PT_TYPE: all_f3h_vptype[0]})
            
        else:
            Pixels = hou.viewportParticleDisplay.Pixels # type: ignore
            
            for view in flam3husd_general_utils.util_getSceneViewers():
                
                # Lets make sure we check for a viewer in the Lop context
                if flam3husd_general_utils.util_is_context('Lop', view):
                    
                    settings = view.curViewport().settings()
                    size = settings.particlePointSize()
                    
                    if size != default_value_pt:
                        node.setParms({PREFS_VIEWPORT_PT_SIZE: size})
                        
                    type = settings.particleDisplayType()
                    if type == Pixels:
                        node.setParms({PREFS_VIEWPORT_PT_TYPE: 1})
                        
                else:
                    # FLAM3HUSD shoud use its parameter default value in this case, but just to be sure
                    node.setParms({PREFS_VIEWPORT_PT_SIZE: default_value_pt})




    def flam3husd_on_create(self) -> None:
        """Initialize FLAM3HUSD node on creation and all the data it need to run.
        
        Args:
            (self)
            
        Returns:
            (None):
        """
        # Set initial node color
        self.node.setColor(hou.Color((0.165,0.165,0.165)))
        
        # Set renderer
        self.autoSetRenderer_on_create()
        # Set viewport preferences settings
        self.flam3husd_on_create_set_prefs_viewport()
        # Check if we are importing a valid FLAM3H node
        self.flam3husd_is_valid_flam3h_node()
        # Check H version and set
        self.flam3husd_h190_check()
        # Set about box
        flam3husd_about_utils(self.kwargs).flam3husd_about_msg()
        
        # Lock utility parameters
        self.node.parm(PREFS_PVT_FLAM3HUSD_DATA_DISABLED).lock(True)
        
        
        
    def flam3husd_on_loaded(self) -> None:
        """Initialize FLAM3HUSD node on creation and all the data it need to run.
        For now the same as the on_create script, will see later on how this will evolve.
        
        Args:
            (self)
            
        Returns:
            (None):
        """
        
        # Set renderer
        self.autoSetRenderer_on_create()
        # Set viewport preferences settings
        self.flam3husd_on_create_set_prefs_viewport()
        # Check if we are importing a valid FLAM3H node
        self.flam3husd_is_valid_flam3h_node()
        # Check H version and set
        self.flam3husd_h190_check()
        # Set about box
        flam3husd_about_utils(self.kwargs).flam3husd_about_msg()
        
        # Lock utility parameters
        self.node.parm(PREFS_PVT_FLAM3HUSD_DATA_DISABLED).lock(True)
        



    def autoSetRenderer_on_create(self) -> None:
        """This need more work to make it smarter...its a start
        Set the hydra renderer based on the one found in the viewers already.
        Since the renderer menu will set all the Lop viewers in one go, we assume that the are all the same type already.
        
        Args:
            (self)
            
        Returns:
            (None):
        """
        
        node: hou.LopNode = self.node
        
        for view in flam3husd_general_utils.util_getSceneViewers():
            
            # Set only if it is a Lop viewer
            if flam3husd_general_utils.util_is_context('Lop', view):
            
                cr = hou.SceneViewer.currentHydraRenderer(view)
                if "Houdini" in cr:
                    hou.SceneViewer.setHydraRenderer(view, cr)
                    # Sync FLAM3HUSD nodes
                    [n.setParms({"rndtype": 0}) for n in node.type().instances()]
                elif flam3husd_general_utils.karma_hydra_renderer_name() in cr:
                    hou.SceneViewer.setHydraRenderer(view, cr)
                    # Sync FLAM3HUSD nodes
                    [n.setParms({"rndtype": 1}) for n in node.type().instances()]
                elif "Storm" in cr:
                    hou.SceneViewer.setHydraRenderer(view, cr)
                    # Sync FLAM3HUSD nodes
                    [n.setParms({"rndtype": 3}) for n in node.type().instances()]
                        
                        
                        
    # Wip
    def flam3husd_on_deleted(self) -> None:
        """Cleanup the data on deletion.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        node_instances = node.type().instances()
        
        if len(node_instances) == 1:
            
            # Delete the Houdini update mode data if needed
            try: del hou.session.HUSD_CS_STASH_DICT # type: ignore
            except: pass








# FLAM3HUSD GENERAL UTILS start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################

class flam3husd_general_utils:
    """
class flam3husd_general_utils

@STATICMETHODS
* set_private_prm(node: hou.SopNode, prm_name: str, data: Union[str, int, float]) -> None:
* karma_hydra_renderer_name() -> str:
* houdini_version(digit: int=1) -> int:
* util_getSceneViewers() -> list:
* util_is_context(context: str, viewport: hou.paneTabType) -> bool:
* flash_message(msg: Union[str, None], timer: float=FLAM3H_FLASH_MESSAGE_TIMER, img: Union[str, None]=None, context: str='Lop') -> None:
* set_status_msg(msg: str, type: str) -> None:

@METHODS
* util_store_all_viewers_color_scheme(self) -> None:
* colorSchemeDark(self, update_others: bool=True) -> None:
* viewportParticleDisplay(self) -> None:
* viewportParticleSize(self, reset_val: Union[float, None]=None) -> None:
* setHydraRenderer(self) -> None:
* reset_flam3h_shader(self) -> None:
* flam3husd_display_help(self) -> None:

    """


    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3HUSD node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs = kwargs
        self._node = kwargs['node']



    @staticmethod
    def set_private_prm(node: hou.SopNode, prm_name: str, data: Union[str, int, float]) -> None:
        """Set a parameter value while making sure to unlock and lock it right after.
        This is being introduced to add an extra level of security so to speak to certain parameters
        that are not meant to be changed by the user, so at least it will require some step before allowing them to do so.
        
        Args:
            node(hou.SopNode): this FLAM3HUSD node.
            prm_name(str): the parameter name.
            data(Union[str, int, float]): The value to set the parameter to.
            
        Returns:
            (None):
        """ 
        prm = node.parm(prm_name)
        prm.lock(False)
        prm.set(data)
        prm.lock(True)





    @staticmethod
    def karma_hydra_renderer_name() -> str:
        """Return the internal hydra renderer name for Karma.
        
        Args:
            (None):
            
        Returns:
            (str): [Return the internal hydra renderer name for Karma.]
        """    
        karma_name = 'Karma CPU'
        if flam3husd_general_utils.houdini_version() < 20: karma_name = 'Karma'
        return karma_name




    @staticmethod
    def houdini_version(digit: int=1) -> int:
        """Retrieve the major Houdini version number currently in use.

        Args:
            digit(int): Default to 1: 19, 20. if set to 2: 190, 195, 200, 205, and so on.

        Returns:
            (int): By default it will retrieve major Houdini version number. ex: 19, 20 but not: 195, 205
        """ 
        return int(''.join(str(x) for x in hou.applicationVersion()[:digit]))



    @staticmethod
    def util_getSceneViewers() -> list:
        """Return a list of viewer currently open in this Houdini session.
        
        Args:
            (None):
            
        Returns:
            (list): [return a list of open scene viewers]
        """    
        views = hou.ui.paneTabs() # type: ignore
        return [v for v in views if isinstance(v, hou.SceneViewer)]
    
    
    
    @staticmethod
    def util_is_context(context: str, viewport: hou.paneTabType) -> bool:
        """Return if we are inside a context or not.
        
        Args:
            context(str): The context we want to check if we are currently in. Options so far are: 
                * Sop: str
                * Lop: str
            viewport(hou.paneTabType): Any of the available pane tab types, in my case will always be: hou.paneTabType.SceneViewer or hou.SceneViewer
            
        Returns:
            (bool): [True if we are in Solaris and False if we are not.]
        """    
        context_now: hou.NodeTypeCategory = hou.ui.findPaneTab(viewport.name()).pwd().childTypeCategory() # type: ignore
        if str(context_now.name()).lower() == context.lower(): return True
        else: return False
        
    
    
    @staticmethod
    def flash_message(msg: Union[str, None], timer: float=FLAM3H_FLASH_MESSAGE_TIMER, img: Union[str, None]=None, context: str='Lop') -> None:
        """Cause a message to appear on the top left of the network editor.
        Will only work if the network editors are within the Lop context.

        Args:
            msg(Union[str, None]): The string message to print or None.
            timer(float): Default to: FLAM3H_FLASH_MESSAGE_TIMER. How long the printed message stay before it fade away.
            img(Union[str, None]): Default to none. specifies an icon or image file that should be displayed along with the text specified in the msg argument.
            context(str): Default to: "Lop". The context the network editors need to belong to in order to display the message.

        Returns:
            (None):
        """  
        if hou.isUIAvailable():
            [ne.flashMessage(img, msg, timer) for ne in [p for p in hou.ui.paneTabs() if p.type() == hou.paneTabType.NetworkEditor and flam3husd_general_utils.util_is_context(context, p)]] # type: ignore

        
        
        
    @staticmethod
    def set_status_msg(msg: str, type: str) -> None:
        """Print a message to the Houdini's status bar if the UI is available.

        Args:
            msg(str): The message string to print
            type(str): The type of severity message to use, Possible choises are: MSG ( message ), IMP ( important message ), WARN ( warning ).
            
        Returns:
            (None):
        """

        if hou.isUIAvailable():
            st = { 'MSG': hou.severityType.Message, 'IMP': hou.severityType.ImportantMessage, 'WARN': hou.severityType.Warning }  # type: ignore
            hou.ui.setStatusMessage(msg, st.get(type)) # type: ignore
        


    @staticmethod
    def util_store_all_viewers_color_scheme_onCreate() -> None:
        """Store dictionaries of viewers color schemes if needed on FLAM3HUSD node creation
        This version do not check from which parameter run as we need it to run regardless.
        
        Args:
            (None):
            
        Returns:
            (None):  
        """  
        # Check if the required data exist already
        try: hou.session.HUSD_CS_STASH_DICT # type: ignore
        except: # if not, lets create it
            views_scheme: list[hou.EnumValue]  = []
            views_keys: list[str] = []
            for v in flam3husd_general_utils.util_getSceneViewers():
                
                # Store only if it is a Lop viewer
                if flam3husd_general_utils.util_is_context('Lop', v):
                
                    view = v.curViewport()
                    settings = view.settings()
                    _CS = settings.colorScheme()
                    if _CS != hou.viewportColorScheme.Dark: # type: ignore
                        views_scheme.append(_CS)
                        views_keys.append(v.name())
            
            # Always store and update this data if we collected something
            if views_scheme and views_keys: hou.session.HUSD_CS_STASH_DICT: dict[str, hou.EnumValue] = dict(zip(views_keys, views_scheme)) # type: ignore







    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def kwargs(self):
        return self._kwargs
    
    @property
    def node(self):
        return self._node




    def util_store_all_viewers_color_scheme(self) -> None:
        """Store dictionaries of viewers color schemes
        
        Args:
            (self):
            
        Returns:
            (None):  
        """  
        # Do this only if the parameter toggle is: PREFS_VIEWPORT_DARK
        try: parm = self.kwargs['parm']
        except: parm = None
        _ENTER_PRM = None
        if parm is not None: _ENTER_PRM = parm.name()
        if _ENTER_PRM is not None and _ENTER_PRM == PREFS_VIEWPORT_DARK:
            views_scheme: list[hou.EnumValue]  = []
            views_keys: list[str] = []
            for v in self.util_getSceneViewers():
                
                # Store only if it is a Lop viewer
                if self.util_is_context('Lop', v):
                    
                    view = v.curViewport()
                    settings = view.settings()
                    _CS = settings.colorScheme()
                    if _CS != hou.viewportColorScheme.Dark: # type: ignore
                        views_scheme.append(_CS)
                        views_keys.append(v.name())
            
            # Always store and update this data
            hou.session.HUSD_CS_STASH_DICT: dict[str, hou.EnumValue] = dict(zip(views_keys, views_scheme)) # type: ignore




    def colorSchemeDark(self, update_others: bool=True) -> None:
        """Change viewport color scheme to dark
        and remember the current color scheme so to switch back to it when unchecked.
        If the viewport color scheme is already dark, checking this option will do nothing. 
        
        Args:
            (self):
            update_others(bool): Default to True. Update also the other FLAM3HUSD nodes in the scene if any
            
        Returns:
            (None):
        """
        node = self.node
        prm = node.parm(PREFS_VIEWPORT_DARK)
        views = self.util_getSceneViewers()
        
        if views:
            if prm.eval():
                # Store all viewers current color schemes
                # if different than Dark
                self.util_store_all_viewers_color_scheme()
                
                dark = False
                lop_view = False
                
                for v in views:
                    
                    # Set only if it is a Lop viewer
                    if self.util_is_context('Lop', v):
                        
                        if lop_view is False: lop_view = True
                        
                        settings = v.curViewport().settings()
                        _CS = settings.colorScheme()
                        if _CS != hou.viewportColorScheme.Dark: # type: ignore
                            settings.setColorScheme(hou.viewportColorScheme.Dark) # type: ignore
                            dark = True
                
                if lop_view:
                    
                    if dark:
                        _MSG = f"Dark: ON"
                        self.flash_message(_MSG)
                        self.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                    else:
                        _MSG = f"Dark already"
                        self.set_status_msg(f"{node.name()}: {_MSG}. Viewers are in Dark mode already", 'MSG')
                        
                else:
                    prm.set(0)
                    
                    _MSG = f"No Lop viewers in the current Houdini Desktop."
                    self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Lop viewer to either set to Dark or restore.", 'WARN')
                    self.flash_message(f"Dark: {_MSG}")
                    
                    
            else:
                
                try: _STASH_DICT: Union[dict[str, hou.EnumValue], None] = hou.session.HUSD_CS_STASH_DICT # type: ignore
                except: _STASH_DICT: Union[dict[str, hou.EnumValue], None] = None
                    
                dark = False
                if _STASH_DICT is not None:
                    for v in views:
                        # Here we are not checking if the viewer belong to Sop or Lop
                        # because the stashed dict has already the viewers filtered on creation inside: flam3husd_general_utils.util_store_all_viewers_color_scheme()
                        key = v.name()
                        _STASH: Union[hou.EnumValue, None] = _STASH_DICT.get(key)
                        if _STASH is not None:
                            settings = v.curViewport().settings()
                            _CS = settings.colorScheme()
                            if _CS == hou.viewportColorScheme.Dark: # type: ignore
                                settings.setColorScheme(_STASH)
                                dark = True
                                
                if dark:
                    _MSG = f"Dark: OFF"
                    self.flash_message(_MSG)
                    self.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    
                else:
                    
                    try:
                        
                        if hou.session.HUSD_CS_STASH_DICT: # type: ignore
                            _MSG = f"No viewer in Dark mode"
                            self.set_status_msg(f"{node.name()}: {_MSG}. None of the current viewer are set to Dark.", 'MSG')
                        else:
                            _MSG = f"Nothing to restore"
                            self.set_status_msg(f"{node.name()}: {_MSG}. None of the current viewers has been switched to Dark. They probably were already in Dark mode.", 'MSG')
                            
                    except AttributeError:
                        pass
                            
        else:
            prm.set(0)
            
            _MSG = f"No Lop viewers in the current Houdini Desktop."
            self.set_status_msg(f"{node.name()}: {_MSG} You need at least one viewer to either set to Dark or restore.", 'WARN')
            self.flash_message(f"Dark: {_MSG}")
            
            
        if update_others:
            # Update dark preference's option toggle on other FLAM3HUSD nodes instances
            all_f3h = self.node.type().instances()
            if len(all_f3h) > 1:
                [f3h.setParms({PREFS_VIEWPORT_DARK: prm.eval()}) for f3h in all_f3h if f3h != node if f3h.parm(PREFS_VIEWPORT_DARK).eval() != prm.eval()]




    def viewportParticleDisplay(self) -> None:
        """Switch viewport particle display mode
        between Pixel and Points.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        pttype = node.parm(PREFS_VIEWPORT_PT_TYPE).evalAsInt()
        Points = hou.viewportParticleDisplay.Points # type: ignore
        Pixels = hou.viewportParticleDisplay.Pixels # type: ignore

        for view in self.util_getSceneViewers():
            
            # Set only if it is a Lop viewer
            if self.util_is_context('Lop', view):
                
                settings = view.curViewport().settings()
                if pttype == 0:
                    settings.particleDisplayType(Points)
                elif pttype == 1:
                    settings.particleDisplayType(Pixels)
                
        # Sync FLAM3HUSD nodes
        all_f3h = node.type().instances()
        if len(all_f3h) > 1:
            [f3h.setParms({PREFS_VIEWPORT_PT_TYPE: pttype}) for f3h in all_f3h if f3h != node if f3h.parm(PREFS_VIEWPORT_PT_TYPE).eval() != pttype]

            
            
            
    def viewportParticleSize(self, reset_val: Union[float, None]=None, prm_name_size: str=PREFS_VIEWPORT_PT_SIZE) -> None:
        """When the viewport particle display type is set to Point
        this will change their viewport size.
        
        Args:
            (self):
            reset_val (Union[float, None]): Default to None. Can be either "None" or a float value. If "None" it will use the current parameter value, otherwise it will use the one passed in this function.
            prm_name_size(str): Default to: PREFS_VIEWPORT_PT_SIZE. The name of the parameter to set.
            
        Returns:
            (None):
        """
        node = self.node
        Points = hou.viewportParticleDisplay.Points # type: ignore
        ptsize = node.parm(prm_name_size).eval()

        for view in self.util_getSceneViewers():
            
            # Set only if it is a Lop viewer
            if self.util_is_context('Lop', view):
            
                settings = view.curViewport().settings()
                settings.particleDisplayType(Points)
                if reset_val is None:
                    if prm_name_size == PREFS_VIEWPORT_PT_SIZE: settings.particlePointSize(ptsize)
                else:
                    ptsize = float(reset_val)
                    if prm_name_size == PREFS_VIEWPORT_PT_SIZE: settings.particlePointSize(ptsize)
                    prm = node.parm(self.kwargs['parmtuple'].name())
                    prm.deleteAllKeyframes()
                    prm.set(ptsize)
            
        # Update Point Size preference's option toggle on other FLAM3H nodes instances
        if prm_name_size == PREFS_VIEWPORT_PT_SIZE and node.parm(PREFS_VIEWPORT_PT_TYPE).evalAsInt() == 0:
            [f3h.parm(prm_name_size).deleteAllKeyframes() for f3h in node.type().instances()]
            [f3h.setParms({prm_name_size: ptsize}) for f3h in node.type().instances() if f3h.parm(prm_name_size).eval() != ptsize]
            



    def setHydraRenderer(self) -> None:
        """Set the selected hydre renderer in the availables Lop viewers.
        
        Args:
            (self):
            
        Returns:
            (None):  
        """  
        node = self.node
        rndtype = node.parm("rndtype").evalAsInt()
        
        for view in self.util_getSceneViewers():
            
            # Set only if it is a Lop viewer
            if self.util_is_context('Lop', view):
                
                # This double check should not be necessary
                # But H19 did throw me an error in some cases so I leave it here for now
                if isinstance(view, hou.SceneViewer):
                    
                    if rndtype == 0:
                        hou.SceneViewer.setHydraRenderer(view, 'Houdini GL')
                        # Sync FLAM3HUSD nodes
                        [n.setParms({"rndtype": rndtype}) for n in node.type().instances() if n != node]
                        
                    elif rndtype == 1:
                        hou.SceneViewer.setHydraRenderer(view, self.karma_hydra_renderer_name())
                        # Sync FLAM3HUSD nodes
                        [n.setParms({"rndtype": rndtype}) for n in node.type().instances() if n != node]
                        
                    elif rndtype == 2:
                        hou.SceneViewer.setHydraRenderer(view, 'Storm')
                        # Sync FLAM3HUSD nodes
                        [n.setParms({"rndtype": rndtype}) for n in node.type().instances() if n != node]
                        
                    
                    
                    
    def reset_flam3h_shader(self) -> None:
        """Reset the OUT Render settings parameters tab.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        
        prms_f3h_shader_data: dict = {  PREFS_KARMA_F3H_SHADER_GAMMA: 2.2,
                                        PREFS_KARMA_F3H_SHADER_HUE: 1,
                                        PREFS_KARMA_F3H_SHADER_SATURATION: 1,
                                        PREFS_KARMA_F3H_SHADER_VALUE: 1 }
        
        # Clear and set
        [node.parm(key).deleteAllKeyframes() for key in prms_f3h_shader_data.keys()]
        [node.setParms({key: value}) for key, value in prms_f3h_shader_data.items()]
        
        
        
    def flam3husd_display_help(self) -> None:
        """Open the Houdini help browser to display the FLAM3HUSD node documentation.

        Args:
            (self):
            
        Returns:
            (None):
        """
        hou.ui.displayNodeHelp(self.node.type()) # type: ignore








# FLAM3HUSD ABOUT start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################

class flam3husd_about_utils():
    """
class flam3husd_about_utils

@STATICMETHODS

@METHODS
* flam3husd_about_msg(self):

    """
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3HUSD node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs = kwargs
        self._node = kwargs['node']




    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def kwargs(self):
        return self._kwargs
    
    @property
    def node(self):
        return self._node




    def flam3husd_about_msg(self):
        """Build and set the FLAM3HUSD about message.
        
        Args:
            (self):
            
        Returns:
            (None):
        """ 
        
        nl = "\n"
        nnl = "\n\n"

        year = datetime.now().strftime("%Y")
        flam3husd_houdini_version = f"VERSION: {FLAM3HUSD_VERSION} :: (GPL)"
        Implementation_years = f"2023/{year}"
        Implementation_build = f"AUTHOR: Alessandro Nardini ( Italy )\n{flam3husd_houdini_version}\nCODE: vex H19.x.x, py 3.7.13\n{Implementation_years}"

        h_version = '.'.join(str(x) for x in hou.applicationVersion())
        Houdini_version = f"HOST:\nSideFX Houdini {h_version}"
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

        self.node.setParms({MSG_FLAM3HUSDABOUT: build_about_msg})

