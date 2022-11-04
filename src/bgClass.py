# Define the class objects for BG implementation using CellML
import sys
import numpy as np 
import math
from operator import attrgetter 
from sympy import Matrix, S, nsimplify 

class CellMLft:
   # Format the CellML Text
   # The following units can be used in CellML with no need to define or import
   defUnit=["ampere","becquerel","candela","celsius","coulomb","dimensionless","farad","gram","gray","henry",
    "hertz","joule","katal","kelvin","kilogram","liter","litre","lumen","lux","meter","metre","mole",
    "newton","ohm","pascal","radian","second","siemens","sievert","steradian","tesla","volt","watt","weber"]
   # The type of interface of variables 
   IO = {'internal':'', 'pub-in': 'pub: in', 'pub-out': 'pub: out', 'priv-in': 'priv: in', 'priv-out': 'priv: out', 
         'pub-in-priv-out': 'pub: in, priv: out', 'pub-out-priv-in': 'pub: out, priv: in', 'pub-out-priv-out': 'pub: out, priv: out'} 
   # Some formatted lines for model structure
   indent = ' ' * 4
   end_model = ['enddef;\n']
   end_comp = [indent +'enddef;\n\n']   
   line_sys0 = [indent*2+ 'var R: J_per_K_per_mol {pub: in, priv: out};\n'+ indent*2 +'var T: kelvin {pub: in, priv: out};\n']
   line_sys1 = line_sys0+[indent*2+ 'var t: second {init: 0};\n']

