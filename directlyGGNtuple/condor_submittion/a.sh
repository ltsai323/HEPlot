#!/usr/bin/env sh
outputFILE=$1
inputFILEs=$2

#export PATH=/cvmfs/cms.cern.ch/share/overrides/bin:/wk_cms3/ltsai/wk_cms/ltsai/CMSSW_11_3_4/bin/slc7_amd64_gcc900:/wk_cms3/ltsai/wk_cms/ltsai/CMSSW_11_3_4/external/slc7_amd64_gcc900/bin:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/bin/slc7_amd64_gcc900:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/external/slc7_amd64_gcc900/bin:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/llvm/11.1.0-llifpc/bin:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gcc/9.3.0/bin:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gsl/2.6-ljfedo/bin:/home/ltsai/local/bin:/home/ltsai/local/usr/bin:/cvmfs/cms.cern.ch/common:/home/ltsai/scripts:/usr/sue/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/usr/pbs/bin:/usr/ptl/bin:/opt/puppetlabs/bin:/home/ltsai/script/tools/:/home/ltsai/bin
#export LD_LIBRARY_PATH=/wk_cms3/ltsai/wk_cms/ltsai/CMSSW_11_3_4/biglib/slc7_amd64_gcc900:/wk_cms3/ltsai/wk_cms/ltsai/CMSSW_11_3_4/lib/slc7_amd64_gcc900:/wk_cms3/ltsai/wk_cms/ltsai/CMSSW_11_3_4/external/slc7_amd64_gcc900/lib:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/biglib/slc7_amd64_gcc900:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/lib/slc7_amd64_gcc900:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/external/slc7_amd64_gcc900/lib:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/llvm/11.1.0-llifpc/lib64:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gcc/9.3.0/lib64:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gcc/9.3.0/lib:/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cuda/11.2.2/drivers::/home/ltsai/local/usr/lib/:/home/ltsai/local/lib




/wk_cms3/ltsai/wk_cms/ltsai/workspace/directlyGGNtuple/a $1 $2
