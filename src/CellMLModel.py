from ordered_set import OrderedSet
from anytree import NodeMixin
import xml.etree.ElementTree as ET
class cellMLNodeBase(object):
    """Base class for CellML nodes."""
    def __init__(self):
        """Initialise the CellML node."""

class Model(cellMLNodeBase, NodeMixin):
    """Class to store a CellML model, the top-level element of a CellML file. Every model element MUST contain a name attribute.
    A model element MAY contain one or more additional specific element children, each of which MUST be of one of the following types:
    A component element; A connection element; An encapsulation element; An import element; or A units element.
    A model element MUST NOT contain more than one encapsulation elements."""

    BUILTIN_UNITS = ['ampere', 'becquerel', 'candela', 'celsius', 'coulomb', 'dimensionless', 'farad', 'gram', 'gray', 'henry', 'hertz', 'item', 'joule', 'katal', 'kelvin', 'kilogram',
    'liter' 'litre', 'lumen', 'lux', 'metre', 'meter', 'mole', 'newton', 'ohm', 'pascal', 'radian', 'second', 'siemens', 'sievert', 'steradian', 'tesla', 'volt', 'watt', 'weber']
    
    def __init__(self, name, parent=None, children=None):
        """Initialise the CellML model."""
        super(cellMLNodeBase, self).__init__()
        self.name = name   
        self.parent = parent
        self._children = children

    @property
    def children(self):
        """Return the children of the model."""
        return self._children
    @children.setter
    def children(self, children):
        """Set the children of the model."""
        # Check that the children are of the correct type
        for child in children:
            if not isinstance(child, (Component, Connection, Encapsulation, Import, Units)):
                raise TypeError(f'Child {child} is not a valid CellML model child type.')
            else:
                self._children = children
     
    @property
    def components(self):
        """Return the components in the model."""
        return [child for child in self.children if isinstance(child, Component)]
    @property
    def units(self):
        """Return the units in the model."""
        return [child for child in self.children if isinstance(child, Units)]
    @property
    def imports(self):
        """Return the imports in the model."""
        return [child for child in self.children if isinstance(child, Import)]
    @property
    def Import_components(self):
        """Return the imported components in the model."""
        imported_components = []
        for child in self.imports:
            imported_components += child.components
        return imported_components
    @property
    def connections(self):
        """Return the connections in the model."""
        pairs = [child for child in self.children if isinstance(child, Connection)]
        # Check for duplicates and raise an error if there are any.
        if len(pairs) != len(set(pairs)):
            # get the duplicate pairs
            duplicate = [item for item in pairs if pairs.count(item) > 1]
            raise ValueError(f"Duplicate connection pairs in the model: {duplicate}.")
        else:
            return pairs
    @property
    def encapsulation(self):
        """Return the encapsulation in the model."""
        for child in self.children:
            if isinstance(child, Encapsulation):
                return child
    
    # Get all the namespace of the components and imported components in the model.
    @property
    def component_namespace(self):
        """Return the component namespaces in the model."""
        namespace = []
        for item in self.components:
            namespace += [item.name]
        for item in self.Import_components:
            namespace += [item.name]
        # Check for duplicates and raise an error if there are any.
        if len(namespace) != len(set(namespace)):
            # get the duplicate namespace
            duplicate = [item for item in namespace if namespace.count(item) > 1]
            raise ValueError(f"Duplicate component namespaces in the model: {duplicate}.")
        else:
            return namespace
    # Get all the namespace of the units needed in the model.
    @property
    def units_namespace(self):
        """Return the units that need to be imported. All the units that are not defined in the model minus the BUILTIN_UNITS."""
        units = OrderedSet()
        for component in self.components:
            for variable in component.variables:
                if variable.units not in self.BUILTIN_UNITS:
                    units.add(variable.units)
        return units
    # Get all the namespace of the units defined in the model.
    @property
    def units_defined(self):
        """Return the units defined in the model."""
        units = []
        for item in self.units:
            units += item.name
        return units

    def cellMLText(self,filename):
        """Return the cellMLTextView representation of the model."""
        cellML = f'def model {self.name} as \n'
        for import_ in self.imports:
            cellML += import_.cellMLText()
        for units in self.units:
            cellML += units.cellMLText()
        for component in self.components:
            cellML += component.cellMLText()
        if self.encapsulation is not None:
            cellML += self.encapsulation.cellMLText()
        for connection in self.connections:
            cellML += connection.cellMLText()
        cellML += f'enddef; \n'
        with open(f'{filename}.txt', 'w') as cid:
           cid.writelines(cellML)
        cid.close() 

    def cellML(self,filename):
        """Using xml.etree.ElementTree to build XML documents (cellml/1.1#)"""
        # Create the root element
        root = ET.Element('model', attrib={'name':self.name})
        # Add the namespace
        root.set('xmlns', 'http://www.cellml.org/cellml/1.1#')
        root.set('xmlns:cellml', 'http://www.cellml.org/cellml/1.1#')
        root.set('xmlns:mathml', 'http://www.w3.org/1998/Math/MathML')
        root.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        # Add the children as subelements
        for child in self.children:
            if isinstance(child, Import):
                child_element=ET.SubElement(root, 'import', attrib={'xlink:href': child.href})
                child_element.tail = "\n" 
                # Add the grandchildren as subelements
                for grandchild in child.children:
                    # Add the import component as subelements
                    # Add the import units as subelements
                    if isinstance(grandchild, Import_component):
                        grandchild_element=ET.SubElement(child_element, 'component', attrib={'name': grandchild.name,'component_ref': grandchild.component_ref})
                    elif isinstance(grandchild, Import_units):
                        grandchild_element=ET.SubElement(child_element, 'units', attrib={'name': grandchild.name,'units_ref': grandchild.units_ref})
                    grandchild_element.tail = "\n"
            elif isinstance(child, Units):
                child_element=ET.SubElement(root, 'units', attrib={'name': child.name})
                child_element.tail = "\n"
                # Add the grandchildren as subelements
                for grandchild in child.children:
                    # Add the unit as subelements
                    if isinstance(grandchild, Unit):
                        grandchild_element=ET.SubElement(child_element, 'unit', attrib={'units': grandchild.units})
                        grandchild_element.tail = "\n"
                        if grandchild.prefix is not None:
                            grandchild_element.set('prefix', grandchild.prefix)
                        if grandchild.exponent is not None:
                            grandchild_element.set('exponent', grandchild.exponent)
                        if grandchild.multiplier is not None:
                            grandchild_element.set('multiplier', grandchild.multiplier)
                        if grandchild.offset is not None:
                            grandchild_element.set('offset', grandchild.offset)                        
            elif isinstance(child, Component):
                child_element=ET.SubElement(root, 'component', attrib={'name': child.name})
                child_element.tail = "\n"
                # Add the grandchildren as subelements
                for grandchild in child.children:
                    # Add the variable as subelements
                    if isinstance(grandchild, Variable):
                        grandchild_element=ET.SubElement(child_element, 'variable', attrib={'name': grandchild.name,'units': grandchild.units})
                        grandchild_element.tail = "\n"
                        if grandchild.public_interface is not None:
                            grandchild_element.set('public_interface', grandchild.public_interface)
                        if grandchild.private_interface is not None:
                            grandchild_element.set('interface', grandchild.private_interface)
                        if grandchild.initial_value is not None:
                            grandchild_element.set('initial_value', grandchild.initial_value)
                    # Add the math as subelements
                    elif isinstance(grandchild, Math):
                        grandchild_element=ET.SubElement(child_element, 'math', attrib={'xmlns': 'http://www.w3.org/1998/Math/MathML'})
                        grandchild_element.tail = "\n"
                        grandchild_element.text = grandchild.math
            elif isinstance(child, Connection):
                # Add the connection as subelements, <connection>  </connection>
                child_element=ET.SubElement(root, 'connection')
                child_element.tail = "\n"
                grandchild_element=ET.SubElement(child_element, 'map_components', attrib={'component_1': child.component_1.name,'component_2': child.component_2.name})
                grandchild_element.tail = "\n"                
                # Add the grandchildren as subelements
                for grandchild in child.children:
                    # Add the map_variables as subelements
                    if isinstance(grandchild, Map_variables):
                        grandchild_element=ET.SubElement(child_element, 'map_variables', attrib={'variable_1': grandchild.variable_1,'variable_2': grandchild.variable_2})
                        grandchild_element.tail = "\n"
            elif isinstance(child, Encapsulation):
                child_element=ET.SubElement(root, 'group')
                child_element.tail = "\n"                
                # Add         <relationship_ref relationship="encapsulation"/>
                grandchild_element=ET.SubElement(child_element, 'relationship_ref', attrib={'relationship': 'encapsulation'})
                grandchild_element.tail = "\n"
                
                # Add the grandgrandchildren as subelements recursively
                # Define a recursive function to add <component_ref component="C0_S2"> and its children
                def add_component_ref(parent, parent_element):
                    if parent.children is not None:
                       for grandgrandchild in parent.children:
                           # Add the component_ref as subelements
                           if isinstance(grandgrandchild, Component_ref):
                               grandgrandchild_element=ET.SubElement(parent_element, 'component_ref', attrib={'component': grandgrandchild.component})
                               grandgrandchild_element.tail = "\n"                               
                               # Add the grandgrandgrandchildren as subelements recursively
                               add_component_ref(grandgrandchild, grandgrandchild_element)
   
                add_component_ref(child, child_element)

        # Write the XML to a file with indentation

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(filename, encoding='utf-8', xml_declaration=True)

