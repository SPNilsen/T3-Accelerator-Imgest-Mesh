# Initial Data Collection Report

![Data Understanding](../img/data-understanding.webp 'data-understanding')


## Data Sources

Approximately 50,000 images, captured in both visible and UV light, are
available via an S3 bucket. Of these, 10,000 to 20,000 images will be annotated
using CVAT, with annotation files shared as JSON downloads through Teams and
distributed in the COCO format.


```
% head ali-tam17-recursive.dmp
2024-10-10 12:42:06          0 A/
2024-10-15 13:13:21    8390144 A/TAM17-A-0422_162943_315.bmp
2024-10-15 13:13:30    8390144 A/TAM17-A-0422_163001_105.bmp
2024-10-15 13:13:38    8390144 A/TAM17-A-0422_175148_912.bmp
2024-10-15 13:13:47    8390144 A/TAM17-A-0422_175155_062.bmp
2024-10-15 13:13:55    8390144 A/TAM17-A-0422_175156_802.bmp
2024-10-15 13:14:04    8390144 A/TAM17-A-0422_175202_152.bmp
2024-10-15 13:14:12    8390144 A/TAM17-A-0422_175210_342.bmp
2024-10-15 13:14:21    8390144 A/TAM17-A-0422_175212_082.bmp
2024-10-15 13:14:29    8390144 A/TAM17-A-0422_175231_262.bmp
...
```

- **Image Files**:

    - Dual-modality images: visible light (top half) and UV light (bottom half) ([Annotation Guide, Page 3](./Annotation-Guide-RMD-v3-20241212.pdf#page=3)).

    - Approximately 50,000 images are targeted for the annotation library ([Annotation Guide, Page 4](./Annotation-Guide-RMD-v3-20241212.pdf#page=4)).

![Image Example](../img/image-snap.webp 'image-snap')

- **Metadata**:

    - Attributes such as "bubble cluster," "edge-tear length," and "arc length percentages" are integral to the defect identification process ([Annotation Guide, Page 5](./Annotation-Guide-RMD-v3-20241212.pdf#page=5)).


**Annotation Sample**

??? abstract "COCO format JSON annotations sample"
    ``` title="job_1411526_annotations_2024_12_11_02_48_47_coco 1.0.json" linenums="1"
    --8<-- "docs/annotations/sample.json"
    ```


---

## Data Characteristics

- **Image Composition**:

    - Visible light images emphasize lens surface and edge defects ([Annotation Guide, Page 6](./Annotation-Guide-RMD-v3-20241212.pdf#page=6)).

    - UV light images assist in hole verification by highlighting bright spots against a dark background ([Annotation Guide, Page 7](./Annotation-Guide-RMD-v3-20241212.pdf#page=7)).

- **Defects to Be Annotated**:

    - Defects include center debris, edge chips, lens out-of-round, and others ([Annotation Guide, Page 8](./Annotation-Guide-RMD-v3-20241212.pdf#page=8)).

    - Some defects require additional attributes, such as "low contrast" or "edge contact" ([Annotation Guide, Page 9](./Annotation-Guide-RMD-v3-20241212.pdf#page=9)).

---

## Data Exploration

- **Initial Analysis**:

    - Distribution of defect types and their frequency in the dataset.

    - Identification of edge cases, such as overlapping bubbles and debris ([Annotation Guide, Page 10](./Annotation-Guide-RMD-v3-20241212.pdf#page=10)).

- **Challenges Identified**:

    - Distinguishing package marks (PPMs) from actual lens defects ([Annotation Guide, Page 11](./Annotation-Guide-RMD-v3-20241212.pdf#page=11)).

    - Handling low-contrast defects and ensuring annotation consistency ([Annotation Guide, Page 12](./Annotation-Guide-RMD-v3-20241212.pdf#page=12)).

---

## Challenges and Considerations

- **Consistency in Annotation**:

    - Variability in annotators' interpretations can lead to inconsistent labeling ([Annotation Guide, Page 13](./Annotation-Guide-RMD-v3-20241212.pdf#page=13)).

    - Certain defects, like subtle bubbles or low-contrast debris, require extra attention during the annotation process.

- **Data Quality**:

    - Ensuring that images are properly annotated for defects while minimizing false positives.

    - Balancing the need for speed with accuracy in annotation efforts ([Annotation Guide, Page 14](./Annotation-Guide-RMD-v3-20241212.pdf#page=14)).

---

## Missing Information

- Specific data exploration insights (e.g., preliminary statistical analysis of defect types and distributions) are not yet available.

- Full details on the completeness and consistency of metadata annotations across batches.

