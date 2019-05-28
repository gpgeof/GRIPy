
from collections import OrderedDict

from classes.om import OMBaseObject
from classes.om import DataObject


class Log(DataObject):
                                  
    tid = "log"
    _FRIENDLY_NAME = 'Log'
    
    _ATTRIBUTES = OrderedDict()
    _ATTRIBUTES['index_uid'] = {
        'default_value': None,
        'type': str       
    }  
    
    _SHOWN_ATTRIBUTES = [
                            ('datatype', 'Curve Type'),
                            ('unit', 'Units'),
                            ('min', 'Min Value'),
                            ('max', 'Max Value')
                            #('index_name', 'Index'),
                            #('start', 'Start'),
                            #('end', 'End'),
                            #('step', 'Step'),
    ] 
    
    
    def __init__(self, data, **attributes):
        super().__init__(data, **attributes) 

                 
    @classmethod
    def _is_tree_tid_node_needed(cls):
        #From matplotlib.docstring.py 
        #@_autogen_docstring(Axes.plot)
        #@_autogen_docstring(OMBaseObject._is_tree_tid_node_needed)
        __doc__ = OMBaseObject._is_tree_tid_node_needed.__doc__
        return False
#    _is_tree_tid_node_needed.__doc__ = OMBaseObject._is_tree_tid_node_needed.__doc__
    
    
    # https://docs.scipy.org/doc/numpy-1.15.0/docs/howto_document.html
    
    # TODO: Usar Sphinx, como modelo abaixo do MPL - confirmar visitando respectiva pagina do MPL
    # neste caso eh a pagina Artist.set_clip_path do docs online.
    




    
    #def __init__(self, *args, **kwargs):   
    def __init__(self, data, **attributes):
#        print ('\nattributes:', attributes)
        """
        index_set_uid = attributes.get('index_set_uid')
        try:    
            tid, oid = index_set_uid 
        except:
            print (index_set_uid, type(index_set_uid))										
            raise Exception('Object attribute \"index_set_uid\" must be a \"uid\" tuple.')    
        if tid != 'index_set':
            raise Exception('Object attribute \"index_set_uid\" must have its first argument as \"index_set\".')
        """
        super().__init__(data, **attributes) 

#        OM = ObjectManager()        
#        OM.subscribe(self._on_OM_add, 'add')

    """
    def _on_OM_add(self, objuid):
        if objuid != self.uid:
            return
        #print 'WellData1D._on_OM_add:', objuid
        OM = ObjectManager()
        try:
            OM.unsubscribe(self._on_OM_add, 'add')     
        except Exception as e:
            print ('Deu ruim no unsub:', e)
        try:
            parent_uid = OM._getparentuid(self.uid)
            # TODO: remover esse armengue
            if self.tid == 'part':
                parent_well_uid = OM._getparentuid(parent_uid)
            else:
                parent_well_uid = parent_uid
            # FIM - Armengue    
        #    print 'parent_well_uid:', parent_well_uid
            my_index_set = OM.get(self.index_set_uid)
        #    print 'my_index_set:', my_index_set
        #    print 'list:'
        #    for obj_is in OM.list('index_set', parent_well_uid):
        #        print obj_is
            if my_index_set not in OM.list('index_set', parent_well_uid):
                print ('DEU RUIM')
                raise Exception('Invalid attribute \"index_set\"={}'.format(self.index_set_uid))
        except:
            raise

    @property
    def index_set_uid(self):
        return self.attributes['index_set_uid']
    """

    def get_data_indexes(self):
        ret_dict = OrderedDict()
        OM = ObjectManager()
#        print (self.__dict__)
        
        index_uid = parse_string_to_uid(self.index_uid)
        index = OM.get(index_uid)

        ret_dict[0] = [index]
        return ret_dict  

    """
    def get_data_indexes(self):
        OM = ObjectManager()    
        
        
        try:
            index_set = OM.get(self.index_set_uid)
            return index_set.get_data_indexes()
        except:
            return None
    """    
        
#    def get_indexes(self):
#        raise Exception('Invalid METHOD')   
    
    def get_friendly_name(self):
        OM = ObjectManager()
        parent_well_uid = OM._getparentuid(self.uid)
        parent_well = OM.get(parent_well_uid)         
        return self.name + '@' + parent_well.name






    
    """
    Set the artist's clip path, which may be:

    - a :class:`~matplotlib.patches.Patch` (or subclass) instance; or
    - a :class:`~matplotlib.path.Path` instance, in which case a
      :class:`~matplotlib.transforms.Transform` instance, which will be
      applied to the path before using it for clipping, must be provided;
      or
    - ``None``, to remove a previously set clipping path.

    For efficiency, if the path happens to be an axis-aligned rectangle,
    this method will set the clipping box to the corresponding rectangle
    and set the clipping path to ``None``.

    ACCEPTS: [(`~matplotlib.path.Path`, `.Transform`) | `.Patch` | None]
        """    
    
    
    '''
    #From matplotlib.axes._base.py line 3152
    
    get_xscale.__doc__ = "Return the xaxis scale string: %s""" % (
    ", ".join(mscale.get_scale_names()))
    
    Written after function
    
    '''
    
    '''
    #From matplotlib.pyplot.py 
    
    def _autogen_docstring(base):
    """Autogenerated wrappers will get their docstring from a base function
    with an addendum."""
    #msg = "\n\nAdditional kwargs: hold = [True|False] overrides default hold state"
    msg = ''
    addendum = docstring.Appender(msg, '\n\n')
    return lambda func: addendum(docstring.copy_dedent(base)(func))
    '''