class Encapsulation(cellMLNodeBase, NodeMixin):
    """Class to store a CellML encapsulation, as a child of a model element."""
    # The root level component_ref is the encapsulation.
    def __init__(self,parent=None, children=None):
        """Initialise the CellML encapsulation."""
        super(cellMLNodeBase, self).__init__()
        self._parent = parent
        if children:
            self._children = children
        
    @property
    def parent(self):
        """Return the parent of the encapsulation."""
        return self._parent
    @parent.setter
    def parent(self, value):
        if value is None:
            self._parent = value
        elif not isinstance(value, Model):
            raise TypeError("Parent must be of type CellMLModel.")
        else:
            self._parent = value
    
    @property
    def children(self):
        """Return the component references of the encapsulation."""
        return self._children
    @children.setter
    def children(self, value):
        if value is None:
            self._children = value
        elif any(not isinstance(item, Component_ref) for item in value):
            raise TypeError("Children must be of type CellMLComponent_ref.")
        else:
            self._children = value            
    # Get all the namespace of the components and component references in the encapsulation.
    @property
    def namespace(self):
        """Return the namespaces of the encapsulation."""
        namespace = []
        for item in self.component_ref:
            namespace += item.namespace
        # Check for duplicates and raise an error if there are any.
        if len(namespace) != len(set(namespace)):
            # get the duplicate namespace
            duplicate = [item for item in namespace if namespace.count(item) > 1]
            raise ValueError(f"Duplicate component namespaces in the encapsulation: {duplicate}.")
        else:
            return namespace

    def cellMLText(self):
        """Return the cellMLTextView representation of the encapsulation."""
        if self.parent is not None:
           cellML = 'def group as encapsulation for \n'
           for item in self.children:
               cellML += item.cellMLText()
           cellML += 'enddef; \n'
           return cellML

