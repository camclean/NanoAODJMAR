
#!/Usr-/bin/env python
import os,sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODJMAR.ZPlusJetsXS_2D import *


# NOTE : This file is configured to Process MC.
# If you want to process Data then ADD "jsonInput='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'"
# to the PostProcessor arguement below


p1=PostProcessor(".",inputFiles() ,"Jet_pt>200 ","keep_and_drop.txt",[ZPlusJetsXS_2D()],provenance=True,fwkJobReport=True,histFileName='80XNanoV0-DYtoLL-histos.root'  , histDirName='zjets'  , haddFileName =  '80XNanoV0-DYtoLL-nanoTrees.root', jsonInput='Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt')


p1.run()

print "DONE"
