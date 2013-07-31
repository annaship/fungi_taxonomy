#! /opt/local/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
# ver 2 2013 Jul 19 - convert taxonomy table
# ver 3 2013 Jul 31 - convert taxonomy table, remove all trailing garbage, leave insertae_cedis
# 1)
# GU295056        k__Fungi;p__Ascomycota;c__Sordariomycetes;o__Incertae_sedis;f__Glomerellaceae;g__Glomerella;s__Colletotrichum_gloeosporioides
# 
# 2)
# GU319887        k__Fungi;p__unidentified;c__unidentified;o__unidentified;f__unidentified;g__unidentified;s__fungal_sp_QP_2010
# 
# 3)
# FJ820581        k__Fungi;p__Basidiomycota;c__Agaricomycetes;o__Thelephorales;f__Thelephoraceae;g__Thelephora;s__unculturedfungus

import argparse

def uniq_array(arr): 
   # order preserving
   noDupes = []
   [noDupes.append(i) for i in arr if not noDupes.count(i)]
   return noDupes
   
def make_taxa_dict(tax_infile):
    taxonomy = {}
    
    for line in open(tax_infile):
        tax_line = {}
        
        line = line.strip()
        # print line
        # if not line:
        #     continue
        tax_line_split = line.split()
        split_tax = tax_line_split[1].split(';')
        id_tax    = tax_line_split[0]
        # print "\n===========\nid_tax = %s, split_tax = %s" % (id_tax, split_tax)
        
        # domain         = 'Eukarya'
        # tax_line["kingdom_phylum"] = ""
        tax_line["class"]          = ""
        tax_line["order"]          = ""
        tax_line["family"]         = ""
        tax_line["genus"]          = ""
        tax_line["species"]        = ""
        for taxon in split_tax:
            # http://species.wikimedia.org/wiki/Fungi
            # Phyla: Ascomycota - Basidiomycota - Blastocladiomycota - Chytridiomycota - Glomeromycota - Microsporidia - Neocallimastigomycota - Zygomycota - Fungi incertae sedis
            # FJ820581        k__Fungi;p__Basidiomycota;c__Agaricomycetes;o__Thelephorales;f__Thelephoraceae;g__Thelephora;s__unculturedfungus
            # print "taxon = %s" % taxon
            
            if taxon.startswith("k__"):
                tax_line["kingdom"] = "Fungi"
            if taxon.startswith("p__"):
                tax_line["phylum"] = taxon.split("__")[1]                
            if taxon.startswith("c__"):
                tax_line["class"] = taxon.split("__")[1]
            if taxon.startswith("o__"):
                tax_line["order"] = taxon.split("__")[1]
            if taxon.startswith("f__"):
                tax_line["family"] = taxon.split("__")[1]
            if taxon.startswith("g__"):
                tax_line["genus"] = taxon.split("__")[1]
            if taxon.startswith("s__"):
                tax_line["species"] = taxon.split("__")[1]
        taxonomy[id_tax] = tax_line
    return taxonomy
    
def remove_empty(tax_line, name):
    if tax_line[name] in ("unculturedfungus", "Fungi", "unidentified"):
        # print "HERE: name = %s, tax_line[name] = %s" % (name, tax_line[name])
        tax_line[name] = ''
    return tax_line[name]
    
def remove_empty_from_end(ordered_names, old_taxonomy):
    taxonomy_with_wholes = {}
    for tax_id, tax_line in old_taxonomy.items():
        for name in reversed(ordered_names):
            res_taxa = remove_empty(tax_line, name)
            if res_taxa != '':
                break
        # print tax_line
        taxonomy_with_wholes[tax_id] = tax_line
    return taxonomy_with_wholes
    
    
def make_kingdom_phylum(tax_line):
    return (tax_line["kingdom"] + "_" + tax_line["phylum"])
    
def separate_binomial_name(species):
    pass
    
def process(args):
    tax_infile    = args.tax_infile
    taxout_fh     = open(args.tax_outfile,'w')
    ordered_names = "phylum", "class", "order", "family", "genus", "species"
    old_taxonomy  = make_taxa_dict(tax_infile)
    taxonomy_with_wholes = remove_empty_from_end(ordered_names, old_taxonomy)
    
    print taxonomy_with_wholes


 
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