class BG_comp:
   # Define the domain variables, units, and components
   # physical domain and variables
   dom = {'Ch':{'e':['mu','J_per_mol'],'f':['v','fmol_per_sec'],'q':['q','fmol']}, 
         'E':{'e':['V','volt'],'f':['I','fA'],'q':['q','fC']}} 
   # component
   comp = {'Ce':{'dom':'Ch', 'description':'Chemical species', 'p':['K','per_fmol']},
           'Se':{'dom':'Ch','description':'Chemostat', 'p':['K','per_fmol']},
           'C':{'dom':'E', 'description':'Capacitor','p':['C','fF']},
           'Ve':{'dom':'E','description':'Voltage source', 'p':['C','fF']},
           'Re':{'dom':'Ch','description':'Chemical Reaction', 'p':['kappa','fmol_per_sec']},
           'Re_GHK':{'dom':'Ch','description':'GHK Reaction', 'p':['kappa','fmol_per_sec']},
           'R':{'dom':'E','description':'Resistor', 'p':['g','fS']} } 
   # Initialize the component according to the type
   def __init__(self, name, type):
      # attribute: type, name, dom, description, para, input, output, eq
      # para, input, output: 2d list [[var_name, unit, IO]], eq: 1d list ['','']
      if type in list(BG_comp.comp):
         self.type = type
      else:
         sys.exit(f'BG {type} is not defined!')
      self.name = name
      self.dom = BG_comp.comp[type]['dom']
      self.description = BG_comp.comp[type]['description'] 

      if type in ['Ce','Se','C','Ve']:
            self.para = [[BG_comp.comp[type]['p'][0] + '_' + name, BG_comp.comp[type]['p'][1], CellMLft.IO['pub-in']],
                         [BG_comp.dom[self.dom]['q'][0]+ '_' + name + '_init', BG_comp.dom[self.dom]['q'][1], CellMLft.IO['pub-in']]]
            self.input = [[BG_comp.dom[self.dom]['f'][0]+ '_' + name, BG_comp.dom[self.dom]['f'][1], CellMLft.IO['priv-in']]]
            self.output = [[BG_comp.dom[self.dom]['e'][0]+ '_' + name, BG_comp.dom[self.dom]['e'][1], CellMLft.IO['pub-out']],
                           [BG_comp.dom[self.dom]['q'][0]+ '_' + name, BG_comp.dom[self.dom]['q'][1], CellMLft.IO['pub-out']]] 
            if type in ['Ce','Se']:   
               self.eq = [f'{self.output[0][0]} = R*T*ln({self.para[0][0]}*{self.output[1][0]});\n'] # constitutive relation
            else:
               self.eq = [f'{self.output[0][0]} = {self.output[1][0]}/{self.para[0][0]};\n'] # constitutive relation
            if type in ['Ce','C']:
               self.eq = self.eq + [f'ode({self.output[0][0]},t) = {self.input[0][0]};\n']            
      elif type == 'Re':
         self.para = [[BG_comp.comp[type]['p'][0] + '_' + name, BG_comp.comp[type]['p'][1], CellMLft.IO['pub-in']]]
         self.input = [[BG_comp.dom[self.dom]['e'][0]+ '_' + name + '_in', BG_comp.dom[self.dom]['e'][1], CellMLft.IO['internal']],
                       [BG_comp.dom[self.dom]['e'][0]+ '_' + name + '_out', BG_comp.dom[self.dom]['e'][1], CellMLft.IO['internal']]]
         self.output = [[BG_comp.dom[self.dom]['f'][0]+ '_' + name, BG_comp.dom[self.dom]['f'][1], CellMLft.IO['internal']]] 
         self.eq = [f'{self.output[0][0]} = {self.para[0][0]}*(exp({self.input[0][0]}/(R*T))-exp({self.input[1][0]}/(R*T)));\n'] # constitutive relation
      elif type == 'Re_GHK':
         offset_eq2 = ' ' * 12
         offset_eq3 = ' ' * 16
         self.para = [[BG_comp.comp[type]['p'][0] + '_' + name, BG_comp.comp[type]['p'][1], CellMLft.IO['pub-in']]]
         self.input = [[BG_comp.dom[self.dom]['e'][0]+ '_' + name + '_in', BG_comp.dom[self.dom]['e'][1], CellMLft.IO['internal']],
                       [BG_comp.dom[self.dom]['e'][0]+ '_' + name + '_out', BG_comp.dom[self.dom]['e'][1], CellMLft.IO['internal']],
                       [BG_comp.dom[self.dom]['e'][0]+ '_' + name + '_mod', BG_comp.dom[self.dom]['e'][1], CellMLft.IO['internal']]] 
         self.output = [[BG_comp.dom[self.dom]['f'][0]+ '_' + name, BG_comp.dom[self.dom]['f'][1], CellMLft.IO['internal']]]
         self.eq = [f'{self.output[0][0]} =  sel\n'] 
         self.eq.append(offset_eq2 + f'case {self.input[2][0]} == 0 {{{self.input[2][1]}}}:\n')
         self.eq.append(offset_eq3 + f'{self.para[0][0]}*(exp({self.input[0][0]}/(R*T))-exp({self.input[1][0]}/(R*T)));\n')
         self.eq.append(offset_eq2 + f'otherwise:\n')
         self.eq.append(offset_eq3 + f'{self.para[0][0]}*{self.input[2][0]}/(R*T)/(exp({self.input[2][0]}/(R*T))-1{{dimensionless}})*(exp({self.input[0][0]}/(R*T))-exp({self.input[1][0]}/(R*T)));\n')
      else:
         self.para = [[BG_comp.comp[type]['p'][0] + '_' + name, BG_comp.comp[type]['p'][1], CellMLft.IO['pub-in']]]
         self.input = [[BG_comp.dom[self.dom]['e'][0]+ '_' + name , BG_comp.dom[self.dom]['e'][1], CellMLft.IO['internal']]]
         self.output = [[BG_comp.dom[self.dom]['f'][0]+ '_' + name, BG_comp.dom[self.dom]['f'][1], CellMLft.IO['internal']]]
         self.eq =  [f'{self.output[0][0]} = {self.para[0]}*{self.input[0][0]};\n'] # constitutive relation
      

