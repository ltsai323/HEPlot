submit condor_job
1. Compile executable by g++ -L/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/external/slc7_amd64_gcc900/bin/../../../../../../../slc7_amd64_gcc900/lcg/root/6.22.08-ljfedo/lib -lCore -lImt -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lROOTVecOps -lTree -lTreePlayer -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -lMultiProc -lROOTDataFrame -pthread -lm -ldl -rdynamic -pthread -std=c++17 -m64 -I/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/external/slc7_amd64_gcc900/bin/../../../../../../../slc7_amd64_gcc900/lcg/root/6.22.08-ljfedo/include.
2. Put PATH and LD_LIBRARY_PATH into shell script.
    * If you want to record the current environment PATH and LD_LIBRARY_PATH to the file, check the content before every submition.
    * Also you can use `condor_submit a.sub -batch-name submit_with_generated_env -append "environment=PATH=$PATH;LD_LIBRARY_PATH=$LD_LIBRARY_PATH"`in the CLI, note that .sub file does not access bash variable.