class Component_ref(cellMLNodeBase, NodeMixin):
    """Class to store a CellML component reference, as a child of an encapsulation element."""
    def __init__(self, component, parent=None, children=None):
        """Initialise the CellML component reference."""
        super(cellMLNodeBase, self).__init__()
        self.component = component
        self._parent = parent
        self._children = children

    @property
    def parent(self):
        """Return the parent of the component reference."""
        return self._parent
    @parent.setter
    def parent(self, value):
        """Set the parent of the component reference."""
        if value is None:
            self._parent = value
        elif not isinstance(value, (Encapsulation,Component_ref)):
            raise ValueError("Parent must be a CellML encapsulation or component references.")
        else:
            self._parent = value
    
    @property
    def children(self):
        """Return the component reference of the component reference."""
        return self._children
    @children.setter
    def children(self, value):
        """Set the component reference of the component reference."""
        if value is None:
            self._children = value
        elif any(not isinstance(item, Component_ref) for item in value):
            raise ValueError("All items must be CellML component references.")
        else:
            self._children = value
    # Get all the namespace of the components and component references.
    @property
    def namespace(self):
        """Return the namespace of the component reference."""
        namespace = []
        if self.children is not None:
            for item in self.children:
                namespace += item.component
        namespace.append(self.component)
        # Check for duplicates and raise an error if there are any.
        if len(namespace) != len(set(namespace)):
            # get the duplicate namespace
            duplicate = [item for item in namespace if namespace.count(item) > 1]
            raise ValueError(f"Duplicate component namespace in the component references: {duplicate}.")
        else:
            return namespace

    def __eq__(self,other) :
        return (self.children == other.children and self.component == other.component)

    def __hash__(self):
        return hash(self.children) + hash(self.component)

    def cellMLText(self):
        """Return the CellML representation of the component reference."""
        if self.children is not None:
            cellML = f'comp {self.component} incl \n'
            for component_ref in self.children:
                cellML += component_ref.cellMLText()
            cellML += f'endcomp; \n'
        else: cellML = f'comp {self.component}; \n'
        return cellML