class BG_module(object):
   # Build a module based on the stoichiometric matrices
   def __init__(self, name, comps, compd, Nf, Nr):
      # attribute: name, comps (energy storage components, 0 node), compd (energy dissipation components, 1 node), direc, para, input, output, eq, Nf, Nr
      self.name = name
      self.comps = comps
      self.compd = compd
      self.direc = ['']*len(comps) # define the direction of positive flow from the storage components    
      self.para = [] 
      self.input = [] 
      self.output = []
      self.eq = []   
      zSet = set() # {(z,unit)} todo: multiple zs in one cell
      mu_in={}
      mu_out={}
      mu_mod={}
      outsign = '+'
      insign = '-'
      for i,e in enumerate(comps):        
         vComp = []
         # domain conversion
         if e.type in ['C','Ve']:
            TF = '*F'
            TF2 = 'F*'
            zSet.add(('R','J_per_K_per_mol', CellMLft.IO['pub-in']))
            zSet.add(('T','kelvin', CellMLft.IO['pub-in']))
            zSet.add(('F','C_per_mol', CellMLft.IO['pub-in']))
         else:
            TF = ''
            TF2 =''
            zSet.add(('R','J_per_K_per_mol', CellMLft.IO['pub-in']))
            zSet.add(('T','kelvin', CellMLft.IO['pub-in']))
         self.input = self.input + [[e.output[0][0], e.output[0][1], CellMLft.IO['pub-in']]]
         self.output = self.output + [[e.input[0][0], e.input[0][1], CellMLft.IO['pub-out']]]
         for j in range(len(Nf[0,:])):
            cellf,cellr = Nf[i,j],Nr[i,j]
            if '/' in cellf:
               self.direc[i]=='in'
               zvar, zunit = cellf.split('/')[0], cellf.split('/')[1]
               if not zvar.replace('.', '', 1).isdigit(): # z*v                  
                  zSet.add((zvar,zunit, CellMLft.IO['pub-in']))
                  vComp.append(f'{outsign} {zvar}{TF}*{compd[j].output[0][0]}')
                  Nf[i,j] = zvar # removing the /unit part
                  if compd[j].name in mu_in:
                     mu_in[compd[j].name]=mu_in[compd[j].name]+(f'+ {zvar}{TF}* {e.output[0][0]}')
                  else:
                     mu_in[compd[j].name]=(f'+ {zvar}{TF}* {e.output[0][0]}')
                  if compd[j].name in mu_mod and compd[j].type == 'Re_GHK' and e.type in ['C','Ve']:
                     mu_mod[compd[j].name]=mu_mod[compd[j].name]+(f' {zvar}{TF}* {e.output[0][0]}')
                  elif compd[j].name not in mu_mod and compd[j].type == 'Re_GHK' and e.type in ['C','Ve']:
                     mu_mod[compd[j].name]=(f'+ {zvar}{TF}* {e.output[0][0]}')                  
               else: # e.g, 2/unit
                  vComp.append(f'{outsign} {zvar}{{{zunit}}}{TF}*{compd[j].output[0][0]}')
                  Nf[i,j] = zvar # removing the /unit part
                  if compd[j].name in mu_in:
                     mu_in[compd[j].name]=mu_in[compd[j].name]+(f'+ {zvar}{{{zunit}}}{TF}* {e.output[0][0]}')
                  else:
                     mu_in[compd[j].name]=(f'+ {zvar}{{{zunit}}}{TF}* {e.output[0][0]}') 
                  if compd[j].name in mu_mod and compd[j].type == 'Re_GHK' and e.type in ['C','Ve']:
                     mu_mod[compd[j].name]=mu_mod[compd[j].name]+(f'+ {zvar}{{{zunit}}}{TF}* {e.output[0][0]}')
                  elif compd[j].name not in mu_mod and compd[j].type == 'Re_GHK' and e.type in ['C','Ve']:
                     mu_mod[compd[j].name]=(f'+ {zvar}{{{zunit}}}{TF}* {e.output[0][0]}')                 
            
            elif cellf.replace('.', '', 1).isdigit() and float(cellf)==1: # 1
               self.direc[i]=='in'
               vComp.append(f'{outsign} {TF2}{compd[j].output[0][0]}')
               if compd[j].name in mu_in:
                  mu_in[compd[j].name]=mu_in[compd[j].name]+(f'+ {TF2}{e.output[0][0]}')
               else:
                  mu_in[compd[j].name]=(f'+ {TF2}{e.output[0][0]}') 
               if compd[j].name in mu_mod and compd[j].type == 'Re_GHK' and e.type in ['C','Ve']:
                  mu_mod[compd[j].name]=mu_mod[compd[j].name]+(f'+ {TF2}{e.output[0][0]}')
               elif compd[j].name not in mu_mod and compd[j].type == 'Re_GHK' and e.type in ['C','Ve']:
                  mu_mod[compd[j].name]=(f'+ {TF2}{e.output[0][0]}')   

            if '/' in cellr:
               if self.direc[i]=='':
                  self.direc[i]=='out'
               zvar, zunit = cellr.split('/')[0], cellr.split('/')[1]
               if not zvar.replace('.', '', 1).isdigit(): # z*v
                  zSet.add((zvar,zunit, CellMLft.IO['pub-in']))
                  vComp.append(f'{insign} {zvar}{TF}*{compd[j].output[0][0]}')
                  Nr[i,j] = zvar # removing the /unit part
                  if compd[j].name in mu_out:
                     mu_out[compd[j].name]=mu_out[compd[j].name]+(f'+ {zvar}{TF}* {e.output[0][0]}')
                  else:
                     mu_out[compd[j].name]=(f'+ {zvar}{TF}* {e.output[0][0]}')                 
               else:
                  vComp.append(f'{insign} {zvar}{{{zunit}}}{TF}*{compd[j].output[0][0]}')
                  Nr[i,j] = zvar # removing the /unit part
                  if compd[j].name in mu_out:
                     mu_out[compd[j].name]=mu_out[compd[j].name]+(f'+ {zvar}{{{zunit}}}{TF}* {e.output[0][0]}')
                  else:
                     mu_out[compd[j].name]=(f'+ {zvar}{{{zunit}}}{TF}* {e.output[0][0]}')           
            elif cellr.replace('.', '', 1).isdigit() and float(cellr)==1:
               if self.direc[i]=='':
                  self.direc[i]=='out'
               vComp.append(f'{insign} {TF2}{compd[j].output[0][0]}')
               if compd[j].name in mu_out:
                  mu_out[compd[j].name]=mu_out[compd[j].name]+(f'+ {TF2}{e.output[0][0]}')
               else:
                  mu_out[compd[j].name]=(f'+ {TF2}{e.output[0][0]}') 
         self.eq.append(f'{e.input[0][0]} = ' + ' '.join(vComp) + ';\n')
      self.Nf = Nf
      self.Nr = Nr
      for i,d in enumerate(compd):
         if len(d.input)==1:
            self.eq.append(f'{d.input[0][0]} = {mu_in[d.name]};\n')
         elif len(d.input)==2:
            self.eq.append(f'{d.input[0][0]} = {mu_in[d.name]};\n')
            self.eq.append(f'{d.input[1][0]} = {mu_out[d.name]};\n')
         elif len(d.input)==3:
            self.eq.append(f'{d.input[0][0]} = {mu_in[d.name]};\n')
            self.eq.append(f'{d.input[1][0]} = {mu_out[d.name]};\n')
            self.eq.append(f'{d.input[2][0]} = {mu_mod[d.name]};\n')
      
      for z in zSet:
           self.para.append(list(z)) 

   def write2CellML_1 (self,fpath,unitLib):
      mName = f'{self.name}_1'
      def_import = [CellMLft.indent + f'def import using "{unitLib}" for\n']
      def_model= [f'def model {mName} as\n']
      def_comp=[CellMLft.indent + f'def comp {mName} as\n']     
      vars = []
      eqs = []
      units = []
      unitset = set()
      list_all = self.para + self.input + self.output
      eq_all = []   
      for comp in self.compd:
         list_all = list_all + comp.para + comp.input +comp.output
         eq_all = eq_all + comp.eq
      eq_all = eq_all +self.eq
      for e in list_all:
         unitset.add(e[1])        
         if len(e[2])>0:
            vars.append(CellMLft.indent*2 + 'var '+ e[0] + ': '+ e[1] +' {' + e[2] + '};\n')
         else:
            vars.append(CellMLft.indent*2 + 'var '+ e[0] + ': '+ e[1]+';\n')    
      for unit in unitset:
         if unit not in CellMLft.defUnit:
            units.append(CellMLft.indent*2 + f'unit {unit} using unit {unit};\n')
      for e in eq_all:
         eqs.append(CellMLft.indent*2 + e)
      
      lines= def_model + def_import + units + CellMLft.end_comp + def_comp + vars + eqs + CellMLft.end_comp + CellMLft.end_model
      with open(f'{fpath}{mName}.txt', 'w') as cid:
         cid.writelines(lines)
      cid.close()

   def write2CellML_d (self,fpath,unitLib,kappa,extraPara):
      mName = f'{self.name}'
      def_import = [CellMLft.indent + f'def import using "{unitLib}" for\n']
      def_model= [f'def model {mName} as\n']
      def_comp=[CellMLft.indent + f'def comp {mName} as\n'] 
      def_group=[CellMLft.indent + f'def group as encapsulation for\n']+ [CellMLft.indent*2 + f'comp {mName} incl\n']
      def_model_para= [f'def model {mName}_para as\n']
      def_comp_para=[CellMLft.indent + f'def comp {mName}_para as\n']
      predef_para= [CellMLft.indent*2 + f'var R: J_per_K_per_mol {{init: 8.31, pub: out}};\n'] + [CellMLft.indent*2 + f'var F: C_per_mol {{init: 96485, pub: out}};\n']    
      vars_para = []
      values_para =[]
      units_para=[]
      impunits_para=[]
      paras_para = []
      unitset_para=set()
      for p in extraPara:
         unitset_para.add(extraPara[p][1])
         vars_para.append(p)
         values_para.append(extraPara[p][0])
         units_para.append(extraPara[p][1])
      vars = []
      units = []
      unitset = set()
      varMap = {}
      varmaps=[] 
      for p in self.para:
         if mName+'_para' in varMap:
            varMap[f'{mName}_para'].append([p[0], p[0]])
         else:
            varMap[f'{mName}_para']=[[p[0], p[0]]]
      for i, p in enumerate(self.compd[0].para):
         if mName+'_para' in varMap:
            varMap[f'{mName}_para'].append([p[0], p[0]])
         else:
            varMap[f'{mName}_para']=[[p[0], p[0]]]
         unitset_para.add(p[1])
         vars_para.append(p[0])
         values_para.append(kappa[i])
         units_para.append(p[1]) 
      for unit in unitset_para:
         if unit not in CellMLft.defUnit:
             impunits_para.append(CellMLft.indent*2 + f'unit {unit} using unit {unit};\n')
      for i,para in enumerate(vars_para):
         paras_para.append(CellMLft.indent*2 + f'var {para}: {units_para[i]} {{init:{values_para[i]}, pub: out}};\n')

      lines_para=def_model_para + def_import + impunits_para + CellMLft.end_comp +def_comp_para+ predef_para+ paras_para+ CellMLft.end_comp + CellMLft.end_model
      with open(f'{fpath}{mName}_para.txt', 'w') as cid:
         cid.writelines(lines_para)
      cid.close()
      for e in self.input+self.output:
         if self.name+'_1' in varMap:
            varMap[f'{self.name}_1'].append([e[0], e[0] ])
         else:
            varMap[f'{self.name}_1']=[[e[0], e[0] ]]
         unitset.add(e[1])        
         if len(e[2])>0:
            if e[2] == 'pub: in':
               vars.append(CellMLft.indent*2 + 'var '+ e[0] + ': '+ e[1] +' {' + CellMLft.IO['pub-in-priv-out'] + '};\n')
            else:
               vars.append(CellMLft.indent*2 + 'var '+ e[0] + ': '+ e[1] +' {' + CellMLft.IO['pub-out-priv-in'] + '};\n')
         else:
            vars.append(CellMLft.indent*2 + 'var '+ e[0] + ': '+ e[1]+';\n')    
      for unit in unitset:
         if unit not in CellMLft.defUnit:
            units.append(CellMLft.indent*2 + f'unit {unit} using unit {unit};\n')
      encap=[]
      impt=[]         
      for imp in [f'{self.name}_1'] + [f'{mName}_para']:
         encap = encap + [CellMLft.indent*3+f'comp {imp};\n']
         impt = impt + [CellMLft.indent + f'def import using "{imp}.cellml" for\n'] + [CellMLft.indent*2 + f'comp {imp} using comp {imp}\n'] + CellMLft.end_comp
      encap = encap + [CellMLft.indent*2+'endcomp;\n']+ CellMLft.end_comp

      imp = f'{self.name}_1'
      varmaps = varmaps + [CellMLft.indent + f'def map between {imp} and {mName} for\n']
      for var in varMap[imp]:
         varmaps = varmaps + [CellMLft.indent*2 + f'vars {var[0]} and {var[1]}\n']
      varmaps = varmaps + CellMLft.end_comp

      imp = f'{mName}_para'
      varmaps = varmaps + [CellMLft.indent + f'def map between {imp} and {self.name}_1 for\n']
      for var in varMap[imp]:
         varmaps = varmaps + [CellMLft.indent*2 + f'vars {var[0]} and {var[1]}\n']
      varmaps = varmaps + CellMLft.end_comp  

      lines= def_model + def_import + units + CellMLft.end_comp + impt+ def_comp + vars + CellMLft.end_comp +def_group+encap+ varmaps+ CellMLft.end_model
      with open(f'{fpath}{mName}.txt', 'w') as cid:
         cid.writelines(lines)
      cid.close()
      
