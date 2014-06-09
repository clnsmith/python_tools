# -*- coding: utf-8 -*-
###############################################################################
#SimTools.py
#Simulation Tools Module
#==============================================================================
#Written by Colin Smith colin.cs.smith@gmail.com
#5/6/2013
#------------------------------------------------------------------------------
#This module is a collection of tools used to import and use SIMM and OpenSim 
#files in python
###############################################################################
def importMot(fileName,colNames=None):
    """Import file.mot data as two numpy arrays: colNames, motData
    
    Inputs
    --------
    file = 'file.mot' string file name (optionally with path) 
    
    Optional:    
    colNames = True: return numpy array of column names  
    
    Outputs
    --------
    colNames = numpy array of column names (as strings)
    motData = numpy array of data
    """
    import numpy as np
    
    #Import numeric data    
    motData = np.loadtxt(fileName,skiprows=14)
    
    #Remove first column (full of empty data)    
    motData = motData[:,1:]
        
    if colNames==None:
        return motData
    
    else:
        #Import column names
        colNames = np.loadtxt(fileName,dtype=str, skiprows=13) 
        colNames = colNames[0,0:]
        
        return [colNames,motData]
        
def importKneeKinematics(fileName,colNames=None):
    """Import file.mot data as two numpy arrays: colNames, motData
    
    Inputs
    --------
    file = 'file.mot' string file name (optionally with path) 
    
    Optional:    
    colNames = True: return numpy array of column names  
    
    Outputs
    --------
    colNames = numpy array of column names (as strings)
    motData = numpy array of data (in .mot file order)
    """
    import numpy as np
    import pandas as pd
    #Import numeric data    
    
    
    data = pd.read_csv(fileName,skiprows=14,delimiter='\t',header=None, usecols=[29,30,31,32,33,34])
    motData = data.as_matrix()
        
    if colNames==None:
        return motData
    
    else:
        #Import column names
        colNames = np.loadtxt(fileName,dtype=str, skiprows=13,usecols =                                     (28,29,30,31,32,33)) 
        colNames = colNames[0,0:]
        
        return [colNames,motData]
        
def getKneeKinFromMotData(motData):
    """Extract knee kinematics (Tx Ty Tz Rx Ry Rz) from motData numpy array

    Inputs
    --------
    motData = numpy array genertated using importMot

    Outputs
    --------
    kneeKin = numpy array containing columns of knee kinematics 
              (Tx Ty Tz FE VV IE)
    """
    
    import numpy as np
    
    #Extract knee kinematic data
    kneeKin_unordered=motData[:,28:34]
    
    #Reorder knee kinematic data (orginally Tz Tx Ty FE VV IE)
    i = np.array([1,2,0,3,4,5])    
    kneeKin=kneeKin_unordered[:,i]

    return kneeKin      

def motToKneeKinArray(pathToSimDirs,motFileName,numSim):
    """Read knee kinematics from .mot results files from condor simulations 
    and convert to numpy array. By default, the array is also saved to current
    directory
    
    Parameters
    ----------
    pathToSimDir : str
        Path from current directory to data directory containing sim_dir.#
        example : '../../data/'
    
    motFileName : str
        String name of .mot file output from condor simulations (located in sim_dir.#).
        Do not include simulation number or .mot
        example : 'kfec_halfhz_fd_MRI_'
        
    numSim : int
        Number of simulations run on condor
    
    save : bool, optional
        Set whether to save numpy array (default = True)
        
    Returns
    -------
    kneeKinArray : numpy array
        3d Array of knee kinematic values in: time Tx Ty Tz FE VV IE order.
        [numSim,row,column]
    """
    
    import numpy as np
    import pandas as pd
    
    
    #Determine Array Size    
    path0 = pathToSimDirs+'sim_dir.0/'
    fName0 = motFileName+'0.mot'
    testData = pd.read_csv(path0+fName0,skiprows=14,delimiter='\t',
                           header=None,usecols=[1]).as_matrix()
    r,c = testData.shape
    
    #Import Knee Kinematic Data
    kneeKinArray = np.zeros([numSim,r,7]) #initialize 3d array
    colOrder = np.array([0,2,3,1,4,5,6]) #final column order
    
    for i in range(numSim):
        path = pathToSimDirs+'sim_dir.'+str(i)+'/'
        fName = motFileName+str(i)+'.mot'
        rawData = pd.read_csv(path+fName,skiprows=14,delimiter='\t',
                    header=None,usecols=[1,29,30,31,32,33,34]).as_matrix()
        kneeKinArray[i,:,:] = rawData[:,colOrder]
    
    #Save data array to .npy file
    arrayFile = pathToSimDirs+'kneeKinArray.npy'    
    np.save(arrayFile,kneeKinArray)
    
    
    return kneeKinArray   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    