class Component(cellMLNodeBase, NodeMixin):
    """Class to store a CellML component, as a child of a model element."""
    def __init__(self, name, parent=None, children=None):
        """Initialise the CellML component."""
        super(cellMLNodeBase, self).__init__()
        self.name = name
        self._parent = parent
        self._children = children
    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, value):
        if value is None:
            self._parent = value
        elif not isinstance(value, Model):
            raise TypeError("Parent must be of type CellMLModel.")
        else:
            self._parent = value

    @property
    def children(self):
        return self._children
    @children.setter
    def children(self, value):
        if any (not isinstance(item, (Variable, Math)) for item in value):
            raise TypeError("Children must be of type CellMLVariable or CellMLMath.")
        else:
            # Check the repeated children
            if len(value) != len(set(value)):
                # get the duplicate children
                duplicate = [item for item in value if value.count(item) > 1]
                raise ValueError(f"Duplicate children in the component: {duplicate}.")
            else:
                self._children = value
                for item in value:
                    item.parent = self
    @property
    def variables(self):
        return [item for item in self.children if isinstance(item, Variable)]
    @property
    def equations(self):
        return [item for item in self.children if isinstance(item, Math)]
    @property
    def variable_namespace(self):
        namespace = [item.name for item in self.children if isinstance(item, Variable)]
        if len(namespace) != len(set(namespace)):
            # get the duplicate namespace
            duplicate = [item for item in namespace if namespace.count(item) > 1]
            raise ValueError(f"Duplicate variable namespace in the component: {duplicate}.")
        else:
            return namespace
    def __eq__(self, other):
        """Check if two components are equal."""
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        """Hash a component."""
        return hash(self.name)

    def __str__(self):
        """String representation of a component."""
        # Return all the attributes of the component
        return f"Component {self.name} with variables {self.variable_namespace}."
    
    def __dir__(self):
        """Return the attributes of a component."""
        return ['name','variables','math','variable_namespace']

    def cellMLText(self):
        """Return the cellMLTextView representation of the component."""
        cellML = f'def comp {self.name} as \n'
        for variable in self.children:
            cellML += variable.cellMLText()+" \n"
        cellML += f'enddef; \n'
        return cellML
  
