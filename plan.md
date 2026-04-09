
#  Structured Report Generation Engine (Django Backend)

---

##  Overview

This project implements a **backend-driven report generation engine** using Django.  
It follows a **strict hierarchical architecture** to ensure clarity, maintainability, and predictable rendering.

Unlike flexible reporting tools, this system enforces a controlled layout:

> **Report → Datasets, Sections → GroupBoxes → Elements**

This design eliminates ambiguity and ensures that reports are built, stored, and rendered in a **deterministic and scalable manner**.

---

#  Objectives

- Build a **robust and scalable backend** for report generation
- Enforce a **fixed hierarchical structure**
- Support **multiple datasets per report**
- Enable **data-bound elements**
- Provide **render-ready APIs**
- Maintain strict separation between:
  - Structure
  - Data
  - Presentation

---

##  System Architecture

###  Hierarchy

```

Report
├── Datasets
└── Sections
└── GroupBoxes
└── Elements (Leaf Nodes)

````

---

##  Domain Model

---

### 1. Report (Root Entity)

Represents the main container for a report.

**Fields:**
- `id`
- `name`
- `description`
- `status` (draft / published)
- `created_at`
- `updated_at`

---

### 2. ReportDataset

Defines data sources associated with a report.

**Fields:**
- `id`
- `report_id` (FK)
- `dataset_name`
- `source_type` (SQL / Stored Procedure / API)
- `query_or_procedure`
- `created_at`

---

### 3. ReportSection

Represents logical divisions of a report.

**Fields:**
- `id`
- `report_id` (FK)
- `title`
- `display_order`

---

### 4. ReportSectionGroupBox

Defines layout containers inside sections.

**Fields:**
- `id`
- `section_id` (FK)
- `groupbox_type` (ENUM)
- `title`
- `display_order`
- `layout_config` (JSON)

---

### 5. ReportSectionGroupBoxElement (Leaf Node)

Represents the smallest renderable unit.

**Responsibilities:**
- Data binding
- Styling
- Rendering behavior

**Fields:**
- `id`
- `groupbox_id` (FK)
- `element_type` (TEXT / FIELD / IMAGE / etc.)
- `display_order`
- `data_binding` (JSON)
- `style_config` (JSON)
- `meta_config` (JSON)

---

##  Supported Types

### GroupBox Types
- `FREE_FORM`
- `GRID`
- `BARCODE`
- `SUBREPORT`
- `IMAGE_CONTAINER`

### Element Types
- `TEXT`
- `FIELD`
- `IMAGE`
- `BARCODE`

---

##  Data Binding

Each element binds to dataset fields using structured JSON.

### Example

```json
{
  "dataset": "orders",
  "field": "total_amount"
}
````

---

##  Styling Configuration

Elements support styling via JSON.

### Example

```json
{
  "font_size": 14,
  "color": "#333333",
  "alignment": "left"
}
```

---

##  Processing Pipeline

---

### 1. Structure Retrieval

* Fetch report hierarchy:

  * Sections
  * GroupBoxes
  * Elements

---

### 2. Dataset Execution

* Execute queries or procedures defined in datasets

---

### 3. Data Binding

* Map dataset fields to elements

---

### 4. Transformation

* Apply formatting and styling

---

### 5. Response Generation

* Return structured JSON for frontend rendering

---

## 🔌 API Design

---

### Report APIs

* `POST /reports/` → Create report
* `GET /reports/` → List reports
* `PATCH /reports/{id}/` → Update report

---

### Dataset APIs

* `POST /reports/{id}/datasets/`
* `PATCH /datasets/{id}/`

---

### Section APIs

* `POST /reports/{id}/sections/`
* `PATCH /sections/{id}/`

---

### GroupBox APIs

* `POST /sections/{id}/groupboxes/`
* `PATCH /groupboxes/{id}/`

---

### Element APIs

* `POST /groupboxes/{id}/elements/`
* `PATCH /elements/{id}/`
* `DELETE /elements/{id}/`

---

### Render API

* `GET /reports/{id}/render/`

---

## 📤 Sample Render Response

```json
{
  "report": "Sales Report",
  "sections": [
    {
      "title": "Customer Info",
      "groupboxes": [
        {
          "type": "FREE_FORM",
          "elements": [
            {
              "type": "TEXT",
              "value": "John Doe",
              "style": {}
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 🧠 Key Design Principles

---

### 1. Strict Hierarchical Structure

* Ensures predictable layout
* Simplifies backend logic
* Prevents UI chaos

---

### 2. Leaf-Level Data Binding

* Only elements interact with datasets
* Clear separation of concerns

---

### 3. Controlled Types

* Prevents uncontrolled complexity
* Ensures consistency in rendering

---

### 4. JSON-Based Flexibility

Used for:

* Styling
* Layout
* Metadata

Avoids frequent schema changes.

---

## 🔐 Validation Strategy

* Validate dataset existence
* Validate field mappings
* Enforce type constraints
* Ensure proper ordering

---

## 🧪 Testing Strategy

* Unit tests for:

  * Dataset execution
  * Data binding
* API testing via Postman
* Edge case handling:

  * Missing fields
  * Invalid configurations

---

## 🚀 Future Enhancements

* Expression engine (computed fields)
* Pagination support
* Export (PDF, Excel)
* Role-based access control
* Versioning system
* Performance optimization (caching, query tuning)

---

## ⚠️ Constraints

* Backend-first development
* Fixed hierarchy (no arbitrary nesting)
* No frontend dependency during core development
* Controlled extensibility

---

## 📌 Development Roadmap (Phase-wise)

---

### 🟢 Level 1 — Domain Modeling

* Define all models
* Create migrations
* Lock schema

---

### 🟡 Level 2 — CRUD APIs

* Report, Dataset, Section, GroupBox, Element APIs
* Test via Postman

---

### 🔵 Level 3 — Structure Retrieval

* Fetch full hierarchy
* Ensure correct ordering

---

### 🟣 Level 4 — Dataset Engine

* Execute queries/procedures
* Return structured data

---

### 🔴 Level 5 — Data Binding

* Map dataset fields to elements

---

### 🟠 Level 6 — Render API

* Combine structure + data
* Return final JSON

---

### ⚫ Level 7 — Validation & Optimization

* Add validations
* Improve performance

---
