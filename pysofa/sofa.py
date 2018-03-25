import tables as tbls
from warnings import simplefilter

class FIR(object):
    '''Object to hold and read the information for an FIR Object as defined by the Sofa specifications.

    Parameters
    ----------
    sofa_file : tables.file.File or str, optional.
      if not None, the information is directly read from a SOFA file.
      This file can be provieded as a PyTables file object or
      path to a SOFA HDF file. (default=None)

    '''
    def __init__(self, sofa_file=None):
        if sofa_file:
            self.from_file(sofa_file)

    def from_file(self, sofa_file):
        # If it is allready a pyTables handle, use that, if it is a
        # file name, open the file
        if not isinstance(sofa_file, tbls.file.File):
            assert isinstance(sofa_file, str)
            tblsfile = tbls.open_file('dtf_nh2.sofa')
        else:
            tblsfile = sofa_file

        datasets = ['Data.IR', 'Data.Delay', 'Data.SamplingRate']

        for param in datasets:
            _add_data(self, tblsfile, '/' + param, name=param[5:],
                      required=True)

        attributes = ['Units']

        # The attribute name should contain Position
        for param in attributes:
            _add_attribute(self, tblsfile, '/' + 'Data.SamplingRate',
                           param, name='SamplingRate'+param,
                           required=True)


        # If the file was opened within this function, close it.
        if not isinstance(sofa_file, tbls.file.File):
            tblsfile.close()


class AudioObject(object):
    '''Object to hold and read the information for an Audio Object as
       defined by the Sofa specifications.

    Examples for Audio Objects are: listener, reciver, source, emitter.

    Parameters
    ----------
    object_string : str
      The name of the node as well as the description of the audio object
      (e.g Reciver).
    sofa_file : tables.file.File or str, optional.
      if not None, the information is directly read from a SOFA file.
      This file can be provieded as a PyTables file object or
      path to a SOFA HDF file.

    '''
    def __init__(self, object_string, sofa_file=None):
        self.object_string = object_string
        if sofa_file:
            self.from_file(sofa_file)

    def from_file(self, sofa_file):
        '''Read Object definition from a SOFA file.

        Parameters:
        -----------
        sofa_file : tables.file.File or str, optional.
          File form which to read the information.  This file can be
          provieded as a PyTables file object or path to a SOFA HDF file.

        '''
        # If it is allready a pyTables handle, use that, if it is a
        # file name, open the file
        if not isinstance(sofa_file, tbls.file.File):
            assert isinstance(sofa_file, str)
            tblsfile = tbls.open_file('dtf_nh2.sofa')
        else:
            tblsfile = sofa_file

        required_datasets = ['Position']

        #The attribute name should not contain Listener
        for param in required_datasets:
            _add_data(self, tblsfile, '/' + self.object_string + param,
                      name=param, required=True)

        req_attributes = ['Type', 'Units']

        # The attribute name should contain Position
        for param in req_attributes:
            _add_attribute(self, tblsfile, '/' + self.object_string + 'Position',
                           param, name='Position'+param,
                           required=True)

        other_datasets = ['Description', 'View', 'Up']

        #The attribute name should not contain Listener
        for param in other_datasets:
            _add_data(self, tblsfile, '/' + self.object_string + param, name=param,
                      required=False)


        # If the file was opened within this function, close it.
        if not isinstance(sofa_file, tbls.file.File):
            tblsfile.close()

    def __repr__(self):
        string = ("%i " +  self.object_string) % len(self.Position)
        return string

    def __len__(self):
        return len(self.Position)

def _add_data(object, tblsfile, node, required=False, name=None):
    '''Adds a dataset to a given object.

    Parameters
    ----------
    object : pySofa object
      The object to which the attribute should be added
    tblsfile : tables.file.File
      PyTables file object to read from.
    node : str
      Path to the node from which to read the data
    required : bool, optional
      decides whether an exception is raised if the node does not
      exist. (default=False)
    name : str or None, optional
      If None, the `node` parameter will be used to determine the
      name of the attribute added to the object. Otherwise, a name can be
      determined using this parameter. (default=None)

    Returns
    -------
    int :
      0 if dataset exists.
      1 if dataset does not exist.

    '''
    try:
        value = tblsfile.get_node(node).read()
        if not name:
            name = node
        setattr(object, name, value)
        return 0
    except AttributeError:
        if required:
            raise Exception('Required Dataset ' + node + ' not found!')
        return 1


def _add_attribute(object, tblsfile, node, attribute, required=False, name=None):
    '''Adds an attribute stored in form of metadata info to a given object.

    Parameters
    ----------
    object : pySofa object
      The object to which the attribute should be added
    tblsfile : tables.file.File
      PyTables file object to read from.
    node : str
      Path to the node from which to read the attribute
    attribute : str
      Name of the attribute to read
    required : bool, optional
      decides whether an exception is raised if the attribute does not
      exist. (default=False)
    name : str or None, optional
      If None, the `attirbute` parameter will be used to determine the
      name of the attribute added to the object. Otherwise, a name can be
      determined using this parameter. (default=None)

    Returns
    -------
    int :
      0 if Attribute exists.
      1 if Attribute does not exist.

    '''
    try:
        value = tblsfile.get_node_attr(node, attribute)
        if not name:
            name = attribute
        setattr(object, name, value)
        return 0
    except AttributeError:
        if required:
            raise Exception('Required Attribute ' + attribute + ' not found!')
        return 1



class SOFA(object):
    '''Main Object to hold and read the information of a whole SOFA file.

    Parameters
    ----------
    sofa_file : tables.file.File or str, optional.
      if not None, the information is directly read from a SOFA file.
      This file can be provieded as a PyTables file object or
      path to a SOFA HDF file. (default=None)

    '''
    def __init__(self, sofa_file=None):
        if sofa_file:
            self.from_file(sofa_file)

    def from_file(self, sofa_file):
        if not isinstance(sofa_file, tbls.file.File):
            assert isinstance(sofa_file, str)
            tblsfile = tbls.open_file(sofa_file)
        else:
            tblsfile = sofa_file

        # Supress DataType Warnings
        simplefilter("ignore")

        # List of the Attributes that are required by the SOFA specivication
        req_attributes = ['Conventions', 'Version', 'SOFAConventions',
                          'SOFAConventionsVersion', 'DataType',
                          'RoomType', 'Title', 'DateCreated',
                          'DateModified', 'APIName', 'APIVersion',
                          'AuthorContact', 'Organization', 'License']

        for param in req_attributes:
            _add_attribute(self, tblsfile, '/', param, required=True)

        # List of the non-required attributes.
        other_attributes = ['ApplicationName', 'ApplicationVersion',
                            'Comment', 'History', 'References',
                            'Origin']

        for param in other_attributes:
            _add_attribute(self, tblsfile, '/', param)

        # read information about the three required Audio Objects
        self.listener = AudioObject('Listener', tblsfile)
        self.source = AudioObject('Source', tblsfile)
        self.receiver = AudioObject('Receiver', tblsfile)
        self.emitter = AudioObject('Emitter', tblsfile)

        # Read the Data included in the SOFA file
        if self.DataType == 'FIR':
            self.data = FIR(tblsfile)
        else:
            raise Exception('Currently only the Datatype FIR is Implemented')

        if not isinstance(sofa_file, tbls.file.File):
            tblsfile.close()
