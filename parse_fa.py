import sys
sys.path.append("/Users/ashipunova/bin/illumina-utils")
sys.path.append("/Users/ashipunova/bin/illumina-utils/illumina-utils/scripts")
import fastalib as u

def main(args):
    try:
        input = u.SequenceSource(args.input_fasta)
    except IOError:
        print 'Error: File does not exist, or you do not have the right permissions to read it: "%s"'\
                    % args.input_fasta
        sys.exit(-1)

    if args.output_fasta:
        output_file_path = args.output_fasta
    else:
        output_file_path = args.input_fasta + '.flat'

    try:
        output = open(output_file_path, 'w')        
    except IOError:
        print 'Error: You have no permission to write destination: "%s"'\
                    % output_file_path
        sys.exit(-1)

    while input.next():
        # print "input.id = %s, input.seq = %s" % (input.id, input.seq)
        output.write('"", "%s","%s"\n' % (input.id, input.seq))
    output.close()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Unique sequences in a FASTA file')
    parser.add_argument('input_fasta', metavar = 'INPUT_FASTA',
                            help = 'Sequences file in FASTA format')
    parser.add_argument('-o', '--output-fasta', metavar = 'OUTPUT_FASTA', default = None,
                            help = 'FASTA file to store unique sequences')

    args = parser.parse_args()
    main(args)
