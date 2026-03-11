# Existing System Analysis Report

## 1. Introduction
- **Objective**: To analyze the current state of text data management within
  Confluence (Atlassian) for the purposes of qualitative and quantitative
analysis.
- **Scope**: Assess existing systems, data extraction capabilities, and
  limitations to inform the development of an enhanced text analysis framework.

## 2. System Overview
- **Current Environment**:
  - Confluence (Atlassian) used for storing documentation, meeting notes, and
    project artifacts.
  - Python and R environments available for data analysis.
- **Data Sources**:
  - Confluence documents and pages, accessible via REST API.
  - Existing textual datasets used in prior analysis efforts.

## 3. Existing Data Flow
- **Data Ingestion**:
  - Current method relies on manual exports or direct API calls.
  - Limited automation for extracting structured content.
- **Data Storage**:
  - Confluence serves as the primary repository, with limited capabilities for
    structured data extraction.
- **Data Analysis**:
  - Basic reporting available within Confluence but lacks advanced NLP
    capabilities.
  - Previous analysis conducted using RStudio IDE and manual data exports.

## 4. Identified Issues & Gaps

### Data Accessibility
- Limited automation for accessing and extracting text data via Confluence API.
- Manual processes prone to errors and time-consuming.

### Analytical Capabilities
- Current tools lack the ability to perform deep text analysis, including
  tokenization, sentiment analysis, and topic modeling.
- No standardized approach for micro, meso, and macro-level text analysis.

### Scalability & Performance
- Existing workflows are not optimized for scaling analysis as data volume
  grows.
- Lack of modular, reusable scripts for analysis.

## 5. Recommendations
- **Automation**: Implement Python scripts to automate data extraction from
  Confluence via REST API.
- **Enhanced Analysis**: Use NLP tools (`spaCy`, `nltk`, etc.) for deeper text
  analysis at various levels.
- **Scalability**: Refactor existing scripts to be modular, enabling reuse and
  scalability.
- **Documentation**: Improve internal documentation for data extraction and
  analysis workflows.

## 6. Assumptions and Constraints
- Full access to the Confluence API with the required permissions.
- Availability of existing computing resources for implementing Python and R
  solutions.
- Stakeholder support for implementing automation and analysis enhancements.