class BG_model(object):
   def __init__(self, name, modules):
      # attribute: name, comps, imp, para, input, eq, imp, sys, varMap, eindx
      self.name = name
      self.comps = []
      self.input = []
      self.para = []
      self.reName = []
      self.imp = list(map(attrgetter('name'), modules)) # import module names
      self.sys = {c:{} for c in self.imp}
      self.varMap = {f'{name}_para':[['R','R'],['T','T']]}
      self.eq = []
      self.eindx=[] # remove the electric component when converting kinetic parameters to BG parameters
      paraset = set()
      emap = {} # direction of q to/from the module
      compName =[] # all storage component names
      compType =[] # all storage component types
      tempcomps=[] # all storage components
      for m in modules:
         self.sys[m.name]['N_f'] = m.Nf
         self.sys[m.name]['N_r'] = m.Nr
         self.sys[m.name]['Kname'] = list(map(attrgetter('name'), m.comps))
         self.sys[m.name]['Ktype'] = list(map(attrgetter('type'), m.comps))
         self.varMap[m.name]=[]
         for d in m.compd: # get parameters of dissipation components in each modules 
            for p in d.para:
              # self.para.append([p[0] + '_' + m.name , p[1], CellMLft.IO['pub-in-priv-out']]) # append the module name to the parameter name of the reaction
               self.reName .append([p[0] + '_' + m.name , p[1]])
              # self.varMap[m.name]=[[p[0], p[0]+ '_' + m.name ]]
              # self.varMap[f'{name}_para'].append([p[0]+ '_' + m.name, p[0]+ '_' + m.name ])               
         for e in m.comps:
            self.input.append([e.input[0][0]+'_' + m.name , e.input[0][1], CellMLft.IO['priv-in']]) # flow contribution from the modules
            self.varMap[m.name].append([e.input[0][0], e.input[0][0]+'_' + m.name])
            self.varMap[m.name].append([e.output[0][0], e.output[0][0]]) # potential to the modules
            tempcomps.append(e)
            compName.append(e.name)
            compType.append(e.type)
            if e.name in emap:
               emap[e.name].append([m.name,m.direc])
            else:
               emap[e.name]=[[m.name,m.direc]] 
         for p in m.para:
            paraset.add((p[0], p[1], CellMLft.IO['pub-in-priv-out']))
           # self.varMap[m.name].append([p[0], p[0]])
      for para in paraset:
         self.para.append(list(para)) 
          # self.varMap[f'{name}_para'].append([list(para)[0], list(para)[0]])            
      # Identify common components (including electrical components)
      arraycompName = np.array(compName)
      arraycompType = np.array(compType)
      compUnique=list(sorted(set(compName),key=compName.index))
      self.Kunique = [] # remove electrical components, i.e., only keep chemical components
      typeKeep =[]
      for comp in compUnique:         
         compIdx = np.array([i for i, x in enumerate(arraycompName) if x == comp])
         types = arraycompType[compIdx]         
         eq = BG_comp.dom[tempcomps[compIdx[0]].dom]['f'][0]+ '_' + comp + ' = '
         if len(compIdx)==1:
           modulename = emap[comp][0][0]
           moduledirec = emap[comp][0][1]
           indx = compIdx[0] 
           typeKeep.append(arraycompType[indx])                             
           if types in ['Ce','Se']:
              self.Kunique.append(comp)
           else:
              self.eindx = compUnique.index(comp)

           if moduledirec == 'in':
              eq= eq + '-' + BG_comp.dom[tempcomps[indx].dom]['f'][0]+ '_' + comp + '_' + modulename + ';\n'
           else:
              eq= eq + '+' + BG_comp.dom[tempcomps[indx].dom]['f'][0]+ '_' + comp + '_' + modulename + ';\n'
         else: # if duplicate          
            if len(set(types))>0: # if the component types are different, ask user to decide
              print(f'The type of {comp} is inconsistent:{types}')
              ctype = input(f"Please specify the type of {comp}:\n")
              typeKeep.append(ctype)
            else:
              typeKeep.append(compType[compIdx[0]]) # only keep the first one
            if ctype in ['Ce','Se']:
              self.Kunique.append(comp)
            else:
              self.eindx = compUnique.index(comp)           
            for i,indx in enumerate(compIdx): 
               modulename = emap[comp][i][0]
               moduledirec = emap[comp][i][1]             
               if moduledirec == 'in':
                 eq= eq +'-' + BG_comp.dom[tempcomps[indx].dom]['f'][0]+ '_' + comp + '_' + modulename
               else:
                 eq= eq +'+' + BG_comp.dom[tempcomps[indx].dom]['f'][0]+ '_' + comp + '_' + modulename            
            self.eq.append(eq+';\n')                     
      for i, e in enumerate(compUnique):
         compi= BG_comp(e, typeKeep[i])
         self.comps.append(compi)
         self.varMap[f'{name}_para'].append([compi.para[0][0], compi.para[0][0]])
         self.varMap[f'{name}_para'].append([compi.para[1][0], compi.para[1][0]])
      # relations between submodule to whole module
      for i,sub in enumerate(self.imp):     
         ids = [compUnique.index(kid) for kid in self.sys[sub]['Kname']]
         self.sys[sub]['I_vec'] = ids
      num_rows = max(self.sys[self.imp[-1]]['I_vec'])+1
      for sub in self.imp:          
         T = BG_model._calcT_(self.sys[sub]['I_vec'],num_rows)
         self.sys[sub]['T'] = T 

   def _calcT_(I_vec,num_rows):
    num_cols = len(I_vec)
    T = np.zeros([num_rows,num_cols])
    for i in range(num_cols):
        T[I_vec[i]][i] = 1   
    return T 
   
   def write2CellML (self,fpath,unitLib):
      def_import = [CellMLft.indent + f'def import using "{unitLib}" for\n']
      def_model= [f'def model {self.name} as\n']
      def_comp=[CellMLft.indent + f'def comp {self.name} as\n']
      def_group=[CellMLft.indent + f'def group as encapsulation for\n']+ [CellMLft.indent*2 + f'comp {self.name} incl\n']    
      vars = []
      eqs = []
      units = []
      impt = []
      varmap =[]
      encap=[]
      unitset = set()
      list_all = self.input
      eq_all = [] 
      for imp in self.imp + [self.name+'_para']:
         encap = encap + [CellMLft.indent*3+f'comp {imp};\n']
         impt = impt + [CellMLft.indent + f'def import using "{imp}.cellml" for\n'] + [CellMLft.indent*2 + f'comp {imp} using comp {imp}\n'] + CellMLft.end_comp
         varmap = varmap + [CellMLft.indent + f'def map between {imp} and {self.name} for\n']
         for var in self.varMap[imp]:
            varmap = varmap + [CellMLft.indent*2 + f'vars {var[0]} and {var[1]}\n']
         varmap = varmap + CellMLft.end_comp  
      encap = encap + [CellMLft.indent*2+'endcomp;\n']+ CellMLft.end_comp
      for comp in self.comps:
         list_all = list_all + comp.para + comp.input +comp.output
         eq_all = eq_all + comp.eq
      eq_all = eq_all + self.eq
      for e in list_all:
         unitset.add(e[1])        
         if len(e[2])>0: # with interface
            vars.append(CellMLft.indent*2 + 'var '+ e[0] + ': '+ e[1] +' {' + e[2] + '};\n')
         else:
            vars.append(CellMLft.indent*2 + 'var '+ e[0] + ': '+ e[1]+';\n')
      for unit in unitset:
         if unit not in CellMLft.defUnit:
            units.append(CellMLft.indent*2 + f'unit {unit} using unit {unit};\n')
      for e in eq_all:
         eqs.append(CellMLft.indent*2 + e)
      lines=def_model + def_import + units + CellMLft.end_comp + impt + CellMLft.end_comp+def_comp+ CellMLft.line_sys1+vars + eqs + CellMLft.end_comp + def_group+ encap+ varmap+ CellMLft.end_model

      with open(f'{fpath}{self.name}.txt', 'w') as cid:
         cid.writelines(lines)
      cid.close()  

