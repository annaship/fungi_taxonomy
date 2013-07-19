import sys

def main(args):
    try: 
        input_file = args.input_file
    except IOError:
        print 'Error: Please provide a valid input file name with taxonomy: "%s"'\
                % args.input_file
        sys.exit(-1)
    
    if args.output_file:
        output_file_path = args.output_file
    else:
        output_file_path = args.input_file + '.csv'

    try:
        output = open(output_file_path, 'w')        
    except IOError:
        print 'Error: You have no permission to write destination: "%s"'\
                    % output_file_path
        sys.exit(-1)

    for line in open(input_file):
        # AJ633596        Eukayra;Fungi_Basidiomycota;Agaricomycetes;Thelephorales;Thelephoraceae;Thelephora;unculturedectomycorrhizal_fungus
        line = line.strip()
        #print line
        if not line:
            continue

        text   = line.split("\t")
        # print "text = %s" % (text)
        output.write('"","%s","%s"\n' % (text[0], text[1]))
        # print "id = %s, tax = %s" % (id, tax)
        # split_tax = tax.split(';')

    # while input.next():
    #     # print "input.id = %s, input.seq = %s" % (input.id, input.seq)
    #     output.write('"", "%s","%s"\n' % (input.id, input.seq))
    output.close()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Unique sequences in a file file')
    parser.add_argument('input_file', metavar = 'INPUT_file',
                            help = 'Sequences file in file format')
    parser.add_argument('-o', '--output-file', metavar = 'OUTPUT_file', default = None,
                            help = 'file to store unique sequences')

    args = parser.parse_args()
    main(args)
