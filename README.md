# pySOFA
This is a Python API for SOFA (Spatially Oriented Format for Acoustics).

## Usage
```python
import  pysofa
sofaobject = pysofa.SOFA("path/to/sofa_file.sofa")
```

The SOFA object implements the specifications in form of a hierarchical object.
The Attribute `ListenerDescription` for example, can be accessed as `sofaobject.Listener.Description` 
and `ReceiverPosition` can be accessed as `sofaobject.Receiver.Position`.

## Limitations
The API is currently read-only and implements the FIR Datatype. The package was implemented for a specific project and only implements the features that where neccessary for that project, but it should be easy to extend the API for all other Datatypes. Feel free to contact the author or to submit a bug report if you are missing any feature.
