import argparse
from os import listdir
from os.path import isfile, join

from PyPDF2 import PdfMerger, PdfReader, PdfWriter


def reset_eof_of_pdf_return_stream(pdf_stream_in: list):
    # find the line position of the EOF
    for i, x in enumerate(pdf_stream_in[::-1]):
        if b'%%EOF' in x:
            actual_line = len(pdf_stream_in) - i
            print(f'EOF found at line position {-i} = actual {actual_line}, with value {x}')
            break

    # return the list up to that point
    return pdf_stream_in[:actual_line]


def do_args():
    parser = argparse.ArgumentParser(prog='pdf merger and optional decoder')
    parser.add_argument('--path', help='folder path you to operate on')
    parser.add_argument('--out', help='output file for merging', default=None)
    parser.add_argument('--pages', help='which page to choose, omit for all', default=None, required=False, nargs='+', type=int)
    parser.add_argument('--password', help='PDFs password', default=None, required=False)
    parser.add_argument('--decode', help='create decoded file', action='store_true', required=False)

    return parser.parse_args()


def main():
    args = do_args()
    path = args.path
    result_file = args.out
    password = args.password
    create_decoded = args.decode
    pdfs = [f for f in listdir(path) if isfile(join(path, f)) and '.pdf' in f]

    # path_dir = Path.cwd()
    # pdfs = sorted([str(f.expanduser().absolute()) for f in path_dir.glob(sys.argv[2])])
    pages = args.pages
    print("Pages: ", pages)
    print(f"merging to {result_file} the following files: {pdfs}")
    merger = PdfMerger()
    for i, pdf in enumerate(pdfs):
        print(f"appending {pdfs[i]}")
        with open(path + '\\' + pdf, 'rb') as input_file:
            reader = PdfReader(input_file)

            if password:
                reader.decrypt(password)

            if create_decoded:
                with open(path + '\\' + 'DECODED_' + pdf, 'wb') as output_file:
                    writer = PdfWriter()
                    for z in range(len(reader.pages)):
                        writer.add_page(reader.pages[z])

                    writer.write(output_file)

            try:
                merger.append(reader, pages=pages)
            except Exception as e:
                print("trying another method...")
                # Try to truncate data after %%EOF
                # opens the file for reading
                with open(path + '\\' + pdf, 'rb') as p:
                    txt = (p.readlines())

                # get the new list terminating correctly
                txtx = reset_eof_of_pdf_return_stream(txt)

                # write to new pdf
                with open(path + '\\' + pdf, 'wb') as f:
                    f.writelines(txtx)
                try:
                    merger.append(path + '\\' + pdf, pages=(pages - 1, pages) if pages else None)
                except Exception as e:
                    print(f"failed handling {pdfs[i]}: {e}")

    merger.write(path + '\\' + result_file)
    merger.close()


if __name__ == "__main__":
    main()
