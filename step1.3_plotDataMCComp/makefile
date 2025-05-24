.PHONY: help
timeSTAMP=$$(date "+%Y%m%d_%H%M")

check_defined = \
    $(strip $(foreach 1,$1, \
    $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
    $(error Undefined $1$(if $2, ($2))))

edityamls: ## edit yaml file using sed [sedCMD='s/1\.5/4.5/g']
	for a in input*.yaml; do sed -i.bak  's/1e-2/1e-1/g'  $$a;done
	#for a in input*.yaml; do sed -i.bak  's/hist2/histBKG/g'  $$a;done
	#for a in input*.yaml; do sed -i.bak  's/linear/log/g'  $$a;done
	#for a in input*.yaml; do sed -i.bak  's/1\.5/4.5/g' $$a;done
plot: ## draw all yaml files [inROOT=output_WPb_loose.root][oTAG]
	$(call check_defined, inROOT)
	$(call check_defined, oTAG)
	touch o.root ; /bin/rm o.root
	touch outputs; /bin/rm -r outputs
	ln -s $(inROOT) o.root
	mkdir outputs
	for a in input.*.yaml; do DrawRatioPlotablesWithCMSFormat.py $$a;done
	mkdir -p figs$(oTAG)_$(timeSTAMP)
	mv outputs/* figs$(oTAG)_$(timeSTAMP)/
	unlink o.root
	@echo "output folder: figs$(oTAG)_$(timeSTAMP)"
massiveplot:
	$(call check_defined, inROOT)
	for a in cut_phopt200/output*.root; do ccc=`basename $$a`; cc=$${ccc%.root}; tag=$${cc#output_};  make plot oTAG=$$tag inROOT=$$a ;done
plotall: ## draw all yaml files from root files [rootFOLDER=hi/]
	$(call check_defined, rootFOLDER)
	@for a in $(rootFOLDER)/output_*.root; do \
		ccc=`basename $${a}`; \
		cc=$${ccc%.root}; \
		tag=$${cc#output_}; \
		make plot oTAG=$${tag} inROOT=$${a}; \
	done
	mkdir -p allfigs_`basename $(rootFOLDER)`
	mv figs* allfigs_`basename $(rootFOLDER)`

	
	
#tar: ## make a tarball to outputs.tar
#	tar -cf outputs.tar outputs/*.pdf
clean: ## clean output pictures
	/bin/rm outputs/*
	/bin/rm -r allfig*



IN_ARGS = [opts]

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[32m<command>\033[0m $(IN_ARGS)\n\nCommands:\n\033[36m\033[0m\n"} /^[0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
