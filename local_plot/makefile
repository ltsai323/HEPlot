self:=makefile

check_defined = \
    $(strip $(foreach 1,$1, \
    $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
    $(error Undefined $1$(if $2, ($2))))


goal1: goal1-allcmd ## run all commands under goal1 [oTAG=hii]
goal1-allcmd: \
	goal1-get_postfit_shape \
	goal1-collect_output \
	goal1-draw_plots

btag := psuedofit_datacard_btag.root
cvsl := psuedofit_datacard_cvsl.root
cvsb := psuedofit_datacard_cvsb.root
goal1-get_postfit_shape: ## Load shape in datacard for further drawing [btag=psuedofit_datacard_btag.root][cvsl=psuedofit_datacard_cvsl.root][cvsb=psuedofit_datacard_cvsb.root]
	python3 get_postfit_shape.py $(btag) fitshape_btag.root gjet_btag
	python3 get_postfit_shape.py $(cvsb) fitshape_cvsb.root gjet_cvsb
	python3 get_postfit_shape.py $(cvsl) fitshape_cvsl.root gjet_cvsl
goal1-collect_output: ## Rename psuedofit_datacard_btag.root and fitshape_btag.root with oTAG [oTAG=hi]
	$(call check_defined,oTAG)
	mv fitshape_btag.root           $(oTAG)_fitshape_btag.root
	mv fitshape_cvsb.root           $(oTAG)_fitshape_cvsb.root
	mv fitshape_cvsl.root           $(oTAG)_fitshape_cvsl.root
goal1-draw_plots: ## Draw plots from result of goal1-get_postfit_shape [oTAG=hi]
	$(call check_defined,oTAG)
	DrawRatioPlotablesWithCMSFormat.py input.check.postfit.btag.yaml commonINPUTfile=$(oTAG)_fitshape_btag.root figNAME=figs/check.$(oTAG).btag.pdf
	DrawRatioPlotablesWithCMSFormat.py input.check.postfit.cvsb.yaml commonINPUTfile=$(oTAG)_fitshape_cvsb.root figNAME=figs/check.$(oTAG).cvsb.pdf
	DrawRatioPlotablesWithCMSFormat.py input.check.postfit.cvsl.yaml commonINPUTfile=$(oTAG)_fitshape_cvsl.root figNAME=figs/check.$(oTAG).cvsl.pdf



goal2: goal2-allcmd ## run all commands under goal2 [makehisto=makehisto_binned_ctagfit_psuedodata__0_0_600_800.root]

goal2-allcmd: \
	goal2-makehisto_shapes \
	goal2a-draw_plots \
	goal2b-draw_plots_forkinematics

makehisto := makehisto_binned_ctagfit_psuedodata__0_0_600_800.root
goal2-makehisto_shapes: ## Get histogram shapes from makehisto.root [makehisto=makehisto_binned_ctagfit_psuedodata__0_0_600_800.root]
	python3 get_makehisto_shape.py $(makehisto) makehisto_shape.root

goal2a-create_yaml_configs: ## Use sed generating yaml configs
	cp                                                                input.makehisto.cvsl.yaml    input.makehistoL.cvsl.yaml
	sed -e 's/cvsl/cvsb/g' -e's/CvsL/CvsB/g'                          input.makehisto.cvsl.yaml  > input.makehistoL.cvsb.yaml
	sed -e 's/cvsl/btag/g' -e's/CvsL/bTagging Score/g'                input.makehisto.cvsl.yaml  > input.makehistoL.btag.yaml
	sed                                                -e 's/L_/C_/g' input.makehisto.cvsl.yaml  > input.makehistoC.cvsl.yaml
	sed -e 's/cvsl/cvsb/g' -e's/CvsL/CvsB/g'           -e 's/L_/C_/g' input.makehisto.cvsl.yaml  > input.makehistoC.cvsb.yaml
	sed -e 's/cvsl/btag/g' -e's/CvsL/bTagging Score/g' -e 's/L_/C_/g' input.makehisto.cvsl.yaml  > input.makehistoC.btag.yaml
	sed                                                -e 's/L_/B_/g' input.makehisto.cvsl.yaml  > input.makehistoB.cvsl.yaml
	sed -e 's/cvsl/cvsb/g' -e's/CvsL/CvsB/g'           -e 's/L_/B_/g' input.makehisto.cvsl.yaml  > input.makehistoB.cvsb.yaml
	sed -e 's/cvsl/btag/g' -e's/CvsL/bTagging Score/g' -e 's/L_/B_/g' input.makehisto.cvsl.yaml  > input.makehistoB.btag.yaml

goal2a-draw_plots: ## Draw plots from yaml configs
	DrawRatioPlotablesWithCMSFormat.py input.makehistoL.cvsl.yaml figNAME=figs/check.makehistoL_cvsl.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehistoL.cvsb.yaml figNAME=figs/check.makehistoL_cvsb.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehistoL.btag.yaml figNAME=figs/check.makehistoL_btag.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehistoC.cvsl.yaml figNAME=figs/check.makehistoC_cvsl.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehistoC.cvsb.yaml figNAME=figs/check.makehistoC_cvsb.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehistoC.btag.yaml figNAME=figs/check.makehistoC_btag.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehistoB.cvsl.yaml figNAME=figs/check.makehistoB_cvsl.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehistoB.cvsb.yaml figNAME=figs/check.makehistoB_cvsb.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehistoB.btag.yaml figNAME=figs/check.makehistoB_btag.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.btag_orig.yaml figNAME=figs/check.makehisto_btag_orig.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.cvsb_orig.yaml figNAME=figs/check.makehisto_cvsb_orig.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.cvsl_orig.yaml figNAME=figs/check.makehisto_cvsl_orig.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.btag_calb.yaml figNAME=figs/check.makehisto_btag_calb.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.cvsb_calb.yaml figNAME=figs/check.makehisto_cvsb_calb.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.cvsl_calb.yaml figNAME=figs/check.makehisto_cvsl_calb.pdf

goal2b-create_yaml_configs_forkinematics: ## Use sed generating yaml configs
	sed -e 's/phopt/phoeta/g'                                         input.makehisto.phopt.yaml > input.makehisto.phoeta.yaml
	sed -e 's/phopt/phophi/g'                                         input.makehisto.phopt.yaml > input.makehisto.phophi.yaml
	sed -e 's/phopt/jetpt/g'                                          input.makehisto.phopt.yaml > input.makehisto.jetpt.yaml
	sed -e 's/phopt/jeteta/g'                                         input.makehisto.phopt.yaml > input.makehisto.jeteta.yaml
	sed -e 's/phopt/jetphi/g'                                         input.makehisto.phopt.yaml > input.makehisto.jetphi.yaml
	sed -e 's/phopt/njet/g'                                           input.makehisto.phopt.yaml > input.makehisto.njet.yaml

goal2b-draw_plots_forkinematics: ## draw plots
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.phopt.yaml  lowerpad/xLABEL='photon pt'  figNAME=figs/check.makehisto_phopt.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.phoeta.yaml lowerpad/xLABEL='photon eta' figNAME=figs/check.makehisto_phoeta.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.phophi.yaml lowerpad/xLABEL='photon phi' figNAME=figs/check.makehisto_phophi.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.jetpt.yaml  lowerpad/xLABEL='jet pt'     figNAME=figs/check.makehisto_jetpt.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.jeteta.yaml lowerpad/xLABEL='jet eta'    figNAME=figs/check.makehisto_jeteta.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.jetphi.yaml lowerpad/xLABEL='jet phi'    figNAME=figs/check.makehisto_jetphi.pdf
	DrawRatioPlotablesWithCMSFormat.py input.makehisto.njet.yaml   lowerpad/xLABEL='njets'      figNAME=figs/check.makehisto_njets.pdf

IN_ARGS = [opts]


help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[32m<command>\033[0m $(IN_ARGS)\n\nCommands:\n\033[36m\033[0m\n"} \
	/^[0-9a-zA-Z_-]+:.*?##/ { gsub(/\\n/, "\n                   "); printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } \
	/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

