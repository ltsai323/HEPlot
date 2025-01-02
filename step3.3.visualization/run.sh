file_postfit=postfit.root
file_yaml_template=data/input.template.yaml

FILE_PLOTABLE=secondary_plotable.root
function the_exit() { echo $1; exit 1; }

mkdir outputs
python3 secondary_plotable.py $file_postfit $FILE_PLOTABLE || the_exit "[Error] secondary_plotable.py reports error."
python3 input_yaml_generator.py $file_yaml_template $FILE_PLOTABLE || the_exit "[Error] input_yaml_generator.py reports error."

# input.cvsl.yaml input.cvsb.yaml input.btag.yaml input.gjet.yaml generated.
DrawRatioPlotablesWithCMSFormat.py input.gjet.yaml || the_exit "[ERROR] DrawRatioPlotablesWithCMSFormat.py input.gjet.yaml reports error"
DrawRatioPlotablesWithCMSFormat.py input.btag.yaml || the_exit "[ERROR] DrawRatioPlotablesWithCMSFormat.py input.btag.yaml reports error"
DrawRatioPlotablesWithCMSFormat.py input.cvsl.yaml || the_exit "[ERROR] DrawRatioPlotablesWithCMSFormat.py input.cvsl.yaml reports error"
DrawRatioPlotablesWithCMSFormat.py input.cvsb.yaml || the_exit "[ERROR] DrawRatioPlotablesWithCMSFormat.py input.cvsb.yaml reports error"
