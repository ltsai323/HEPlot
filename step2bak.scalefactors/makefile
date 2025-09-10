self:=makefile
iFILE=scalefactors_and_uncertainties.root

check_defined = \
    $(strip $(foreach 1,$1, \
    $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
    $(error Undefined $1$(if $2, ($2))))

oTAG:=hii
compare: ## Plot 2 TGraphAsymmError and Compare difference of them [iFILE=scalefactors_and_uncertainties.root][nCOMP=effL0][nORIG=origeffL0][oTAG=hii]
	$(call check_defined,nCOMP)
	$(call check_defined,nORIG)
	python3 create_compare.py $(iFILE) $(nCOMP) $(nORIG) && DrawRatioPlotablesWithCMSFormat.py input_create_compare.yaml && mv t.pdf h_$(oTAG).pdf

compare_all: ## plot all eff comparison [iFILE=scalefactors_and_uncertainties.root]
	$(MAKE) -f $(self) compare iFILE=$(iFILE) nCOMP=effL0 nORIG=origeffL0 oTAG=effL0
	$(MAKE) -f $(self) compare iFILE=$(iFILE) nCOMP=effC0 nORIG=origeffC0 oTAG=effC0
	$(MAKE) -f $(self) compare iFILE=$(iFILE) nCOMP=effB0 nORIG=origeffB0 oTAG=effB0
	$(MAKE) -f $(self) compare iFILE=$(iFILE) nCOMP=effL1 nORIG=origeffL1 oTAG=effL1
	$(MAKE) -f $(self) compare iFILE=$(iFILE) nCOMP=effC1 nORIG=origeffC1 oTAG=effC1
	$(MAKE) -f $(self) compare iFILE=$(iFILE) nCOMP=effB1 nORIG=origeffB1 oTAG=effB1


IN_ARGS = [opts]


help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[32m<command>\033[0m $(IN_ARGS)\n\nCommands:\n\033[36m\033[0m\n"} \
	/^[0-9a-zA-Z_-]+:.*?##/ { gsub(/\\n/, "\n                   "); printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } \
	/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
