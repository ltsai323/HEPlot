### efficiency B
cp data/input.drawplotable.binconsistency_effB_WPcLoose.yaml input.drawplotable.binconsistency_effB_WPcLoose.yaml 
sed 's/Loose/Medium/g;s/WPcL/WPcM/g' input.drawplotable.binconsistency_effB_WPcLoose.yaml > input.drawplotable.binconsistency_effB_WPcMedium.yaml
sed 's/Loose/Tight/g;s/WPcL/WPcT/g'  input.drawplotable.binconsistency_effB_WPcLoose.yaml > input.drawplotable.binconsistency_effB_WPcTight.yaml

sed 's/WPc/WPb/g'                    input.drawplotable.binconsistency_effB_WPcLoose.yaml  > input.drawplotable.binconsistency_effB_WPbLoose.yaml
sed 's/WPc/WPb/g'                    input.drawplotable.binconsistency_effB_WPcMedium.yaml > input.drawplotable.binconsistency_effB_WPbMedium.yaml
sed 's/WPc/WPb/g'                    input.drawplotable.binconsistency_effB_WPcTight.yaml  > input.drawplotable.binconsistency_effB_WPbTight.yaml



### efficiency C
sed 's/\epsilon_{b}/\epsilon_{c}/;s/B_/C_/g' input.drawplotable.binconsistency_effB_WPcLoose.yaml  > input.drawplotable.binconsistency_effC_WPcLoose.yaml
sed 's/\epsilon_{b}/\epsilon_{c}/;s/B_/C_/g' input.drawplotable.binconsistency_effB_WPcMedium.yaml > input.drawplotable.binconsistency_effC_WPcMedium.yaml
sed 's/\epsilon_{b}/\epsilon_{c}/;s/B_/C_/g' input.drawplotable.binconsistency_effB_WPcTight.yaml  > input.drawplotable.binconsistency_effC_WPcTight.yaml

sed 's/\epsilon_{b}/\epsilon_{c}/;s/B_/C_/g' input.drawplotable.binconsistency_effB_WPbLoose.yaml  > input.drawplotable.binconsistency_effC_WPbLoose.yaml
sed 's/\epsilon_{b}/\epsilon_{c}/;s/B_/C_/g' input.drawplotable.binconsistency_effB_WPbMedium.yaml > input.drawplotable.binconsistency_effC_WPbMedium.yaml
sed 's/\epsilon_{b}/\epsilon_{c}/;s/B_/C_/g' input.drawplotable.binconsistency_effB_WPbTight.yaml  > input.drawplotable.binconsistency_effC_WPbTight.yaml


### efficiency L
sed 's/\epsilon_{b}/\epsilon_{l}/;s/B_/L_/g' input.drawplotable.binconsistency_effB_WPcLoose.yaml  > input.drawplotable.binconsistency_effL_WPcLoose.yaml
sed 's/\epsilon_{b}/\epsilon_{l}/;s/B_/L_/g' input.drawplotable.binconsistency_effB_WPcMedium.yaml > input.drawplotable.binconsistency_effL_WPcMedium.yaml
sed 's/\epsilon_{b}/\epsilon_{l}/;s/B_/L_/g' input.drawplotable.binconsistency_effB_WPcTight.yaml  > input.drawplotable.binconsistency_effL_WPcTight.yaml

sed 's/\epsilon_{b}/\epsilon_{l}/;s/B_/L_/g' input.drawplotable.binconsistency_effB_WPbLoose.yaml  > input.drawplotable.binconsistency_effL_WPbLoose.yaml
sed 's/\epsilon_{b}/\epsilon_{l}/;s/B_/L_/g' input.drawplotable.binconsistency_effB_WPbMedium.yaml > input.drawplotable.binconsistency_effL_WPbMedium.yaml
sed 's/\epsilon_{b}/\epsilon_{l}/;s/B_/L_/g' input.drawplotable.binconsistency_effB_WPbTight.yaml  > input.drawplotable.binconsistency_effL_WPbTight.yaml
