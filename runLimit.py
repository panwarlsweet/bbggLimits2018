#!/usr/bin/env python

from ROOT import *
import os,sys,json,time,re
import logging
from shutil import copy
from pprint import pformat
from multiprocessing import current_process
from utils import *
from os import listdir
import getpass

__username__ = getpass.getuser()
__author__ = 'Andrey Pozdnyakov'

__BAD__ = 666

gROOT.SetBatch()

import argparse

parser =  argparse.ArgumentParser(description='Limit Tree maker')
parser.add_argument('-f', '--configFile', dest="configName", type=str, default=None, required=True,
                    help="Json config file")
parser.add_argument('-o', '--outDir', dest="outDir", type=str, default="LIMS_OutDir",
                    help="Output directory (will be created).")
parser.add_argument('--node', dest="node", default=None, type=str,
                    choices=['2','3','4','5','6','7','8','9','10','11','12','13','SM','box'],
                    help = "Choose the nodes to run")
parser.add_argument('--mass', dest="mass", default=None, type=str,
                    choices=['250','260','270','280','300','320','340','350','400','450','500','550','600','650','700', '750', '800', '900'],
                    help = "Choose the resonant mass to run")
parser.add_argument('--overwrite', dest="overwrite", action="store_true", default=False,
                    help="Overwrite the results into the same directory")
parser.add_argument("-v", dest="verb", type=int, default=0,
                    help="Verbosity level: 0 - Minimal or no messages; 1 - INFO; 2 - DEBUG; 3 - Go crazy")
parser.add_argument('--extraLabel', dest='extraLabel', default='',
                    help='Extra label')
parser.add_argument('--ttHTaggerCut', dest='ttHTaggerCut', type=float, default=None)
parser.add_argument('--analyticalRW', dest='analyticalRW', action='store_true', default=False)
parser.add_argument('--kl', dest='ARW_kl', type=float, default=1.0)
parser.add_argument('--kt', dest='ARW_kt', type=float, default=1.0)
parser.add_argument('--cg', dest='ARW_cg', type=float, default=0.0)
parser.add_argument('--c2', dest='ARW_c2', type=float, default=0.0)
parser.add_argument('--c2g', dest='ARW_c2g', type=float, default=0.0)

opt = parser.parse_args()
print opt
# opt.func()
#  parser.print_help()

if opt.verb==0:
  logLvl = logging.ERROR
elif opt.verb==1:
  logLvl = logging.INFO
else:
  logLvl = logging.DEBUG

if opt.verb < 3:
  gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
  RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)
  RooMsgService.instance().setSilentMode(True)


begin = time.time()


def printTime(t1, t2, log):
  tNew = time.time()
  log.debug('Time since start of worker: %.2f sec; since previous point: %.2f sec' %(tNew-t2,tNew-t1))
  return tNew


