from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.transferLogs    = False
config.General.transferOutputs = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'

config.section_("Data")
config.Data.publication  = False
#################################################################
# ALLOWS NON VALID DATASETS
config.Data.allowNonValidInputDataset = True

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'

config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'

## Something that can be changed frequently
primary_dataset = 'Muon0'
processed_dataset = 'Run2023C-PromptReco-v4'
config.Data.inputDataset = f"/{primary_dataset}/{processed_dataset}/AOD"
config.Data.unitsPerJob = 10
#config.Data.lumiMask = '../../data/LumiJSON/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON_MuonPhys.txt'
config.JobType.psetName = 'analyzeRPCwithTnP_Z_cfg.py'

from datetime import datetime
today = datetime.now().strftime(f'%y%m%d_00')
config.Data.outLFNDirBase = f'/store/user/seyang/RPC/Efficiency-TnP/{primary_dataset}/{processed_dataset}/{today}'
config.General.requestName = f'RPC_Efficiency-TnP_{primary_dataset}_{processed_dataset}'
