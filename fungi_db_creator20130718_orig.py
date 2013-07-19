#!/usr/bin/env python

##!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
from stat import * # ST_SIZE etc
import sys
import shutil
import types
from time import sleep


import argparse
# >DQ068970|
#Thelephora terrestris|
#Fungi; Basidiomycota; Agaricomycotina; Agaricomycetes; Incertae sedis; Thelephorales; Thelephoraceae; Thelephora; Thelephora terrestris|
#Thelephora terrestris|
#Fungi; Basidiomycota; Agaricomycotina; Agaricomycetes; Incertae sedis; Thelephorales; Thelephoraceae; Thelephora; Thelephora terrestris


def process(args):
    tax_infile = args.tax_infile
    #fa_infile = args.fasta_infile
        
    
    taxout_fh = open(args.tax_outfile,'w')
    #faout_fh = open(args.fasta_outfile,'w')
    
    seq_lookup={}
    id_lookup={}
    
    # FASTA FILE
    #for line in open(fa_infile):
        # line ex: 
    #   line = line.strip()
    
    
    
    # TAXONOMY FILE
    for line in open(tax_infile):
        # DQ482002  k__Fungi;p__Basidiomycota;c__Agaricomycetes;o__Thelephorales;f__Thelephoraceae;g__Tomentella;s__Tomentella_sublilacina
        line = line.strip()
        #print line
        if not line:
            continue
        items = line.split('\t')
        id = items[0]
        pretax = items[1]
        tax_items=pretax.split(';')
        
        
        
        
        new_tax = ['Eukayra']
        for i in tax_items:
            name = i.split('__')[1]
            if i[0] == 'k':
                pass
            if i[0] == 'p':
                if name=='unidentified' or name=='Incertae_sedis':
                    new_tax.append('Fungi_NA')
                else:
                    new_tax.append('Fungi_'+name)
            if i[0] == 'c':
                if name=='unidentified' or name=='Incertae_sedis':
                    name='Class_NA'
                new_tax.append(name)
            if i[0] == 'o':
                if name=='unidentified' or name=='Incertae_sedis':
                    name='Order_NA'
                new_tax.append(name)
            if i[0] == 'f':
                if name=='unidentified' or name=='Incertae_sedis':
                    name='Family_NA'
                new_tax.append(name)
                
            if i[0] == 'g':
                genus = name
                if name=='unidentified' or name=='Incertae_sedis':
                    name='Genus_NA'
                new_tax.append(name)
            if i[0] == 's':
                species = name
                #print line
                if(species.find(genus,0,len(genus)) != -1 and species != genus):
                    species = species.split('_')[1]
                new_tax.append(species)
            
        
            
        taxonomy = ';'.join(new_tax)
        
        print taxonomy
        taxout_fh.write(id+"\t"+taxonomy+"\n")
            #out_fh.write('>'+id+"\n")
 
 
 
 
if __name__ == '__main__':
    THE_DEFAULT_BASE_OUTPUT = '.'

    usage = "usage: %prog [options] arg1"
    parser = argparse.ArgumentParser(description='ref fasta/tax file creator')
    parser.add_argument('-it', '--tax_in', required=True, dest = "tax_infile",
                                                 help = '')   
    #parser.add_argument('-if', '--fasta_in', required=True, dest = "fasta_infile",
    #                                             help = '')
    parser.add_argument('-ot', '--tax_out', required=False, dest = "tax_outfile",   default='outfile.tax',
                                                 help = '')
    #parser.add_argument('-of', '--fasta_out', required=False, dest = "fasta_outfile", default='outfile.fasta',
    #                                             help = '')                                            
    args = parser.parse_args() 
    
     

    # now do all the work
    process(args)

