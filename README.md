# pascal-voc-read-write
This repository help in reading and writing the annotations files written in pascal voc format.

## Prerequisites

Following modules are needed:

| Modules              | Installation command                     |
| -------------------- | ---------------------------------------- |
| pandas         | pip install pandas          |
| numpy           | pip install numpy           |
| pascal_voc_writer | pip install pascal-voc-writer |

## Procedure

```bash
# First of all make count csv
python annotation_count.py \
path/to/xml_dir \
path/to/csv_file.csv \
--arrange

# Now modified the labels by placing label in Modified_Label column of csv.
# NOTE: If uou want to remove label than place it empty.
python annotation_count.py \
path/to/xml_dir \
path/to/output_dir \
path/to/csv_file.csv

# If you need help use --help
```



## Authors

* **Muhammad Tahir Rafique**
