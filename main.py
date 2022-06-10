"""
    Author: Michael Fernandez
    Usage: Fix and re-export a Rig with rotated root rig node.
"""

from pymel.core import *

from maya import cmds

"""
    Steps:
        Duplicate RigRoot hierarchy = RigRoot1
        Copy keys from all joints from RigRoot to RigRoot1
        Delete Keys from all joints in RigRoot
        Parent RigPelvis to World -- MEL(parent -world RigPelvis ;)
        Rotate RigRoot 90* on X-axis
        Parent Constrain RigPelvis ( RigRoot1 ) to RigPelvis ( RigRoot )
        Freeze transforms of RigRoot
        Parent RigPelvis to RigRoot
        Parent Constrain RigRoot1 to RigRoot
"""


"""
    Functions
"""

def SelectHierarchy(root):
    """
        Select a hierarchy and the root object.
        root should be a object class.
    """

    select(root)

    for obj in listRelatives(root, ad=True):
        select(obj, add=True)

def CopyKeysToRig(rigCopyFrom, rigCopyTo):
    SelectHierarchy(rigCopyFrom)
    
    copyKey(option="curve") # Copies keys from all active objects.

    SelectHierarchy(rigCopyTo)

    pasteKey()

def ParentConstraintRigToRig(rig1, rig2):
    """
        Parent Constraint rig1 joints to rig2 joints
    """
    def CollectJoints(rig):
        """
            Returns a list of all joints in rig
        """
        select(rig)
        listOfJoints = []

        for joint in listRelatives(rig, allDescendents=True):
            if type(joint) == nt.Joint:
                listOfJoints.append(joint)
        
        return listOfJoints

    rig1Set = set(CollectJoints(rig1))
    rig2Set = set(CollectJoints(rig2))

    for j1 in rig1Set:
        for j2 in rig2Set:
            if str(j1).split("|")[-1] == str(j2).split("|")[-1]:
                print("Constraint %s to %s") %(str(j1), str(j2))
                parentConstraint(j1, j2)
            else:
                continue
                #print("Could not constraint %s to %s") %(str(j1), str(j2))


"""
    Test code
"""
# Duplicate RigRoot
rigRoot = PyNode( 'RigRoot' )
rigPelvis = rigRoot.outputs()[0] # Get direct child at index 0
duplicate(rigRoot)

# Get duplicated RigRoot and its Pelvis joint
rigRoot1 = PyNode( 'RigRoot1' )
rig1Pelvis = rigRoot1.outputs()[0]

# Copy keys from RigRoot to RigRoot1
SelectHierarchy(rigRoot1)
CopyKeysToRig(rigRoot, rigRoot1)

# Remove all keys from rigRoot
SelectHierarchy(rigRoot)
cutKey(cl=True) # Clears keys on selected objects

# Parent RigRoot Pelvis joint to World
parent(rigPelvis, world=True)

# Rotate rigRoot 90* on X-axis
select(clear=True)
select(rigRoot)
rotate('90deg', r=True)
# Freeze transforms of rigRoot
makeIdentity(a=True, r=True) # applies and freezes the rotation transforms

# Parent Constraint rig1Pelvis to rigPelvis
# select(rig1Pelvis)
# select(rigPelvis, add=True)
parentConstraint(rig1Pelvis,rigPelvis, maintainOffset=True)

# Parent rigPelvis to rigRoot
parent(rigPelvis, rigRoot)

# Parent Constraint rigRoot1 to rigRoot
ParentConstraintRigToRig(rigRoot1, rigRoot)

