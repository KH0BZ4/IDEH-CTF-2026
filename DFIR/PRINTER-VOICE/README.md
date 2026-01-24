# Printer's Voice - DFIR

- CTF: IDEH CTF 2026
- Category: DFIR
- Author: K4G3SEC
- Solver: Akari
- Flag: `IDEH{Ev1denc3_L1ng3r5_1n_Sp00l_B1ts}`

---

## Challenge
> “A disgruntled employee managed to exfiltrate confidential data moments before being fired. He knew his USB drives were monitored and his email traffic was heavily filtered. Our investigation suggests he printed the classified document to smuggle it out physically — but he insists he never printed anything.
>
> During the forensic analysis of his workstation, we recovered a strange file hidden inside one of the system’s temporary spooler directories.
>
> Prove he's lying.
> file -> `evidence.SPL`”

---

## Overview
In a Digital Forensics and Incident Response (DFIR) context, the Windows Print Spooler directory (`C:\Windows\System32\spool\PRINTERS`) is a goldmine for evidence of data exfiltration. The `.SPL` file is a spool file that contains the actual content of the print job. Modern Windows spool files often utilize the XPS format, which is a package of XMLs and resource files (like images) compressed into a ZIP structure.

---

## Root Cause if found
The employee attempted to use the physical print queue to bypass digital monitoring systems. By printing to a spooler, a temporary file was created that cached the document contents. Even if the print job was deleted from the queue or never reached a physical printer, the `.SPL` file remained in the system's temporary directory, preserving the evidence in an XPS/ZIP format.

---

## Exploitation Steps

### 1. Identify and Extract the Spool File
The `.SPL` file is identified as zip file . To begin the investigation, we need to unzip it :) .

```bash
# Rename the SPL file to a ZIP for extraction
unzip evidence.SPL
Archive:  evidence.SPL
  inflating: Metadata/Job_PT.xml
  inflating: Metadata/MXDC_Empty_PT.xml
  inflating: Documents/1/Metadata/Page1_PT.xml
 extracting: Documents/1/Resources/Images/1.JPG
  inflating: Documents/1/Pages/1.fpage
  inflating: Documents/1/Pages/_rels/1.fpage.rels
  inflating: Documents/1/Resources/Fonts/70DBEC0A-92C8-4539-86A0-F13CF9347DA6.odttf
  inflating: Documents/1/FixedDocument.fdoc
  inflating: Documents/1/_rels/FixedDocument.fdoc.rels
  inflating: FixedDocumentSequence.fdseq
  inflating: _rels/FixedDocumentSequence.fdseq.rels
  inflating: _rels/.rels
  inflating: [Content_Types].xml
```

### 2. Check XML Files for Metadata
Once extracted, the internal structure of the print job is visible. Navigating through the XML files allows an investigator to see the print settings, page layouts, and metadata associated with the print job.

```bash
# Navigate to the Documents directory to inspect the layout
cd extracted_spool/Documents/1/
# Check XML files for page content and structure
cat Pages/1.fpage
```

### 3. Extract Embedded Evidence (JPG Files)
The core evidence is often stored as image resources within the spool package. To find the exfiltrated data that the employee claimed did not exist, we search the entire extracted directory for any embedded image files.

```bash
# Extract all JPG files from the unzipped XPS structure
find . -name "*.JPG" -o -name "*.jpg"
```
 - or we just navigate in the folder and find the image that contains the flag :)
### 4. Conclusion
By locating the JPG files within the `Resources` folder of the unzipped spool file, we can reconstruct the document the employee attempted to print. Finding these images proves the exfiltration attempt and provides the flag.

   <img src="1.JPG" width="500" alt="Evidence">
---