def updateStoich (model, newz):
      Nf = []
      Nr = []
      for sub in model.sys:
         for z in newz: # update z with value
            model.sys[sub]['N_f'][model.sys[sub]['N_f']==z] == z.value
            model.sys[sub]['N_r'][model.sys[sub]['N_r']==z] == z.value
         N_f=model.sys[sub]['N_f'].astype(float)
         N_r=model.sys[sub]['N_r'].astype(float)
         new_f = np.matmul(model.sys[sub]['T'],N_f)
         new_r = np.matmul(model.sys[sub]['T'],N_r)
         if not len(Nf):
            Nf = new_f
            Nr = new_r
         else:
            Nf = np.append(Nf, new_f,1)
            Nr = np.append(Nr, new_r,1)
      N_f = np.delete(Nf, model.eindx, axis=0) 
      N_r = np.delete(Nr, model.eindx, axis=0)     
      return N_f, N_r            
# Convert kinetic parameter to BG parameter        
def k2BGpara(N_f,N_r,kf,kr,K_c,N_c,Ws):
   # N_f/N_r: forward and reverse stoichiometric matrices
   # kf/kr: column vectors of the forward and reverse kinetic rate constants; 
   # K_c: column vector of known constraints between the species defined in N_c; 
   # Ws: column vector of the volume of species
   # Construct M, W, and vector of kinetic paras
   N_fT = np.transpose(N_f)
   N_rT = np.transpose(N_r) 
   N = N_r - N_f
   num_cols = len(N[0])
   I = np.identity(num_cols)
   if len(N_c)>0:
      N_cT=np.transpose(N_c)
      zerofill = np.zeros(num_cols)
      tempM = np.append(np.append(I, N_fT,1), np.append(I, N_rT,1),0)
      M = np.append(tempM, np.append(zerofill, N_cT,1),0)
      k_kinetic = kf + kr + K_c
   else:
      M = np.append(np.append(I, N_fT,1), np.append(I, N_rT,1),0)
      k_kinetic = kf + kr
   W = list(np.append([1]*num_cols, Ws))
   # Convert kinetic paras to BG paras
   lambda_expo = np.matmul(np.linalg.pinv(M), [math.log(k) for k in k_kinetic])
   lambdaW = [math.exp(l) for l in lambda_expo]
   lambdak = [lambdaW[i]/W[i] for i in range(len(W))]
   kappa = lambdak[:num_cols]
   K = lambdak[num_cols:]
   # Checks
   R = nsimplify(Matrix(N), rational=True).nullspace() #rational_nullspace(N, max_denom=len(N[0]))
   if R:
       R = np.transpose(np.array(R).astype(np.float64))[0]
   # Check that there is a detailed balance constraint
   Z = nsimplify(Matrix(M), rational=True).nullspace() #rational_nullspace(M, 2)
   if Z:
       Z = np.transpose(np.array(Z).astype(np.float64))[0] 
   k_est = np.matmul(M,[math.log(k) for k in lambdaW])
   k_est = [math.exp(k) for k in k_est]
   diff = [(k_kinetic[i] - k_est[i])/k_kinetic[i] for i in range(len(k_kinetic))]
   error = np.sum([abs(d) for d in diff])
   K_eq = [kf[i]/kr[i] for i in range(len(kr))]      
   try:
       zero_est = np.matmul(np.transpose(R),K_eq)
       zero_est_log = np.matmul(np.transpose(R),[math.log(k) for k in K_eq])
   except:
       print('undefined R nullspace')
   return kappa, K, error

