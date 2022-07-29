/** \file
 \brief Binary to hex converter
 \author Tomasz Ostrowski, ot at epf dot pl
 \date October 2006
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <getopt.h>

/** Flag set by `--verbose'. */
static int verbose_flag;

char fin[255]; 			///< input filename
char fout[255]; 		///< output filename
char strtmp[255]; 		///< temporary string
char separator[255]; 	///< separator for output strings
int bytes_per_string; 	///< how many bytes convert to string? (byte/word/quad/... data)
unsigned int wrap_line;	///< wrap line after about N chars
int write_hex_only = 0;

/** \brief Print some help */
void help(const char *exename)
{
    puts("\nBinary to hex string (C-like) converter");
    printf("\nUsage: %s --i <input_filename> --o <output_filename>\n", exename);
    puts(" i.e. bin2hex --i myfile.dat --o myfile.c");
    puts("Other options:");
    puts(" --s <separator> select separator for output string (i.e. comma or comma+space)");
    puts(" --b <bytes_per_string> read byte (default), word, int (0xAB/0xABCD/0x89ABCDEF)");
    puts(" --w <wrap_line> wrap line after specified number of chars (default: 70)");
    puts(" -x write only hex characters to file (no 0x and comma/space)");
    puts(" multi-bytes values treated as little endian");
    puts("\nauthor: Tomasz Ostrowski, ot at epf dot pl");
    puts("created: 2006.10.23\n");
}


/** \brief Init default options (if not exist in command line) */
void init_options(void)
{
    strcpy(fin,"");
    strcpy(fout,"hex_out.c");
    strcpy(separator, ", ");  	//default separator
	bytes_per_string = 1;		//read bytes (not words or ints) from file
	wrap_line = 70;
	write_hex_only = 0;
}


