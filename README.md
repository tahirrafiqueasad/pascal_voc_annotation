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

1. First of all make count csv

   ```bash
   python annotation_count.py -i x -o c --arrange
   ```

   where:

   | Variables | Description                                      | Example              |
   | --------- | ------------------------------------------------ | -------------------- |
   | x         | Path to directory containing xml files.          | path/to/xml_dir      |
   | c         | Path to csv file.                                | path/to/csv_file.csv |
   | arrange   | Arrange the labels according to ascending order. |                      |

2. Now modified the labels by placing label in Modified_Label column of csv.

   NOTE: If you want to remove label than place it empty.

   In below example Cat  label will remain the same, Dog label will changed white_dog and Horse label will be removed. 

   | Label | Count | Modified_Label |
   | ----- | ----- | -------------- |
   | Cat   | 245   | Cat            |
   | Dog   | 302   | white_dog      |
   | Horse | 254   |                |

3. Run the following command to make changes in xml files.

   ```bash
   python modified_labels.py -i x -f c -o y 
   ```

   Where:

   | Variables | Description                             | Example              |
   | --------- | --------------------------------------- | -------------------- |
   | x         | Path to directory containing xml files. | path/to/xml_dir      |
   | c         | Path to csv file.                       | path/to/csv_file.csv |
   | y         | Path to output directory.               | path/to/output_dir   |

## Release:

| Tag    | Date        | Description |
| ------ | ----------- | ----------- |
| v0.0.1 | 27-Aug-2021 | Test Passed |

## Authors

* **Muhammad Tahir Rafique**
