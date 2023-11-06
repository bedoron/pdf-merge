Example run:

Join all files in folder `C:\Users\dawg\Documents\Secret PDFs` to `C:\Users\dawg\Documents\Secret PDFs\out.pdf` and use `thepassword` to access the pds in the folder
```commandline
python.exe .\main.py --out out.pdf --path "C:\Users\dawg\Documents\Secret PDFs" --password "thepassword"
```

To use page 1 from each file:
```commandline
python.exe .\main.py --out out.pdf --path "C:\Users\dawg\Documents\Secret PDFs" --password "thepassword" --pages 1
```

To decode files individually
```commandline
python.exe .\main.py --out out.pdf --path "C:\Users\dawg\Documents\Secret PDFs" --password "thepassword" --decode
```