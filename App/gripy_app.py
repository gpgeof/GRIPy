# -*- coding: utf-8 -*-
import os
import wx
from collections import OrderedDict
import app_utils
import gripy_classes
import gripy_functions
from OM.Manager import ObjectManager
from UI.uimanager import UIManager
from App import DEFS 
from App import log
from gripy_plugin_manager import GripyPluginManagerSingleton
#
wx.SystemOptions.SetOption("msw.remap", '0')
#

class GripyApp(wx.App):
    __version__ = None
    _inited = False
      
      
    def __init__(self):
        #self._load_app_definitions()
        #
        self.OM_file = None
        #self.UIM_file = None
        self._wx_app_state = OrderedDict(DEFS.get('wx.App'))
        class_full_name = app_utils.get_class_full_name(self)
        self._gripy_app_state = OrderedDict(DEFS.get(class_full_name))
        self._plugins_state = OrderedDict(DEFS.get('plugins', dict()))
        plugins_places = self._plugins_state.get('plugins_places')
        if plugins_places:
            plugins_places = [place.encode('utf-8') for place in plugins_places]
        else:
            plugins_places = ['Plugins']
        self._plugins_state['plugins_places'] = plugins_places   
        self._logging_state = OrderedDict(DEFS.get('logging', dict()))   
        #
        self._app_dir = os.getcwd()
        # wx.App args    
        _redirect = self._wx_app_state.get('redirect', False)
        _filename = self._wx_app_state.get('filename', None) 
        _useBestVisual = self._wx_app_state.get('useBestVisual', False) 
        _clearSigInt = self._wx_app_state.get('clearSigInt', True)
        # wx.App.__init__()        
        super(GripyApp, self).__init__(_redirect, _filename, 
                                       _useBestVisual, _clearSigInt
        )
        # Then, wx.App has inited and it calls OnInit


    # TODO: REVER ISSO E COLOCAR COMO wx.Config ou wx.StandardPaths
    #def set_app_dir():
    #    wx.App.Get()._app_dir = os.getcwd()
        """        
        print 'a1:', os.getcwd()
        sp = wx.StandardPaths.Get()
        sp.SetInstallPrefix(os.getcwd())
        print type(wx.App.Get())
        print wx.App.Get()
        
        print '\n\n\n'
        for f in ['GetConfigDir',
                  'GetUserConfigDir',
                  'GetDataDir',
                  'GetLocalDataDir',
                  'GetUserDataDir',
                  'GetUserLocalDataDir',
                  'GetDocumentsDir',
                  'GetPluginsDir',
                  'GetInstallPrefix',
                  'GetResourcesDir',
                  'GetTempDir',
                  'GetExecutablePath',
        ]:
            func = getattr(sp, f)
            print f, func()
        """    
        '''    
        print 'ExecutablePath:', sp.GetExecutablePath()
        print 'UserConfigDir:', sp.GetUserConfigDir()
        print 'DataDir:', sp.GetDataDir()
        print 'PluginsDir:', sp.GetPluginsDir()
        print 'InstallPrefix:', sp.GetInstallPrefix()
        '''
        #print os.getcwd()
        # print '\n\n\n'
        
        
    @staticmethod    
    def get_app_dir():
        return wx.App.Get()._app_dir
        

    def get_project_filename(self):
        return self.OM_file
        
        
    #def get_interface_filename(self):
    #    return self.UIM_file
 
    '''
    def _load_app_definitions(self):
        self.OM_file = None
        #self.UIM_file = None
        self._wx_app_state = OrderedDict(DEFS.get('wx.App'))
        class_full_name = app_utils.get_class_full_name(self)
        self._gripy_app_state = OrderedDict(DEFS.get(class_full_name))
        self._plugins_state = OrderedDict(DEFS.get('plugins', dict()))
        plugins_places = self._plugins_state.get('plugins_places')
        if plugins_places:
            plugins_places = [place.encode('utf-8') for place in plugins_places]
        else:
            plugins_places = ['Plugins']
        self._plugins_state['plugins_places'] = plugins_places   
        self._logging_state = OrderedDict(DEFS.get('logging', dict()))      
    '''
          
    '''          
    def save_app_state(self):
        return self.save_state_as(self._app_full_filename)
        
        
    def save_app_state_as(self, fullfilename):
        try:
            _state = self._get_state_dict()
            AsciiFile.write_json_file(_state, fullfilename)
            self._app_full_filename = fullfilename
            msg = 'GripyApp state was saved to file {}'.format(self._app_full_filename)
            self.loginfo(msg)
            return True
        except Exception, e:
            msg = 'Error in saving GripyApp state to file {}'.format(fullfilename)
            self.logexception(msg)
            raise e     
    '''        

    """
    Load ObjectManager data.
    """
    # Falta unload data
    def load_project_data(self, fullfilename):
        OM = ObjectManager(self)
        UIM = UIManager()
        self.OM_file = fullfilename
        ret = OM.load(self.OM_file)
        if not ret:
            msg = 'GRIPy project cannot be opened.'
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
            return
        mwc = UIM.list('main_window_controller')[0]
        tree_ctrl = UIM.list('tree_controller', mwc.uid)[0]
        if tree_ctrl:        
            tree_ctrl.set_project_name(self.OM_file)
                  
    """
    Save ObjectManager data.
    """                  
    def save_project_data(self, fullfilename=None):
        if fullfilename:
            self.OM_file = fullfilename
        if self.OM_file:
            OM = ObjectManager(self)
            OM.save(self.OM_file)

    """
    Load interface data.
    """
    def load_application_UI_data(self, fullfilename):
        #self.UIM_file = fullfilename
        #if self.UIM_file:
        UIM = UIManager()
        UIM.load_application_state_from_file(fullfilename)

    """
    Load interface data.
    """
    def load_user_UI_data(self, fullfilename):
        UIM = UIManager()
        UIM.load_user_state_from_file(fullfilename)


    """
    Save application structure UI data.
    """        
    def save_UI_application_data(self, fullfilename):
        UIM = UIManager()
        #UIM.save_application_state_to_file(fullfilename)
     
 
    """
    Save user UI data.
    """        
    def save_UI_user_data(self, fullfilename):
        #if fullfilename:
        #    self.UIM_file = fullfilename
        #if self.UIM_file:
        UIM = UIManager()
        #UIM.save_user_state_to_file(fullfilename)
        #UIM._save_state_to_file(self.UIM_file)        
       



    def OnInit(self):
        self._app_dir = os.getcwd()
        #self.set_app_dir()  # TODO: REVER ISSO CONFORME ACIMA NA FUNÇÃO

        if self._gripy_app_state.get('app_name') is not None:
            self.SetAppName(self._gripy_app_state.get('app_name')) 
        if self._gripy_app_state.get('app_display_name') is not None:
            self.SetAppDisplayName(self._gripy_app_state.get('app_display_name'))       
        if self._gripy_app_state.get('app_version') is not None:    
            self.__version__ = self._gripy_app_state.get('app_version')   
        if self._gripy_app_state.get('vendor_name') is not None:
            self.SetVendorName(self._gripy_app_state.get('vendor_name'))                       
        if self._gripy_app_state.get('vendor_display_name') is not None:
            self.SetVendorDisplayName(self._gripy_app_state.get('vendor_display_name'))           
        class_name = str(self.__class__.__module__) + '.' + str(self.__class__.__name__)  
        if self._gripy_app_state.get('class_name'):
            class_name = self._gripy_app_state.get('class_name') 
        self.SetClassName(class_name)
        self._gripy_debug_file = self._gripy_app_state.get('gripy_debug_file')
        self._inited = True
        self._init_has_ended_message()
        
        log.info('Starting to register Gripy internal classes...')
        gripy_classes.register_app_classes()
        log.info('Registering Gripy internal classes ended.')   
        
        log.info('Starting to register Gripy internal functions...')
        gripy_functions.register_app_functions()
        log.info('Registering Gripy internal functions ended.')          
        
        
        

        UIM = UIManager()
          
        #load_UI_file = True        
        load_UI_file = False

        if load_UI_file:
            """
            Load basic app from file.            
            """
            self.load_application_UI_data(self._gripy_app_state.get('app_UI_file'))
            
            self.load_user_UI_data(self._gripy_app_state.get('user_UI_file'))
            
            mwc = UIM.list('main_window_controller')[0]
            
        else:
            """
            Construct the application itself.
            """
            mwc = UIM.create('main_window_controller', 
                title=self._gripy_app_state.get('app_display_name') #,
                #icon='./icons/logo-transp.ico'#, pos=wx.Point(399, 322) 
            )
            
           # """
            # Menubar
            menubar_ctrl = UIM.create('menubar_controller', mwc.uid)
            # First level Menus
            mc_project = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&Project")      
            mc_edit = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&Edit")
            mc_well = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&Well")
            mc_precond = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&Preconditioning")
            mc_interp = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&Interpretation")
            mc_infer = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&Inference")
            mc_specdecom = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&SpecDecom")
            mc_tools = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&Tools")
            mc_plugins = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&Plugins")
            mc_debug = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&Debug")      
            

            
            # Project Menu
            UIM.create('menu_item_controller', mc_project.uid, 
                    label=u'&New project', 
                    help=u'Create a new empty GriPy Project.',
                    id=wx.ID_NEW,
                    callback='App.menu_functions.on_new'
            )
            UIM.create('menu_item_controller', mc_project.uid, 
                           kind=wx.ITEM_SEPARATOR
            )
            UIM.create('menu_item_controller', mc_project.uid, 
                    label=u'&Open', 
                    help=u'Open GriPy Project (*.pgg)',
                    id=wx.ID_OPEN,
                    callback='App.menu_functions.on_open'
            )
            UIM.create('menu_item_controller', mc_project.uid, 
                    label=u'&Save', 
                    help=u'Save GriPy Project',
                    id=wx.ID_SAVE,
                    callback='App.menu_functions.on_save'
            )   
            UIM.create('menu_item_controller', mc_project.uid, 
                    label=u'&Save as', 
                    help=u'Save GriPy Project with a new name',
                    id=wx.ID_SAVEAS, 
                    callback='App.menu_functions.on_save_as'
            ) 
            
            # Inserting a separator...
            UIM.create('menu_item_controller', mc_project.uid, 
                           kind=wx.ITEM_SEPARATOR
            )
            
            mc_import = UIM.create('menu_controller', mc_project.uid, 
                                          label=u"&Import",
                                          help=u"Import file"
            )
           
            UIM.create('menu_item_controller', mc_import.uid, 
                    label=u"LAS File", 
                    help=u'Import a LAS file to current GriPy Project',
                    callback='App.menu_functions.on_import_las'
            )

            UIM.create('menu_item_controller', mc_import.uid, 
                    label=u"ODT File", 
                    help=u'Import a ODT file to current GriPy Project',
                    callback='App.menu_functions.on_import_odt'
            )

            UIM.create('menu_item_controller', mc_import.uid, 
                    label=u"LIS File", 
                    help=u'Import a LIS file to current GriPy Project',
                    callback='App.menu_functions.on_import_lis'
            )            
            
            # TODO: Falta DLis !!!!
            '''
            mic_import_dlis = UIM.create('menu_item_controller', mc_import.uid, 
                    label=u"DLIS File", 
                    help=u'Import a DLIS file to current GriPy Project',
                    callback='App.menu_functions.on_import_dlis'
            )  
            '''

            UIM.create('menu_item_controller', mc_import.uid, 
                    label=u"SEG-Y Well Gather", 
                    help=u'Import a SEG-Y Seismic file as Well Gather',
                    callback='App.menu_functions.on_import_segy_well_gather'
            )  
            

            
            UIM.create('menu_item_controller', mc_import.uid, 
                    label=u"SEG-Y Seismic", 
                    help=u'Import a SEG-Y Seismic file to current GriPy Project',
                    callback='App.menu_functions.on_import_segy_seis'
            )  
            
            UIM.create('menu_item_controller', mc_import.uid, 
                    label=u"SEG-Y Velocity", 
                    help=u'Import a SEG-Y Velocity file to current GriPy Project',
                    callback='App.menu_functions.on_import_segy_vel'
            )  
                   
            mc_export = UIM.create('menu_controller', mc_project.uid, 
                                          label=u"Export",
                                          help=u"Export file"
            )      
            
            UIM.create('menu_item_controller', mc_export.uid, 
                    label=u"LAS File", 
                    help=u'Export a LAS file from a well in current GriPy Project',
                    callback='App.menu_functions.on_export_las'
            )
            # Exit Application
            UIM.create('menu_item_controller', mc_project.uid, 
                           kind=wx.ITEM_SEPARATOR
            )
            UIM.create('menu_item_controller', mc_project.uid, 
                    label=u'Exit', 
                    help=u'Exits GRIPy application.',
                    id=wx.ID_EXIT,
                    callback='App.menu_functions.on_exit'
            )                  
            
            # Edit
            UIM.create('menu_item_controller', mc_edit.uid, 
                    label=u"Partitions", 
                    callback='App.menu_functions.on_partitionedit'
            )    
            UIM.create('menu_item_controller', mc_edit.uid, 
                    label=u"New Rock", 
                    callback='App.menu_functions.on_createrock'
            )    
            #
            
            
            # Well
            UIM.create('menu_item_controller', mc_well.uid, 
                                          label=u"New well",
                                          help=u"Create new well",
                                          callback='App.menu_functions.on_createwell'
            ) 

            UIM.create('menu_item_controller', mc_well.uid, 
                    label=u"Create Synthetic Log",
                    callback='App.menu_functions.on_create_synthetic'
            )
            #
            
            UIM.create('menu_item_controller', mc_debug.uid, 
                    label=u"Debug Console", help=u"Gripy Debug Console", 
                    callback='App.menu_functions.on_debugconsole'
            )    
            UIM.create('menu_item_controller', mc_debug.uid, 
                           kind=wx.ITEM_SEPARATOR
            )
            UIM.create('menu_item_controller', mc_debug.uid, 
                    label=u"Load Wilson Synthetics", 
                    callback='App.menu_functions.on_load_wilson'
            )  
                  


            UIM.create('menu_item_controller', mc_infer.uid, 
                    label=u"Avo PP", 
                    callback='App.menu_functions.teste6'
            )  


            UIM.create('menu_item_controller', mc_infer.uid, 
                    label=u"Avo PP-PS", 
                    callback='App.menu_functions.teste7'
            )  


            UIM.create('menu_item_controller', mc_debug.uid, 
                    label=u"Modeling PP", 
                    callback='App.menu_functions.on_modelling_pp'
            )              

            UIM.create('menu_item_controller', mc_debug.uid, 
                    label=u"Load Stack North Viking Data", 
                    callback='App.menu_functions.teste10'
            )   
            
            UIM.create('menu_item_controller', mc_debug.uid, 
                    label=u"Teste 11", 
                    callback='App.menu_functions.teste11'
            )   
            
            
            #
            UIM.create('menu_item_controller', mc_specdecom.uid, 
                    label=u"Wavelet Transform", 
                    callback='App.menu_functions.teste5'
            )  
            #
            
            

            '''                        
            menubar_ctrl.create_menu_separator('file')
            menubar_ctrl.create_submenu('file', 'import_menu', text=u"Importar",
                                        help=u"Importar arquivo")
            menubar_ctrl.create_menu_item('file', parent_key='import_menu', key='import_las',                             
                                        text=u"&LAS", help=u"Importar arquivo LAS",
                                        callback=self.on_import_las)
            menubar_ctrl.create_menu_item('file', parent_key='import_menu', key='import_odt',                             
                                        text=u"&ODT", help=u"Importar arquivo ODT",
                                        callback=self.on_import_odt)
            menubar_ctrl.create_menu_item('file', parent_key='import_menu', key='import_lis',                             
                                        text=u"&LIS", help=u"Importar arquivo LIS",
                                        callback=self.on_import_lis)     
            menubar_ctrl.create_menu_item('file', parent_key='import_menu', key='import_seis_segy',                             
                            text=u"&SEG-Y Seismic", help=u"Importar arquivo SEG-Y",
                            callback=self.on_import_seis_segy)

            menubar_ctrl.create_menu_item('file', parent_key='import_menu', key='import_vel_segy',                             
                            text=u"&SEG-Y Velocity", help=u"Importar arquivo SEG-Y",
                            callback=self.on_import_vel_segy)                            
                            
            menubar_ctrl.create_menu_item('file', parent_key='import_menu', key='wilson',                             
                            text=u"&Load Wilson Synthetics", help=u"Load Wilson Synthetics",
                            callback=self.on_load_wilson)  
            menubar_ctrl.create_menu_item('file', parent_key='import_menu', key='avo_inv_wells',                             
                            text=u"&Load AVO Inv Wells", help=u"",
                            callback=self.on_load_avo_inv_wells)  
            menubar_ctrl.create_menu_item('file', parent_key='import_menu', key='test_partition',                             
                            text=u"&Load Partition for testing", help=u"",
                            callback=self.on_test_partition)                              
        
            menubar_ctrl.create_submenu('file', 'export_menu', text=u"Exportar",
                                        help=u"Exportar arquivo")        
            menubar_ctrl.create_menu_item('file', parent_key='export_menu', key='export_las',                             
                                        text=u"&LAS", help=u"Exportar arquivo LAS",
                                        callback=self.on_export_las)                                      
            menubar_ctrl.create_menu_separator('file')
            '''
            
            # TODO: VERIFICAR self.OnDoClose
            #menubar_ctrl.create_menu_item('file', key='close', text=u"&Fechar", 
            #                              help=u"Fechar o programa", id=wx.ID_CLOSE,
            #                              callback=self.OnDoClose)     
                      

            # TreeController                                                          
            UIM.create('tree_controller', mwc.uid)                            
                
            
            # ToolBarController 
            tbc = UIM.create('toolbar_controller', mwc.uid)
            
            UIM.create('toolbartool_controller', tbc.uid,
                           label=u"New project", 
                           bitmap='./icons/aqua_new_file_24.png',
                           help='New project', long_help='Start a new Gripy project, closes existing',
                           callback='App.menu_functions.on_open'
            )            
            
            UIM.create('toolbartool_controller', tbc.uid,
                           label=u"Abrir projeto", 
                           bitmap='./icons/folder_opened_24.png',
                           help='Abrir projeto', long_help='Abrir projeto GriPy',
                           callback='App.menu_functions.on_open'
            )
                        
            UIM.create('toolbartool_controller', tbc.uid,
                           label=u"Salvar projeto", 
                           bitmap='./icons/floppy_24.png',
                           help='Salvar projeto', long_help='Salvar projeto GriPy',
                           callback='App.menu_functions.on_save'
            )

            UIM.create('toolbartool_controller', tbc.uid,
                           label=u"Visualizar LogPlot", 
                           bitmap='./icons/log_plot_24.png',
                           help='Log Plot', long_help='Log Plot',
                           callback='App.menu_functions.on_new_logplot' #GripyController.on_plo
            )

            UIM.create('toolbartool_controller', tbc.uid,
                           label=u"Visualizar Crossplot", 
                           bitmap='./icons/crossplot_24.png',
                           help='Crossplot', long_help='Crossplot',
                           #callback='App.menu_functions.on_open' # GripyController.on_crossplot
                           callback='App.menu_functions.on_new_crossplot'
            )         

           
            # StatusBarController  
            UIM.create('statusbar_controller', mwc.uid, 
                label='Bem vindo ao ' + self._gripy_app_state.get('app_display_name')
            )   
            
            #"""
            
            # """
            # Testes 
            # """
            
            #fullfilename = 'C:\\Users\\Adriano\\Desktop\\aaa_teste_2.pgg'
            #self.load_project_data(fullfilename)      
            
            #lpc = UIM.create('logplot_controller', mwc.uid)
            #tc1 = UIM.create('track_controller', lpc.uid)
            #tc1.model.width = 900
            
            #UIM.create('track_controller', lpc.uid)
            #UIM.create('track_controller', lpc.uid)
            
            #UIM.create('track_controller', lpc.uid, overview=True, plotgrid=False)
            
            
            #
            # CASA
            #mwc.model.pos = (-8, 0)
            #mwc.model.size = (1240, 1046)
            #mwc.model.maximized = False
            #
            # BR
            #mwc.model.pos = (-1925, -921) 
            #mwc.model.size = (1116, 1131) 

            # """    
            # Fim - Testes
            # """
            
            
        PM = GripyPluginManagerSingleton.get()
        plugins_places = self._plugins_state.get('plugins_places')
        PM.setPluginPlaces(plugins_places)
        #PM.setPluginPlaces(['Plugins'])
        PM.collectPlugins()   
        
        mwc.view.Show()
        self.SetTopWindow(mwc.view)
        # Here, it is necessary to return True as requested by wx.App         
        return True



    """
    When the MainWindow calls the function below, GripyApp will close UIManager 
    but not finish the wx.App.
    This job must be done by Wx. (don't try to change it!)
    """
    def PreExit(self):
        msg = 'GriPy Application is preparing to terminate....'
        log.info(msg)
        print '\n', msg
        OM = ObjectManager(self)
        if OM.get_changed_flag():
            dial = wx.MessageDialog(self.GetTopWindow(), 
                                    'Do you want to save your project?', 
                                    'GriPy', 
                                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
            )
            if dial.ShowModal() == wx.ID_YES:
                self.on_save()   
        #
        self.reset_ObjectManager()
        #
        app_UI_filename = self._gripy_app_state.get('app_UI_file')
        self.save_UI_application_data(app_UI_filename)

        user_UI_filename = self._gripy_app_state.get('user_UI_file')
        self.save_UI_user_data(user_UI_filename)
        
        
        # This time I choose not use the line below because there was a little
        # freeze on exiting (1-2 seconds). Then I opted delegate it do compiler.
        #UIM = UIManager()      
        #UIM.close()
        UIM = UIManager()  
        UIM.PreExit()
        
        # As indicated by https://forums.wxwidgets.org/viewtopic.php?t=32138        
        aui_manager = wx.aui.AuiManager.GetManager(self.GetTopWindow())
        aui_manager.UnInit()        
        
        
    def OnExit(self):
        msg = 'GriPy Application has finished.'
        log.info(msg)
        print msg, '\n'
        return super(GripyApp, self).OnExit()
        
    # Convenience function    
    def getLogger(self):    
        return log
        
    # Convenience function    
    def getPluginManager(self):
        return GripyPluginManagerSingleton.get()
        
    
    def reload_state(self):
        self._gripy_app_state['app_name'] = self.GetAppName()
        self._gripy_app_state['app_display_name'] = self.GetAppDisplayName()
        self._gripy_app_state['app_version'] = self.__version__
        self._gripy_app_state['class_name'] = self.GetClassName()
        self._gripy_app_state['vendor_name'] = self.GetVendorName()
        self._gripy_app_state['vendor_display_name'] = self.GetVendorDisplayName()
          
          
    def get_app_full_name(self):
        if not self._inited:
            raise Exception('GripyApp has not initializated.')
        return self.GetAppName() + ' ' + self.__version__   


    def _init_has_ended_message(self):
        _app_name = self.get_app_full_name()    
        log.info('Welcome to {}.'.format(_app_name))
        log.info('{} was initializated. Settings loaded are:'.format(_app_name))
        _state = self._get_state_dict()
        for key, value in _state.items():
            msg = '    ' + str(key) + ' = ' + str(value)
            log.info(msg)
        

    def _get_state_dict(self):
        class_full_name = app_utils.get_class_full_name(self)
        _state = OrderedDict()
        _state['wx.App'] = self._wx_app_state
        _state[class_full_name] = self._gripy_app_state
        _state['logging'] = self._logging_state
        return _state        


    def on_save(self):
        if self.get_project_filename():
            disableAll = wx.WindowDisabler()
            wait = wx.BusyInfo("Saving GriPy project. Wait...")
            self.save_project_data()
            del wait
            del disableAll
        else:
            self.on_save_as()
        
    
    def on_save_as(self):
        if self.get_project_filename():
            dir_name, file_name = os.path.split(self.get_project_filename())
        style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        wildcard = "Arquivo de projeto do GRIPy (*.pgg)|*.pgg"
        fdlg = wx.FileDialog(self.GetTopWindow(), 
                             'Escolha o arquivo PGG', 
                            #dir_name, file_name, 
                            wildcard=wildcard, style=style
        )
        if fdlg.ShowModal() == wx.ID_OK:
            file_name = fdlg.GetFilename()
            dir_name = fdlg.GetDirectory()
            if not file_name.endswith('.pgg'):
                file_name += '.pgg'
            disableAll = wx.WindowDisabler()
            wait = wx.BusyInfo("Saving GriPy project. Wait...")    
            self.save_project_data(os.path.join(dir_name, file_name))
            del wait
            del disableAll
        fdlg.Destroy()   


    def reset_ObjectManager(self):
        OM = ObjectManager(self)
        OM._reset()
