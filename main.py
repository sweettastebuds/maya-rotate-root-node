"""
    Author: Michael Fernandez
    Usage: Fix and re-export a Rig with rotated root rig node.
"""

from pymel.core import *
import maya.mel as mel

"""
    Global Variables
"""

isAnimation = False # False, will fix the Rig only.
importAFile = True


"""
    Functions
"""

def importFBX(filepath):
    newFile(force=True) # force new empty file
    openFile(filepath, type="fbx", force=True) # force open FBX file.

def exportFBX(filepath, useMel=False):
    
    if not useMel:
        exportSelectedAnim(filepath, type="FBX", force=True)
    
    else:

        command = "file -force -options \"v=0;\" -typ \"FBX export\" -pr -es \"%s\" " %(filepath)
        mel.eval(command)
        print "DONE"

def SelectHierarchy(root):
    """
        Select a hierarchy and the root object.
        root should be a object class.
    """

    select(root)

    for obj in listRelatives(root, ad=True):
        select(obj, add=True)

def CopyKeysToRig(rigCopyFrom, rigCopyTo):
    """
        Copy all keys rigCopyFrom to rigCopyTo.
    """
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
        j1Name = str(j1).split("|")[-1]
        j1Root = str(j1).split("|")[0]

        for j2 in rig2Set:
            j2Name = str(j2).split("|")[-1]
            j2Root = str(j2).split("|")[0]

            if j1Name == j2Name:
                print("Constraint [%s]%s ---> [%s]%s") %(j1Root, j1Name, j2Root, j2Name)
                parentConstraint(j1, j2)

            else:
                continue

def main():
    # Duplicate RigRoot
    rigRoot = PyNode( 'RigRoot' )
    rigPelvis = rigRoot.outputs()[0] # Get direct child at index 0
    duplicate(rigRoot)

    if isAnimation:
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

    if isAnimation:
        # Parent Constraint rig1Pelvis to rigPelvis
        # select(rig1Pelvis)
        # select(rigPelvis, add=True)
        parentConstraint(rigRoot1,rigRoot, maintainOffset=True)

        # Parent rigPelvis to rigRoot
        parent(rigPelvis, rigRoot)

        # Parent Constraint rigRoot1 to rigRoot
        ParentConstraintRigToRig(rigRoot1, rigRoot)
        
    
    else:
        # Parent rigPelvis to rigRoot
        parent(rigPelvis, rigRoot)

if __name__ == "__main__":
    def parse_inputs(pathToFiles, filterType=".fbx"):
        filepath_list = []
        count=0

        for filepath in pathToFiles:
            if os.path.isfile(filepath):
                print(filepath)

            else:
                for file in os.listdir(filepath):
                    file_path = os.path.join(filepath, file)
                    output_path = outputPath + file
                    
                    if file.lower().endswith(filterType):
                        count+=1
                        print("Import path: %s" %file_path)
                        print("output path: %s" %output_path)
                        importFBX(file_path)
                        main()
                        exportFBX(output_path, useMel=True)


    pathToFiles = ['D:\Workspace\Cosmos-Main\CosmosUnity\Assets\Art\Characters\Animals\GermanShepherd\Animations']
    outputPath = 'D:/Workspace/Cosmos-Main/CosmosUnity/Assets/Art/TechArt/temp/'
    parse_inputs(pathToFiles)