def runFullChain(opt, Params, point=None, NRgridPoint=-1, extraLabel=''):
  #print 'Running: ', sys._getframe().f_code.co_name, " Node=",point
  # print sys._getframe().f_code
  gInterpreter.ProcessLine('#include "interface/bbgg2DFitter.h"')
  gSystem.Load('libHiggsAnalysisbbggLimits2018')

  PID = os.getpid()

  if opt.verb==0:
    logLvl = logging.ERROR
  elif opt.verb==1:
    logLvl = logging.INFO
  else:
    logLvl = logging.DEBUG

  LTDir  = os.getenv("CMSSW_BASE")+'/src/HiggsAnalysis/bbggLimits2018/'+Params['LTDIR']
  if '/tmp' in Params['LTDIR'] or '/store' in Params['LTDIR'] or '/afs' in Params['LTDIR']:
    LTDir = Params['LTDIR']
    if '/store' in Params['LTDIR']:
      LTDir = '/eos/cms'+Params['LTDIR']

  lumi = 42. # Only used for plot produced by bbgg2Dfitter
  energy = str(Params["energy"])
  NCAT    = Params["ncat"]
  mass   = Params["higgsMass"]
  addHiggs   = Params["addHiggs"]
  scaleSingleHiggs = Params["scaleSingleHiggs"]
  doBlinding = Params["doBlinding"]
  doBands = Params["doBands"]
  doSingleLimit = Params['doSingleLimit']
  doCombine       = Params["runCombine"]
  useSigTheoryUnc = Params["useSigTheoryUnc"]
  HH   = Params["HH"]
  base = Params["base"]
  low  = Params["low"]
  obs  = Params["obs"]
  dataName = Params['data']['name']
  combineOpt = Params['combineOption']
  doDoubleSidedCB = Params['doDoubleSidedCB']
  fitStrategy = Params['fitStrategy']

  massCuts = [Params["minMggMassFit"], Params["maxMggMassFit"],
              Params["minMjjMassFit"], Params["maxMjjMassFit"],
              Params["minSigFitMgg"],  Params["maxSigFitMgg"],
              Params["minSigFitMjj"],  Params["maxSigFitMjj"],
              Params["minHigMggFit"],  Params["maxHigMggFit"],
              Params["minHigMjjFit"],  Params["maxHigMjjFit"]]


  if point!=None and NRgridPoint!=-1:
    print 'WARning: cannot have both the Node and grid Point. Chose one and try again'
    return __BAD__
  elif opt.analyticalRW==True:
    Label = "_ARW_"
  elif point!=None:
    Label = "Node_"+str(point)
  elif NRgridPoint!=-1:
    Label = "_gridPoint_"+str(NRgridPoint)
  else:
    print 'WARning: using list of nodes from the json input file'
    return __BAD__

  sigCat = 0
  isRes = 0
  if point==None:
    sigCat = -1
  elif point == 'SM':
    sigCat = 0
  elif point == 'box':
    sigCat = 1
  elif int(point) > 15:
    sigCat = int(point)
    isRes = 1
    Label.replace("Node", "Mass")
  else:
    sigCat = int(point)

  Label +=  extraLabel

  print "Label=",Label



  # Create PID file to track the job:
  pidfile = "/tmp/"+__username__+"/PIDs/PoolWorker_"+Label+".pid"
  file(pidfile, 'w').write(str(PID))

  procName = current_process().name


  mainLog.info('\n\n New process Log started. PID = %d,  job label: %r\n', PID, Label)
  mainLog.info("This log filename = "+logging.getLoggerClass().root.handlers[0].baseFilename)
  mainLog.info('Node or Mass=%r  gridPoint=%r  PID=%r \n Options: %s',point, NRgridPoint, PID, pformat(opt))

  start = time.time()


  # For now the mass cuts are all the same, but can be changed in future.
  # ParamsForFits = {'SM': massCuts, 'box': massCuts}

  SignalFile = "/LT_output_GluGluToHHTo2B2G_node_"+str(point)+"_13TeV-madgraph.root"
  if "LT_StrikeBack" in LTDir or "MadMax" in LTDir or "ttH" in LTDir:
      SignalFile = "/LT_output_GluGluToHHTo2B2G_node_"+str(point)+"_13TeV-madgraph.root"
  if isRes:
    SignalFile = "/LT_output_GluGluToTYPEToHHTo2B2G_M-"+str(point)+"_narrow_13TeV-madgraph.root"
    if "RES_Mar21" in LTDir:
      SignalFile = "/LT_output_GluGluToTYPEToHHTo2B2G_M-"+str(point)+"_narrow_13TeV-madgraph_0.root"

  if NRgridPoint >= 0:
    SignalFile = "/LT_NR_Nodes_2to13_merged.root"

  if opt.analyticalRW == True:
    pointStr = "_".join(['kl',str(opt.ARW_kl),'kt',str(opt.ARW_kt),'cg',str(opt.ARW_cg),'c2',str(opt.ARW_c2),'c2g',str(opt.ARW_c2g)]).replace('.', 'p').replace('-', 'm')
    SignalFile="/LT_NR_Nodes_All_merged_"+pointStr+".root"

  mainLog.debug('%s', SignalFile)

  newFolder = baseFolder+ str('/'+Label)

  createDir(newFolder,mainLog)

  allCatFitsTemplate = os.getcwd()+'/'+Params['RooFitTemplateName']+'.rs'
  os.system(' '.join(['cat', os.getcwd()+'/'+Params['RooFitTemplateName']+'_vars.rs', os.getcwd()+'/'+Params['RooFitTemplateName']+'_cat*.rs','>', allCatFitsTemplate]))

  if opt.verb>1:
    print "File with PDF templates:\n", allCatFitsTemplate

  HLFactoryname= str(Label)
  hlf = RooStats.HLFactory(HLFactoryname, allCatFitsTemplate, False)
  w = hlf.GetWs()

  theFitter = bbgg2DFitter()

  theFitter.Initialize( w, sigCat, lumi, newFolder, energy, doBlinding, NCAT, addHiggs,
                        massCuts[0],massCuts[1],massCuts[2],
                        massCuts[3],massCuts[4],massCuts[5],
                        massCuts[6],massCuts[7],massCuts[8],
                        massCuts[9],massCuts[10],massCuts[11], NRgridPoint,
                        logging.getLoggerClass().root.handlers[0].baseFilename+'.bbgg2D', opt.analyticalRW)

  theFitter.SetVerbosityLevel(opt.verb)

  if opt.verb>1:
    theFitter.PrintWorkspace();

  if opt.ttHTaggerCut!=None:
    theFitter.SetCut("ttHTagger > "+str(opt.ttHTaggerCut))
    if opt.verb>0:
      mainLog.info('Apply the cut on ttHTagger: ' + str(opt.ttHTaggerCut))

  # Fit strategies. 1: 1D - m(gg); 2: 2D - m(gg),m(jj)
  if fitStrategy not in [1,2]:
    print "Fit strategy is not supported:", fitStrategy
    return __BAD__
  else:
    mainLog.info('Setting fit strategy to: %r', fitStrategy)
    theFitter.SetFitStrategy(fitStrategy)