def writePara (model, K, q_init, extraPara, fpath,unitLib):
   # extraPara {'varname':[value,'unit']}
   def_import = [CellMLft.indent + f'def import using "{unitLib}" for\n']
   def_model= [f'def model {model.name}_para as\n']
   def_comp=[CellMLft.indent + f'def comp {model.name}_para as\n']
   predef= [CellMLft.indent*2 + f'var R: J_per_K_per_mol {{init: 8.31, pub: out}};\n'] + [CellMLft.indent*2 + f'var F: C_per_mol {{init: 96485, pub: out}};\n']
   unitset=set()
   vars = []
   values =[]
   units=[]
   impunits=[]
   paras = []
   for p in extraPara:
      unitset.add(extraPara[p][1])
      vars.append(p)
      values.append(extraPara[p][0])
      units.append(extraPara[p][1])
   for i,comp in enumerate(model.Kunique):
      vars.append('K_'+comp)
      values.append(K[i])
      units.append('per_fmol')
   for i,comp in enumerate(model.Kunique):
      vars.append('q_init_'+comp)
      values.append(q_init[i])
      units.append('fmol')

   unitset.add('fmol')
   unitset.add('per_fmol')
   for unit in unitset:
      if unit not in CellMLft.defUnit:
         impunits.append(CellMLft.indent*2 + f'unit {unit} using unit {unit};\n')
   for i,para in enumerate(vars):
      paras.append(CellMLft.indent*2 + f'var {para}: {units[i]} {{init:{values[i]}, pub: out}};\n')

   lines=def_model + def_import + impunits + CellMLft.end_comp +def_comp+ predef+ paras+ CellMLft.end_comp + CellMLft.end_model

   with open(f'{fpath}{model.name}_para.txt', 'w') as cid:
      cid.writelines(lines)
   cid.close() 

        

   