class Connection(cellMLNodeBase, NodeMixin):
    """Class to store a CellML connection, as a child of a model element."""
    def __init__(self,component_1,component_2, parent=None, children=None):
        """Initialise the CellML connection."""
        super(cellMLNodeBase, self).__init__()
        if component_1!=component_2:
            self.component_1 = component_1
            self.component_2 = component_2
            self._parent = parent
            self._children = children
        else:
            raise ValueError(f"Connection components {component_1.name} and {component_2.name} are the same.")
    @property
    def parent(self):
        """Return the parent of the connection."""
        return self._parent
    @parent.setter
    def parent(self, value):
        """Set the parent of the connection."""
        if value is None:
            self._parent = value
        elif not isinstance(value, Model):
            raise TypeError("Parent must be of type CellMLModel.")
        else:
            self._parent = value
    @property
    def children(self):
        """Return the children of the connection."""
        return self._children
    @children.setter
    def children(self, value):
        """Set the children of the connection."""
        if any(not isinstance(item, Map_variables) for item in value):
            raise TypeError("Children must be of type CellMLMap_variables.")
        else:
            # Check the repeated children
            if len(value) != len(set(value)):
                # get the duplicate children
                duplicate = [item for item in value if value.count(item) > 1]
                raise ValueError(f"Duplicate children in the connection: {duplicate}.")
            else:
                for item in value:
                    if item.variable_1 not in self.component_1.variable_namespace or item.variable_2 not in self.component_2.variable_namespace:
                        raise ValueError(f"Map_variables {item.variable_1} and {item.variable_2} are not in the correct components.")
                    item.parent = self
                self._children = value       

    def __eq__(self, other):
        """Check if two connections are equal."""
        if isinstance(other, self.__class__):
            return self.component_1.name == other.component_1.name and self.component_2.name == other.component_2.name
        else:
            return False

    def __hash__(self):
        """Hash a connection."""
        return hash((self.component_1.name, self.component_2.name))

    def __str__(self):
        """String representation of a connection."""
        return f"{self.component_1.name} <-> {self.component_2.name}"

    def __contains__(self, item):
        """Check if a connection contains a map_variable."""
        return item in self.children

    def __getitem__(self, key):
        """Get a component_1 from a connection."""
        if key == 'comp1':
            return self.component_1.name
        elif key == 'comp2':
            return self.component_2.name
        else:
            raise KeyError(f"Connection key {key} not recognised.")  

    def cellMLText(self):
        """Return the cellMLTextView representation of a connection."""
        cellML = f"def map between {self.component_1.name} and {self.component_2.name} for \n"
        for map_variables in self.children:
            cellML += map_variables.cellMLText()
        cellML += f'enddef; \n'
        return cellML

class Map_variables(cellMLNodeBase, NodeMixin):
    """Class to store a CellML map_variable, as a child of a connection element."""
    def __init__(self, variable_1,variable_2, parent=None, children=None):
        """Initialise the CellML map_variable."""
        super(cellMLNodeBase, self).__init__()
        self.variable_1 = variable_1
        self.variable_2 = variable_2
        self._parent = parent
        if children:
            self.children = children

    @property
    def parent(self):
        """Get the parent of a map_variable."""
        return self._parent
    @parent.setter
    def parent(self, value):
        """Set the parent of a map_variable."""
        if value is None:
            self._parent = value
        elif isinstance(value, Connection):
            self._parent = value
        else:
            raise TypeError("Parent must be of type Connection.")

    def __eq__(self, other):
        """Check if two map_variables are equal."""
        if isinstance(other, self.__class__):
            return self.variable_1 == other.variable_1 and self.variable_2 == other.variable_2
        else:
            return False

    def __hash__(self):
        """Hash a map_variable."""
        return hash((self.variable_1, self.variable_2))

    def __str__(self):
        """String representation of a map_variable."""
        return f"{self.variable_1} <-> {self.variable_2}"

    def cellMLText(self):
        """Return the CellMLTextView representation of a map_variable."""
        return f"vars {self.variable_1} and {self.variable_2}; \n"

