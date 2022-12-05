import sys
sys.path.insert(1, '../src/')
from readMatrices import load_matrix
import os
import numpy as np
from bgClass import BG_comp, CellMLft, BG_module, BG_model, updateStoich, k2BGpara, writePara 
if __name__ == "__main__":
  
    modules=[]
    # Getting the name of the directory where this file is present.
    current = os.path.dirname(os.path.realpath(__file__))
    mPath = current+'/' 
    txtPath = mPath+'txt/'
    mSub = ['A','B','C']
    #unitLib = '../cellLib/BG/units_BG.cellml'
    unitLib = 'units_BG.cellml'
    for mName in mSub:
      comps=[]
      compd=[]      
      CompNamei,CompTypei,ReNamei,ReTypei,Nfi,Nri=load_matrix(f'{mPath}csv/{mName}_f.csv',f'{mPath}csv/{mName}_r.csv',mName)

      for i, name in enumerate(CompNamei):
         comps.append(BG_comp(name,CompTypei[i]))
      for i, name in enumerate(ReNamei):
         compd.append(BG_comp(name,ReTypei[i])) 

      sub = BG_module(mName,comps,compd,Nfi,Nri)
      modules.append(sub)
      sub.write2CellML_1(txtPath, unitLib)
      nspecies = len(Nfi)
      nreaction = len(Nfi[0])
      kf = [1]*nreaction
      kr = [1]*nreaction
      q_init=[1]*nspecies
      N_c = []
      K_c = 1
      Ws = np.ones((nspecies,1))
      extraPara={'T':[279.45,'kelvin']}
      Nf= Nfi.astype(float)
      Nr= Nri.astype(float)
      kappa, K, error=k2BGpara(Nf,Nr,kf,kr,K_c,N_c,Ws)
      sub.write2CellML_d(txtPath, unitLib,kappa,extraPara)      
      model= BG_model(f'{mName}_test',[sub])
      writePara (model,K, q_init, extraPara, txtPath,unitLib)
      model.write2CellML(txtPath,unitLib)

    model= BG_model('ABC',modules)
    model.write2CellML(txtPath,unitLib)
    Nf,Nr= updateStoich (model, [])
    nspecies = len(model.Kunique)
    nreaction = len(Nf[0])
    kf = [1]*nreaction
    kr = [1]*nreaction
    q_init=[1]*nspecies
    N_c = []
    K_c = 1
    Ws = np.ones((nspecies,1))
    kappa, K, error=k2BGpara(Nf,Nr,kf,kr,K_c,N_c,Ws)
    print(kappa, K, error)
    extraPara={'T':[279.45,'kelvin']}
    writePara (model,K, q_init, extraPara, txtPath,unitLib)