#  if fitStrategy==1:
#    theFitter.SetCut("mjj > 100 && mjj < 150")

  if opt.verb>0:
    mainLog.info('Using Double Sided Crystal Ball as Signal Model: %r', doDoubleSidedCB)
  if doDoubleSidedCB: theFitter.UseDoubleSidedCB()

  mass = 125.0
  if opt.verb>0:
    mainLog.info('Signal File:\n'+LTDir+SignalFile)

  if not os.path.isfile(LTDir+SignalFile):
    print 'File does not exist: ', LTDir+SignalFile
    return __BAD__

  openStatus = theFitter.AddSigData( mass, str(LTDir+SignalFile))
  if openStatus==-1:
    mainLog.error('There is a problem with openStatus')
    return __BAD__
  mainLog.info("\t SIGNAL ADDED. Node=%r, GridPoint=%r", point,NRgridPoint)
  if opt.verb>0: p1 = printTime(start, start, mainLog)

  if opt.verb>1:
    theFitter.PrintWorkspace();

  theFitter.SigModelFit(mass)
  mainLog.info("\t SIGNAL FITTED. Node=%r, GridPoint=%r", point,NRgridPoint)
  if opt.verb>0: p2 = printTime(p1,start, mainLog)

  fileBaseName = "ws_hhbbgg.HH.sig.mH"+str(mass)[0:3]+"_13TeV"
  theFitter.MakeSigWS(fileBaseName)
  mainLog.info("\t SIGNAL'S WORKSPACE DONE. Node=%r, GridPoint=%r", point,NRgridPoint)
  if opt.verb>0: p3 = printTime(p2,start,mainLog)

  if addHiggs:
    higTypes = Params['higgs']['type']
    if opt.verb>1:
      mainLog.debug('Here will add SM Higgs contributions \n Higgs types: '+ pformat(higTypes))
    higgsExp = {}
    for iht,HT in enumerate(higTypes):
      ht = higTypes[HT]
      if opt.verb>1:
        mainLog.debug('iht = %r, ht = %r, HT = %r' % (iht,ht,HT))
      higFileName = str(LTDir)+"/LT_output_"+str(ht)+".root"

      exphig = theFitter.AddHigData( mass,higFileName,iht, str(HT))
      theFitter.HigModelFit(mass,iht, str(HT) )
      theFitter.MakeHigWS(str('ws_hhbbgg.')+str(HT), iht, str(HT))

      higgsExp[HT] = []
      for c in range(NCAT):
        higgsExp[HT].append(exphig[c])
        if opt.verb>1:
          mainLog.debug('Hig events for %r, cat %r: %r' % (HT,c,exphig[c]))

    if opt.verb>1:
      mainLog.debug("Done SM Higgs")

  ddata = str(LTDir + '/LT_'+dataName+'.root')
  ddata = ddata.replace("%MASS%", str(point))


  theFitter.AddBkgData(ddata)
  mainLog.info("\t BKG ADDED. Node=%r, GridPoint=%r, data file=%s", point,NRgridPoint,ddata)
  if opt.verb>0: p4 = printTime(p3,start, mainLog)

  if opt.verb>1:
    theFitter.PrintWorkspace();

  fitresults = theFitter.BkgModelFit()
  wsMultipdfFileBkgName = "ws_hhbbgg.data_bkg_multipdf"
  theFitter.BkgMultiModelFit(wsMultipdfFileBkgName)
  mainLog.info("\t BKG FITTED. Node=%r, GridPoint=%r", point,NRgridPoint)
  if opt.verb>0: p5 = printTime(p4,start,mainLog)
  if fitresults==None:
    mainLog.error("PROBLEM with fitresults !!")
    return __BAD__

  if opt.verb>1:
    mainLog.debug("\n Fit Results: \n\n"+pformat(fitresults.Print()))

  wsFileBkgName = "ws_hhbbgg.data_bkg"
  theFitter.MakeBkgWS( wsFileBkgName);
  mainLog.info("\t BKG'S WORKSPACE DONE. Node=%r, GridPoint=%r", point,NRgridPoint)
  if opt.verb>0: p6 = printTime(p5,start,mainLog)

  # print PID, "IM HERE"

  sigExp = []
  bkgObs = []
  for cc in xrange(NCAT):
    sigExp.append(-1)
    bkgObs.append(-1)

  sigExpStr = ''
  bkgObsStr = ''
  for cc in xrange(NCAT):
    sigExp[cc] = theFitter.GetSigExpectedCats(cc);
    if not doBlinding:
      bkgObs[cc] = theFitter.GetObservedCats(cc);

    if opt.verb>1:
      mainLog.debug('SIG events in cat %r: %r,  OBS (BKG): %r' % (sigExp[cc], cc, bkgObs[cc]))

  # Make datacards:
  myLoc = os.getenv("CMSSW_BASE") + '/src/HiggsAnalysis/bbggLimits2018/'+newFolder
  if isRes==1:
    DataCardMaker(str(myLoc), NCAT, sigExp, bkgObs, isRes)
  elif addHiggs == 0:
    DataCardMaker(str(myLoc), NCAT, sigExp, bkgObs, isRes)
  else:
    DataCardMaker_wHiggs(str(myLoc), NCAT, sigExp, bkgObs, higgsExp, mainLog)
    DataCardMaker_bias(str(myLoc), NCAT, sigExp, bkgObs, mainLog)

  mainLog.info("\t DATACARD DONE. Node/Mass=%r, GridPoint=%r", point,NRgridPoint)
  if opt.verb>0: p7 = printTime(p6,start,mainLog)

  if doSingleLimit or isRes:
    if doCombine:
      runCombine(newFolder+"/", doBlinding, mainLog, combineOpt,  Label)


  #Nonresonant data card massaging...
  if not isRes:

    if doCombine:
      for method in [1,2,3]:
        # If options 1,2,3 are provided - run the corresponding limits:
        # 1 - asymptotic, 2 - asymptotoc with adaptive azimov option; 3 - hybridnew
        # If combineOpt==4: run all of them at once
        if combineOpt!=4 and method!=combineOpt: continue
        try:
          combStatus = runCombine(newFolder, doBlinding, mainLog, method,  Label, scaleSingleHiggs)
        except:
          return __BAD__
        mainLog.info("\t COMBINE with Option=%r is DONE. Node=%r, GridPoint=%r \n \t Status = %r",
                     method, point,NRgridPoint, combStatus)
        if combStatus!=0:
          mainLog.error('Combine failed...')
          # return __BAD__


  if opt.verb>0: p8 = printTime(p7,start,mainLog)
  os.remove(pidfile)

  mainLog.info('This process has ended. Label=%r', Label)
  return 42