class Import(cellMLNodeBase, NodeMixin):
    """Class to store a CellML import, as a child of a model"""
    def __init__(self, href, parent=None, children=None):
        """Initialise the CellML import."""
        super(cellMLNodeBase, self).__init__()
        self.href = href
        self._parent = parent
        if children:
            self._children = children

    @property
    def parent(self):
        """Get the parent of the import."""
        return self._parent
    @parent.setter
    def parent(self, value):
        """Set the parent of the import."""
        if value is None:
            self._parent = value
        elif not isinstance(value, Model):
            raise TypeError("Parent must be of type CellMLModel.")
        else:
            self._parent = value
    @property
    def children(self):
        """Get the children of the import."""
        return self._children
    @children.setter
    def children(self, value):
        """Set the children of the import."""
        if any(not isinstance(item, (Import_component,Import_units)) for item in value):
            raise TypeError("Children must be of type CellMLImport_component or CellMLImport_units.")
        else:
            # Check the repeated children
            if len(value) != len(set(value)):
                # get the duplicate children
                duplicate = [item for item in value if value.count(item) > 1]
                raise ValueError(f"Duplicate children in the import: {duplicate}.")
            else:
                self._children = value            
                for item in self._children:
                    item.parent = self

    @property
    def components(self):
        """Get the components imported by the import."""
        return [item for item in self.children if isinstance(item, Import_component)]
    @property
    def units(self):
        """Get the units imported by the import."""
        return [item for item in self.children if isinstance(item, Import_units)]

    def __eq__(self, other):
        """Check if two imports are equal."""
        if isinstance(other, self.__class__):
            return self.href == other.href and (len(self.components.intersection(other.components))>0 or len(self.units.intersection(other.units))>0)
        else:
            return False
    def __str__(self):
        return f"Import of {self.href}"

    def __hash__(self):
        """Hash an import."""
        return hash((self.href))
    
    def __contains__(self, item):
        """Check if an import contains a component or units."""
        return item in self.children
    
    def cellMLText(self):
        """Return the CellMLTextView representation of an import."""
        cellML = f"def import using \"{self.href}\" for \n"
        for item in self.children:
            cellML += item.cellMLText()
        cellML += "enddef; \n"
        return cellML

class Import_component(cellMLNodeBase, NodeMixin):
    """Class to store a CellML import component, as a child of an import element"""
    def __init__(self, name,component_ref, component_def, parent=None, children=None):
        """Initialise the CellML import component."""
        super(cellMLNodeBase, self).__init__()
        self.name = name
        self.component_ref = component_ref
        self.component_def = component_def # component_def is the component definition in the imported model
        self._parent = parent
        if children:
            self.children = children
    @property
    def parent(self):
        """Return the parent of an import_component."""
        return self._parent
    @parent.setter
    def parent(self, value):
        if value is None:
            self._parent = value
        elif isinstance(value, Import):
            self._parent = value
        else:
            raise TypeError("Parent must be of type CellMLImport.")

    def __eq__(self, other):
        """Check if two import_components are equal."""
        if isinstance(other, self.__class__):
            return self.name == other.name and self.component_ref == other.component_ref
        else:
            return False

    def __hash__(self):
        """Hash an import_component."""
        return hash((self.name, self.component_ref))

    def __str__(self):
        """String representation of an import_component."""
        return f"{self.name} <-> {self.component_ref}"

    def cellMLText(self):
        """Return the CellMLTextView representation of an import_component."""
        return f"comp {self.name} using comp {self.component_ref}; \n"
    
class Import_units(cellMLNodeBase, NodeMixin):
    """Class to store a CellML import unit, as a child of an import element"""
    def __init__(self, name,units_ref, parent=None, children=None):
        """Initialise the CellML import unit."""
        super(cellMLNodeBase, self).__init__()
        self.name = name
        self.units_ref = units_ref
        self._parent = parent
        if children:
            self.children = children
    
    @property
    def parent(self):
        """Get the parent of an import_unit."""
        return self._parent
    @parent.setter
    def parent(self, value):
        """Set the parent of an import_unit."""
        if value is None:
            self._parent = value
        elif isinstance(value, Import):
            self._parent = value
        else:
            raise TypeError("Parent must be of type CellMLImport.")

    def __eq__(self, other):
        """Check if two import_units are equal."""
        if isinstance(other, self.__class__):
            return self.name == other.name or self.units_ref == other.units_ref
        else:
            return False
    def __str__(self):
        """String representation of an import_unit."""
        return f"{self.name} <-> {self.units_ref}"

    def __hash__(self):
        """Hash an import_unit."""
        return hash((self.name, self.units_ref))

    def cellMLText(self):
        """Return the CellMLTextView representation of an import_units."""
        return f"unit {self.name} using unit {self.units_ref}; \n"


