#Sample name, sum of weights, xsec*br (in fb)
hggbr = 2.27e-3
genDiPhoFilterFactor = 1./(1 - 0.06)
#factor comes from the fact that pythia includes H->gamma*gamma->llgamma, while branching fraction from YR4  does not
#for more info, see: https://indico.cern.ch/event/598436/contributions/2529023/attachments/1434414/2205057/Zenz-News-Hgg-27Mar-v2.pdf
# below the list contains bTagNF yearwise for all SignalH sample
SMHiggsNodes = [
    ['output_GluGluHToGG_M-125_13TeV_powheg_pythia8.root', 1.0505, 1.0881, 1.053],
    ['output_VBFHToGG_M-125_13TeV_powheg_pythia8.root', 1.0468, 1.069, 1.0398],
    ['output_VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8.root', 1.0495, 1.071, 1.0497],
    ['output_ttHToGG_M125_13TeV_powheg_pythia8.root', 1.0523, 1.0553, 1.0241],
    ['output_bbHToGG_M-125_4FS_yb2_13TeV_amcatnlo.root', 1.0587, 1.0631, 1.0419],
    ['output_bbHToGG_M-125_4FS_ybyt_13TeV_amcatnlo.root', 1.0326, 1.0352, 1.0277]
]
SignalNodes = [
    ['Radion260', 1.0652, 1.1089, 1.0887],
    ['Radion270', 1.0628, 1.1058, 1.0865],
    ['Radion280', 1.0637, 1.1043, 1.0845],
    ['Radion300', 1.0610, 1.1001, 1.0806],
    ['Radion320', 1.0568, 1.0959, 1.0778],
    ['Radion350', 1.0548, 1.0897, 1.0721],
    ['Radion400', 1.0504, 1.0843, 1.0656],
    ['Radion450', 1.0465, 1.0778, 1.0605],
    ['Radion500', 1.0445, 1.0722, 1.0571],
    ['Radion550', 1.0422, 1.0675, 1.0540],
    ['Radion600', 1.0411, 1.0650, 1.0523],
    ['Radion650', 1.0408, 1.0631, 1.0490],
    ['Radion700', 1.0404, 1.0597, 1.0467],
    ['Radion800', 1.0368, 1.0563, 1.0421],
    ['Radion900', 1.0371, 1.0510, 1.0399],
    ['Radion1000',1.0071, 1.0502, 1.0368]
]