int
main (argc, argv)
int argc;
char **argv;
{
    int c;
    int i;
    unsigned int chars_in_line=0;	///< number of chars in current line
    int stringlength;	///< length of single converted string
    long lSize;			///< filesize
    unsigned char *buffer;		///< pointer to buffer for input file
    int option_count=0; ///< command-line options counter
    FILE *fileIn, *fileOut; ///< input and output file


    init_options();

    while (1)
    {
        static struct option long_options[] =
            {
                /* Flag-type options */
                {"verbose", no_argument,       &verbose_flag, 1
                },
                /* Non-flag options distinguished by their indices. */
                {"add",     no_argument,       0, 'a'
                },
                {"bytes_per_string",    required_argument, 0, 'b'
                },
                {"in",  required_argument, 0, 'i'
                },
                {"out",  required_argument, 0, 'o'
                },
                {"separator",    required_argument, 0, 's'
                },
                {"wrap_line",    required_argument, 0, 'w'
                },
                {"hex_only", no_argument, 0, 'x'
                },
                {0, 0, 0, 0
                }
            };
        /* getopt_long stores the option index here. */
        int option_index = 0;

        c = getopt_long (argc, argv, "abc:d:f:x",
                         long_options, &option_index);

        /* Detect the end of the options. */
        if (c == -1)
        {
            if(option_count<1)
                help(argv[0]); // print help if no arguments
            break;
        }
        option_count++;

        switch (c)
        {
            case 0:
            /* If this option set a flag, do nothing else now. */
            if (long_options[option_index].flag != 0)
                break;
            printf ("option %s", long_options[option_index].name);
            if (optarg)
                printf (" with arg %s", optarg);
            printf ("\n");
            break;

            case 'a':
            puts ("option -a\n");
            break;

            case 'b':
            printf ("option -b with value `%s'\n", optarg);
            bytes_per_string = atoi(optarg);
            if(bytes_per_string<1 || bytes_per_string>10)
            {
                puts("Required 0<bytes_per_string<=10");
                exit(1);
            }
            break;

            case 'c':
            printf ("option -c with value `%s'\n", optarg);
            break;

            case 'i':
            printf ("option -i with value `%s'\n", optarg);
            strcpy(fin, optarg);
            break;

            case 'o':
            printf ("option -o with value `%s'\n", optarg);
            strcpy(fout, optarg);
            break;

            case 's':
            printf ("option -s with value `%s'\n", optarg);
            strcpy(separator, optarg);
            break;

            case 'x':
            printf ("option -x\n");
            write_hex_only = 1;
            break;

            case 'w':
            printf ("option -w with value `%s'\n", optarg);
            wrap_line = atoi(optarg);
            if (wrap_line < 1)
                wrap_line = 70;
            break;

            case '?':
            /* getopt_long already printed an error message. */
            help(argv[0]);
            break;

            default:
            abort ();
        }
    }


    if (verbose_flag)
        puts ("verbose flag is set");

    /* Print any remaining command line arguments (not options). */
    if (optind < argc)
    {
        printf ("non-option ARGV-elements: ");
        while (optind < argc)
            printf ("%s ", argv[optind++]);
        putchar ('\n');
    }

    // start processing
    fileIn = fopen(fin, "rb"); // open input file (binary)
    if (fileIn==NULL)
    {
        puts("Error opening input file");
        exit (1);
    }

    // open output file
    fileOut = fopen(fout, "wt");
    if (fileOut==NULL)
    {
        puts("Error opening output file for write");
        exit (1);
    }


    // obtain file size.
    fseek (fileIn , 0 , SEEK_END);
    lSize = ftell (fileIn);
    rewind (fileIn);
	printf("Filesize: %d bytes.\n", lSize);
	if(lSize%bytes_per_string)
	{
		puts("Error: length of file isn't multiplication of bytes_per_string value.");
		puts("Please modify input file or select other formatting");
		exit (3);
	}

    // allocate memory to contain the whole file.
    buffer = (unsigned char*) malloc (lSize);
    if (buffer == NULL)
    {
    	puts("malloc for input file buffer failed (not enough memory?)");
        exit (2);
    }

    // copy the file into the buffer.
    fread (buffer,1,lSize,fileIn);

    if (write_hex_only)
    {
        switch(bytes_per_string)
        {
            case 1:
                stringlength = 2;	//length of single converted string
                for(i=0; i<lSize-1; i++)
                {
                    fprintf(fileOut,"%02X",buffer[i]);
                    chars_in_line += stringlength;
                    if(chars_in_line >= wrap_line)
                    {
                        fprintf(fileOut, "\n");
                        chars_in_line = 0;
                    }
                }
                fprintf(fileOut,"%02X",buffer[i]);	//no separator after last string
                break;
            case 2:
                stringlength = 4;
                for(i=0; i<lSize-2; i+=2)
                {
                    fprintf(fileOut,"%04X",(unsigned int)(buffer[i]*256 + buffer[i+1]));
                    chars_in_line += stringlength;
                    if(chars_in_line >= wrap_line)
                    {
                        fprintf(fileOut, "\n");
                        chars_in_line = 0;
                    }
                }
                fprintf(fileOut,"%04X",(unsigned int)(buffer[i]*256 +
                    buffer[i+1]));
                break;
            case 4:
                stringlength = 8;
                for(i=0; i<lSize-4; i+=4)
                {
                    fprintf(fileOut,"%08X",(unsigned int)(buffer[i]*16777216 +
                        buffer[i+1]*65536 + buffer[i+2]*256 +
                        buffer[i+3]));
                    chars_in_line += stringlength;
                    if(chars_in_line >= wrap_line)
                    {
                        fprintf(fileOut, "\n");
                        chars_in_line = 0;
                    }
                }
                fprintf(fileOut,"%08X",(unsigned int)(buffer[i]*16777216 +
                    buffer[i+1]*65536 + buffer[i+2]*256 +
                    buffer[i+3]));
                break;
            default:
            puts("Sorry, processing for this bytes_per_string value not implemented yet");
        }
    }
    else
    {
        switch(bytes_per_string)
        {
            case 1:
                stringlength = 4 + strlen(separator);	//length of single converted string
                for(i=0; i<lSize-1; i++)
                {
                    fprintf(fileOut,"0x%02X%s",buffer[i],separator);
                    chars_in_line += stringlength;
                    if(chars_in_line >= wrap_line)
                    {
                        fprintf(fileOut, "\n");
                        chars_in_line = 0;
                    }
                }
                fprintf(fileOut,"0x%02X",buffer[i]);	//no separator after last string
                break;
            case 2:
                stringlength = 6 + strlen(separator);
                for(i=0; i<lSize-2; i+=2)
                {
                    fprintf(fileOut,"0x%04X%s",(unsigned int)(buffer[i]*256 +
                        buffer[i+1]), separator);
                    chars_in_line += stringlength;
                    if(chars_in_line >= wrap_line)
                    {
                        fprintf(fileOut, "\n");
                        chars_in_line = 0;
                    }
                }
                fprintf(fileOut,"0x%04X",(unsigned int)(buffer[i]*256 +
                    buffer[i+1]));
                break;
            case 4:
                stringlength = 10 + strlen(separator);
                for(i=0; i<lSize-4; i+=4)
                {
                    fprintf(fileOut,"0x%08X%s",(unsigned int)(buffer[i]*16777216 +
                        buffer[i+1]*65536 + buffer[i+2]*256 +
                        buffer[i+3]), separator);
                    chars_in_line += stringlength;
                    if(chars_in_line >= wrap_line)
                    {
                        fprintf(fileOut, "\n");
                        chars_in_line = 0;
                    }
                }
                fprintf(fileOut,"0x%08X",(unsigned int)(buffer[i]*16777216 +
                    buffer[i+1]*65536 + buffer[i+2]*256 +
                    buffer[i+3]));
                break;
            default:
            puts("Sorry, processing for this bytes_per_string value not implemented yet");
        }
    }
	printf("%d strings printed to file\n", i/bytes_per_string+1);

	if(fileIn) fclose (fileIn);
	if(fileOut) fclose (fileOut);
	if(buffer) free (buffer);
    exit (0);
}