class Math (cellMLNodeBase, NodeMixin):
    """Class to store a CellML math in the format of MathML tree."""
    def __init__(self, equation_id, math,parent=None, children=None):
        """Initialise the CellML math element."""
        super(cellMLNodeBase, self).__init__()
        self.id = equation_id
        self.math = math # math is a MathML tree
        self._parent = parent
        if children:
            self.children = children
    @property
    def parent(self):
        """Get the parent of the math element."""
        return self._parent
    @parent.setter
    def parent(self, value):
        if value is None:
            self._parent = value
        elif not isinstance(value, Component):
            raise TypeError("Parent must be of type CellMLComponent.")
        else:
            self._parent = value
    # to do

class Units(cellMLNodeBase, NodeMixin):
    """Class to store a CellML units element, as a child of a model."""
    def __init__(self, name, parent=None, children=None):
        """Initialise the CellML units element."""
        super(cellMLNodeBase, self).__init__()
        self.name = name
        self._parent = parent
        self._children = children
    
    @property
    def parent(self):
        """Get the parent of the units element."""
        return self._parent
    @parent.setter
    def parent(self, value):
        if value is None:
            self._parent = value
        elif not isinstance(value, Model):
            raise TypeError("Parent must be of type CellMLModel.")
        else:
            self._parent = value
    @property
    def children(self):
        """Get the children of the units element."""
        return self._children
    @children.setter
    def children(self, value):
        if any(not isinstance(item, Unit) for item in value):
            raise TypeError("Children must be of type CellMLUnit.")
        else:
             # check replicated units
            unit_names = [item.units for item in value]
            if len(unit_names) != len(set(unit_names)):
                raise ValueError("Replicated units are not allowed.")
            else:
                self._children = value
                for item in self.children:
                    item.parent = self          

    @property
    def name(self):
        """Get the name of the units element."""
        return self._name
    @name.setter
    def name(self, value):
        # check if the name is in the Built-in units list
        if value in Model.BUILTIN_UNITS:
            raise ValueError(f"Unit {value} is a built-in unit.")
        else:
            self._name = value

    def __eq__(self, other):
        """Check if two units are equal."""
        if isinstance(other, self.__class__):
            return self.name == other.name 
        else:
            return False

    def __hash__(self):
        """Hash a units element."""
        return hash((self.name))

    def cellMLText(self):
        """Return the CellMLTextView representation of a units element."""
        cellML = f"def unit {self.name} as \n"
        for unit in self.children:
            cellML += unit.cellMLText() + " \n"
        cellML += "enddef; \n"
        return cellML   

class Unit(cellMLNodeBase, NodeMixin):
    """Class to store a CellML unit, as a child of a units element. """
    def __init__(self, units, prefix=None, exponent=None, multiplier=None, offset=None, parent=None, children=None):
        """Initialise the CellML unit."""
        super(cellMLNodeBase, self).__init__()
        self.units = units
        self.prefix = prefix
        self.exponent = exponent
        self.multiplier = multiplier
        self.offset = offset
        self._parent = parent
        if children:
            self.children = children 
    
    @property
    def parent(self):
        """Get the parent of the unit."""
        return self._parent
    @parent.setter
    def parent(self, value):
        if value is None:
            self._parent = value
        elif not isinstance(value, Units):
            raise TypeError("Parent must be of type CellMLUnits.")
        else:
            self._parent = value

    def __eq__(self, other):
        """Check if two units are equal."""
        if isinstance(other, self.__class__):
            return self.units == other.units and self.prefix == other.prefix and self.exponent == other.exponent and self.multiplier == other.multiplier and self.offset == other.offset
        else:
            return False

    def __hash__(self):
        """Hash a unit."""
        return hash((self.units, self.prefix, self.exponent, self.multiplier, self.offset))

    def __str__(self):
        """String representation of a unit."""
        return f"{self.prefix}{self.units}^{self.exponent}*{self.multiplier}+{self.offset}"

    def cellMLText(self):
        """Return the CellMLTextView representation of a unit."""
        # Define the optional attributes of a unit
        _optional_attributes = ['prefix', 'exponent', 'multiplier', 'offset']
        _attribute_lookup = {'prefix': 'pref', 'exponent': 'expo', 'multiplier': 'mult', 'offset': 'off'}
        # Check if the unit has any optional attributes
        if any([getattr(self, attribute) is not None for attribute in _optional_attributes]):
            # If the variable has any optional attributes, return the CellMLTextView representation of the variable with the optional attributes
            return f'unit {self.units} '+ '{' + ','.join([f"{_attribute_lookup[attribute]}: {getattr(self, attribute)}" for attribute in _optional_attributes if getattr(self, attribute) is not None]) +'};'
        else:
            # If the variable has no optional attributes, return the CellMLTextView representation of the variable without the optional attributes
            return f"unit {self.units};"    

