### Business Objectives

The primary objectives of Project ARMOR are to:

- **Enhance Defect Detection**: Evaluate and develop algorithms capable of
  identifying both inspectable and non-inspectable defects with high accuracy.
- **Streamline Quality Assurance**: Design solutions that align with production
  cycle time requirements, maintaining or improving throughput.
- **Transferable Learnings**: Ensure findings are applicable to future imaging
  solutions, enhancing adaptability across evolving manufacturing technologies.
- **Improve Specific Defect Detection**: Focus on low-contrast and challenging
  defects, such as:
    - Lens Presentation Errors (Binary Classifier for Pass/Fail)
        - Lens Out-Of-Focus
        - Lens Out-Of-Round
        - Bubble Scatter
        - Lens Folded
        - Missing Lens
        - Multiple Lenses
        - Lens Inverted
        - Lens “123” Mark Obstructed
        - Ripple Obstruction
        - Major Bubble Obstruction
        - Edge Obstruction
        - Edge Off Image

    - Lens Defects (Specific Defect Models)
        - Center Defects:
        - Center Debris
        - Center Holes
        - Center Surface Tears
        - Edge Defects:
        - Edge Chips
        - Edge Not Closed
        - Edge Tears
        - Edge Exterior Excess

Each of these defects will require dedicated models or enhancements to existing
models to ensure accurate detection, classification, and adherence to predefined
quality standards. This comprehensive defect taxonomy serves as the foundation
for developing robust algorithmic solutions tailored to specific defect types.

**Out of Scope**

The project scope is focused exclusively on evaluating and enhancing algorithms
within the constraints of the existing ALI imaging system. Out-of-scope items
include:

- **New Image Formation Solutions**: No changes to the existing imaging setup
  will be considered.
- **Manufacturing Integration**: Interface considerations, operator tools, and
  production deployment will be addressed in future phases.
- **Support Infrastructure**: Development of hardware or additional support
  systems is not part of this evaluation.


**Manufacturing Locations**

Project ARMOR will evaluate algorithms at Johnson & Johnson MedTech facilities in:

- **Jacksonville, Florida**
- **Limerick, Ireland**

**References**

This project will adhere to internal standards and procedures, including:

- **QP-0075**: Visual Attribute Inspection Procedure.
- **VWA-0974**: Lens Visual Inspection Work Aid.
- **SGOP-0023**: Design, Procurement, and Maintenance of Equipment and Process
  Equipment.
