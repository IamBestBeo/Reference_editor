import maya.cmds as cmds
import maya.mel as mel
import os

def REF_UI():
    window_name = "ReferenceMasterWindow"

    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)

    cmds.window(window_name, title="Reference Editor", widthHeight=(400, 300))

    main_layout = cmds.columnLayout(adjustableColumn=True)

    cmds.text(label="REFERENCE LIST", font="boldLabelFont", height=24, align='center')
    reference_list = cmds.textScrollList("referenceList", numberOfRows=8, allowMultiSelection=True, height=200)

    cmds.button(label="Refresh List", command=lambda x: refresh_reference_list(reference_list))
    cmds.separator(height=2, style='none')
    cmds.button(label="Add Reference", command=add_reference)
    cmds.separator(height=2, style='none')
    cmds.button(label="Remove Selected References", command=lambda x: remove_selected_references(reference_list))
    cmds.separator(height=2, style='none')
    cmds.button(label="Reload References", command=lambda x: reload_references(reference_list))

    cmds.showWindow(window_name)

    refresh_reference_list(reference_list)

def refresh_reference_list(reference_list):
    """
    Refresh the reference list
    """
    cmds.textScrollList(reference_list, edit=True, removeAll=True)
    
    references = cmds.ls(references=True)
    
    for ref in references:
        cmds.textScrollList(reference_list, edit=True, append=ref)

def add_reference(*args):
    """
    Add new references
    """
    file_paths = cmds.fileDialog2(fileFilter="Maya Files (*.ma *.mb)", dialogStyle=2, fileMode=4)
    if file_paths:
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            namespace = os.path.splitext(file_name)[0]
            cmds.file(file_path, reference=True, namespace=namespace, mergeNamespacesOnClash=False)
        refresh_reference_list("referenceList")

def reload_references(reference_list):
    """
    Reload all references in the list
    """
    selected_refs = cmds.textScrollList(reference_list, query=True, allItems=True)
    if selected_refs:
        for ref in selected_refs:
            ref_node = cmds.referenceQuery(ref, referenceNode=True)
            cmds.file(loadReference=ref_node)

def remove_selected_references(reference_list):
    """
    Remove the selected references
    """
    selected_refs = cmds.textScrollList(reference_list, query=True, selectItem=True)
    if selected_refs:
        confirm = cmds.confirmDialog(title='Remove Reference', message='Are you sure to remove the selected references?', button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        
        if confirm == 'Yes':
            for ref in selected_refs:
                ref_node = cmds.referenceQuery(ref, referenceNode=True)
                cmds.file(removeReference=True, referenceNode=ref_node)
            refresh_reference_list(reference_list)

# Call the function to create UI
REF_UI()
