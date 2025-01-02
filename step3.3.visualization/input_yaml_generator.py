#!/usr/bin/env python3
import yaml

FILE_IDENTIFIER = 'input_yaml_generator.py'
def info(mesg):
    print(f'i-{FILE_IDENTIFIER}@ {mesg}')


BUILT_IN_X_AXIS = {
        'gjet': 'BDTG score ($\gamma$)',
        'cvsb': 'C vs B score',
        'cvsl': 'C vs L score',
        'btag': 'b Score',
                   }

def create_yaml(
        templateFILE:str,
        xVAR:str,
        inROOTfile:str,
        ):
    out_file_name = f'input.{xVAR}.yaml'

    f_template = open(templateFILE, 'r')
    info(f'[ExportYAML] Config file {out_file_name}')
    with open(out_file_name, 'w') as f_out:
        f_out.write( f_template.read().format(
            var=xVAR,
            inFILE=inROOTfile,
            xTITLE=BUILT_IN_X_AXIS[xVAR]
            ))
    info(f'[ExportYAML] Config file {out_file_name} generated')

if __name__ == "__main__":
    from collections import namedtuple
    io = namedtuple('IOArgs', 'yaml_template hist_source')
    import sys
    inARGs = io(*sys.argv[1:])

    template_file_input = inARGs.yaml_template
    info(f'[TemplateFile] Use template file {template_file_input}')
    for xvar in [ 'gjet', 'btag', 'cvsb', 'cvsl']:
        create_yaml(
            inARGs.yaml_template,
            xvar,
            inARGs.hist_source,
        )