class Variable(cellMLNodeBase, NodeMixin):
    """Class to store a CellML variable, as a child of a component."""
    def __init__(self, name, units, initial_value=None, public_interface=None, private_interface=None, parent=None, children=None):
        """Initialise the CellML variable."""
        super(cellMLNodeBase, self).__init__()
        self.name = name
        self.units = units
        self.initial_value = initial_value
        self.public_interface = public_interface
        self.private_interface = private_interface
        self.annotation = name
        self._parent = parent
        if children:
            self.children = children         
    
    @property
    def parent(self):
        """Return the parent of the variable."""
        return self._parent
    @parent.setter
    def parent(self, value):
        """Set the parent of the variable."""
        if value is None:
            self._parent = value
        elif isinstance(value, Component):
            self._parent = value
        else:
            raise TypeError(f"Parent {value} is not a Component.")

    @property
    def public_interface(self):
        """Return the public interface of the variable."""
        return self._public_interface
    @public_interface.setter
    def public_interface(self, public_interface):
        """Set the public interface of the variable."""
        if public_interface in ['in', 'out', 'none',None]:
            self._public_interface = public_interface
        else:
            raise ValueError(f"Public interface {public_interface} is not valid.")
    
    @property
    def private_interface(self):
        """Return the private interface of the variable."""
        return self._private_interface
    @private_interface.setter
    def private_interface(self, private_interface):
        """Set the private interface of the variable."""
        if private_interface in ['in', 'out', 'none',None]:
            self._private_interface = private_interface
        else:
            raise ValueError(f"Private interface {private_interface} is not valid.")
    
    def annotate(self,annotation):
        """Add an annotation to the CellML variable."""
        self.annotation = annotation
     
    def __eq__(self, other):
        """Check if two variables are equal."""
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        """Hash a variable."""
        return hash(self.name)

    def __str__(self):
        """String representation of a variable."""
        return f'{self.name}: {self.units};'

    def __dir__(self):
        """Return the attributes of a variable."""
        return ['name', 'units', 'initial_value', 'public_interface', 'private_interface', 'annotation']

    def cellMLText(self):
        """Return the CellMLTextView representation of the variable."""
        _optional_attributes = ['public_interface', 'private_interface', 'initial_value']
        _attribute_lookup = {'public_interface': 'pub', 'private_interface': 'priv', 'initial_value': 'init'}
        if any([getattr(self, attribute) is not None for attribute in _optional_attributes]):
            # If the variable has any optional attributes, return the CellMLTextView representation of the variable with the optional attributes
            return f'var {self.name}: {self.units} '+ '{' + ','.join([f"{_attribute_lookup[attribute]}: {getattr(self, attribute)}" for attribute in _optional_attributes if getattr(self, attribute) is not None]) +'};'
        else:
            # If the variable has no optional attributes, return the CellMLTextView representation of the variable without the optional attributes
            return f'var {self.name}: {self.units};'  

def addImport_Units(Model, href,units):
    """Add the units that need to be imported."""
    collection = []
    for unit in units:
        collection+=[Import_units(unit, unit)]
    return Import(href,parent=Model,children = collection)