if __name__ == "__main__":
  print "This is the __main__ part"

  #workingPath = os.getcwd()
  # parentDir = os.path.abspath(os.path.join(workingPath, os.pardir))
  #if opt.verb: print workingPath

  with open(opt.configName, 'r') as fp:
    Params = json.load(fp)

  if opt.verb>1:
    print '\t Input JSON config file:'
    print json.dumps(Params, sort_keys=True, indent=4)


  baseFolder=opt.outDir

  createDir(baseFolder, over=opt.overwrite)

  copy(opt.configName, baseFolder)

  logging.basicConfig(level=logLvl,
                      format='%(asctime)s PID:%(process)d %(name)-12s %(levelname)-8s %(message)s',
                      datefmt='%m-%d %H:%M',
                      filename=baseFolder+'/mainLog_'+time.strftime("%Y%m%d-%H%M%S")+'.log',
                      filemode='w')

  mainLog = logging.getLogger('Main.Log')
  mainLog.info('Main Log started')

  mainLog.info(pformat(opt))


  createDir('/tmp/'+__username__+'/PIDs/',mainLog,True)

  res = None
  if opt.mass!=None:
    mainLog.info('Running over mass:\n'+pformat(opt.mass))
    res = runFullChain(opt, Params, opt.mass, -1, str(opt.extraLabel))

  if opt.node!=None:
    mainLog.info('Running over node:\n'+pformat(opt.node))
    res = runFullChain(opt, Params, opt.node, -1, str(opt.extraLabel))


  end = time.time()

  mainLog.info("Result of this job = %r" % res)
  mainLog.info('\t Total Time: %.2f'%(end-begin))

  mainLog.info('My Main Log Finished')
