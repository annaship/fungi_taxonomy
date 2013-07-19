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

# import os
# from stat import * # ST_SIZE etc
# import sys
# import shutil
# import types
# from time import sleep
# 
# 
import argparse
# "taxonomy_id","taxonomy"
# 4396,"Eukarya;Fungi"
# 33425,"Eukarya;Fungi;"
# 4397,"Eukarya;Fungi;Ascomycota"
# 566729,"Eukarya;Fungi;Blastocladiomycota;Blastocladiomycetes;Blastocladiales;Blastocladiaceae;Allomyces;Allomyces;anomalus"

def uniq_array(arr): 
   # order preserving
   noDupes = []
   [noDupes.append(i) for i in arr if not noDupes.count(i)]
   return noDupes


def process(args):
    tax_infile = args.tax_infile
    taxout_fh  = open(args.tax_outfile,'w')
    
    # TAXONOMY FILE
    for line in open(tax_infile):
        new_tax_line = {}
        
        # 566729,"Eukarya;Fungi;  Blastocladiomycota;Blastocladiomycetes;Blastocladiales;Blastocladiaceae;Allomyces;Allomyces;anomalus"
        #                 kingdom;phylum            ;class              ;order          ;family          ;genus              ;species
        line = line.strip()
        # print line
        if not line:
            continue
        
        id_tax    = line.split(',')
        split_tax = id_tax[1].strip('"').split(';')
        # print "id = %s, split_tax = %s" % (id_tax, split_tax)
        # print "id_tax = %s" % (id_tax)
        # print "split_tax = %s" % (split_tax)
        unique_split_tax = uniq_array(split_tax)
        print "unique_split_tax = %s" % (unique_split_tax)
        arr_size = len(unique_split_tax)
        
        # domain         = 'Eukarya'
        new_tax_line["kingdom_phylum"] = ""
        new_tax_line["class"]          = ""
        new_tax_line["order"]          = ""
        new_tax_line["family"]         = ""
        new_tax_line["genus"]          = ""
        new_tax_line["species"]        = ""
        for taxon in unique_split_tax:
            # http://species.wikimedia.org/wiki/Fungi
            # Phyla: Ascomycota - Basidiomycota - Blastocladiomycota - Chytridiomycota - Glomeromycota - Microsporidia - Neocallimastigomycota - Zygomycota - Fungi incertae sedis
            if taxon.endswith("mycota") or taxon == "Microsporidia":
                new_tax_line["kingdom_phylum"] = "Fungi" + "_" + taxon
            if taxon.endswith("mycetes"):
                new_tax_line["class"] = taxon
            if taxon.endswith("ales"):
                new_tax_line["order"] = taxon
            if taxon.endswith("aceae"):
                new_tax_line["family"] = taxon
        if arr_size == int(2) or (arr_size == int(3) and unique_split_tax[2] == ''):
            print "HERE: %s" % unique_split_tax
            new_tax_line["kingdom_phylum"] = "Fungi"
        if arr_size >= 6:
            new_tax_line["family"] = unique_split_tax[6]
        if arr_size >= 7:
            new_tax_line["species"] = unique_split_tax[7]
            
        # # k__Fungi;p__Basidiomycota;c__Agaricomycetes;o__Thelephorales;f__Thelephoraceae;g__Thelephora;s__Thelephora_terrestris
        # if arr_size > 2:
        #     if (unique_split_tax[1] == 'Fungi' and unique_split_tax[2] != ''):
        #         kingdom_phylum = unique_split_tax[1] + "_" + unique_split_tax[2]            
        # if arr_size > 3:
        #     new_class  = unique_split_tax[3]
        # if arr_size > 4:
        #     new_orderx = unique_split_tax[4]
        # if arr_size > 5:
        #     new_family = unique_split_tax[5]
        # family         =
        # genus          =
        # species        =
        # strain         =
        
        # print "kingdom_phylum = %s; new_class = %s; new_orderx = %s; new_family = %s" % (kingdom_phylum, new_class, new_orderx, new_family)
        print "kingdom_phylum = %s; class = %s; order = %s; family = %s, species = %s" % (new_tax_line["kingdom_phylum"], new_tax_line["class"], new_tax_line["order"], new_tax_line["family"], new_tax_line["species"])
         # todo: split species and unique again
        
        # for i in tax_items:
        #     name = i.split('__')[1]
        #     if i[0] == 'k':
        #         pass
        #     if i[0] == 'p':
        #         if name=='unidentified' or name=='Incertae_sedis':
        #             new_tax.append('Fungi_NA')
        #         else:
        #             new_tax.append('Fungi_'+name)
        #     if i[0] == 'c':
        #         if name=='unidentified' or name=='Incertae_sedis':
        #             name='Class_NA'
        #         new_tax.append(name)
        #     if i[0] == 'o':
        #         if name=='unidentified' or name=='Incertae_sedis':
        #             name='Order_NA'
        #         new_tax.append(name)
        #     if i[0] == 'f':
        #         if name=='unidentified' or name=='Incertae_sedis':
        #             name='Family_NA'
        #         new_tax.append(name)
        #         
        #     if i[0] == 'g':
        #         genus = name
        #         if name=='unidentified' or name=='Incertae_sedis':
        #             name='Genus_NA'
        #         new_tax.append(name)
        #     if i[0] == 's':
        #         species = name
        #         #print line
        #         if(species.find(genus,0,len(genus)) != -1 and species != genus):
        #             species = species.split('_')[1]
        #         new_tax.append(species)
        #     
        # 
        #     
        # taxonomy = ';'.join(new_tax)
        # 
        # print taxonomy
        # taxout_fh.write(id+"\t"+taxonomy+"\n")
        #     #out_fh.write('>'+id+"\n")
        #  
        #  
        #  
 
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

