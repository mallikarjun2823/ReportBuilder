# Report App Model Reference

This file documents what data should be stored in each model field in the `Report` app.

## General conventions

- Primary key fields like `report_num`, `dataset_num`, and similar identifier fields should store stable, human-readable unique codes.
- `status` fields should be used to mark a record as active or inactive without deleting it.
- `created_at` and `updated_at` are system-managed timestamps and should not be entered manually.
- `config` fields should store structured JSON settings for layout, behavior, formatting, or source-specific options.
- Foreign key fields should point to existing parent records and preserve the report hierarchy.

## 1. Report

Represents the top-level report definition.

| Field | What to store |
| --- | --- |
| `report_num` | Unique report identifier code. Use a stable code that can be referenced from datasets, sections, and subreports. |
| `report_name` | Human-friendly report title. This is the main display name shown in the UI or admin. |
| `description` | Optional free-text explanation of the report purpose, business context, or usage notes. |
| `status` | Whether the report is active and available for use. Use `True` for active, `False` for inactive/archived. |
| `created_at` | Auto-generated creation timestamp. |
| `updated_at` | Auto-updated last modified timestamp. |

## 2. ReportDataset

Stores data source definitions used by report elements.

| Field | What to store |
| --- | --- |
| `report` | Parent `Report` record this dataset belongs to. |
| `dataset_num` | Unique dataset identifier code within the system. |
| `dataset_name` | Friendly name for the dataset, such as "Sales Summary" or "Customer List". |
| `source_type` | Type of source used to populate data. Expected values are `PROCEDURE`, `SQL`, or `API`. |
| `procedure_name` | Name of the stored procedure when `source_type` is `PROCEDURE`. Leave empty for other source types. |
| `query` | SQL statement or API query definition when the source is not a stored procedure. Store the exact source logic needed to retrieve data. |
| `created_at` | Auto-generated creation timestamp. |

## 3. ReportSectionLookup

Lookup table for standard section categories.

| Field | What to store |
| --- | --- |
| `section_type_num` | Unique code for the section type. |
| `section_type_name` | Display name for the section type, such as `HEADER`, `BODY`, or `FOOTER`. |
| `status` | Whether this section type is active and available for selection. |
| `created_at` | Auto-generated creation timestamp. |

## 4. ReportSection

Represents a section inside a report.

| Field | What to store |
| --- | --- |
| `report` | Parent `Report` this section belongs to. |
| `section_num` | Unique section identifier code. |
| `section_name` | Human-readable section name. |
| `section_type` | Section category. Current expected values are `HEADER`, `BODY`, or `FOOTER`. |
| `display_order` | Numeric order for rendering sections in sequence. Lower values should appear first. |
| `status` | Whether the section is active and should be rendered or processed. |
| `created_at` | Auto-generated creation timestamp. |

## 5. ReportGroupBoxLookup

Lookup table for group box container types.

| Field | What to store |
| --- | --- |
| `groupbox_type_num` | Unique code for the group box type. |
| `groupbox_type_name` | Display name for the group box type, such as a layout container, subreport container, chart container, or similar grouping concept. |
| `status` | Whether this lookup value is active. |
| `created_at` | Auto-generated creation timestamp. |

## 6. ReportSectionGroupBox

Represents a container inside a section. This is used to group elements or embed a subreport.

| Field | What to store |
| --- | --- |
| `section` | Parent `ReportSection` that contains this group box. |
| `groupbox_num` | Unique group box identifier code. |
| `groupbox_name` | Human-readable name for the container. |
| `groupbox_type` | Reference to `ReportGroupBoxLookup` describing the container type. |
| `subreport` | Optional linked `Report` when this group box should render or reference another report as a subreport. Leave empty if not used. |
| `config` | JSON settings for container behavior, layout, dimensions, styling, conditional logic, or subreport-specific options. |
| `display_order` | Ordering value for group boxes within the section. Lower values appear first. |
| `status` | Whether the group box is active and should be used during rendering. |
| `created_at` | Auto-generated creation timestamp. |

## 7. ReportElementLookup

Lookup table for supported element types.

| Field | What to store |
| --- | --- |
| `element_type_num` | Unique code for the element type. |
| `element_type_name` | Display name for the element type, such as text, label, image, table, chart, or other supported visual/control type. |
| `status` | Whether the element type is active. |
| `created_at` | Auto-generated creation timestamp. |

## 8. ReportSectionGroupBoxElement

Represents the leaf-level content inside a group box.

| Field | What to store |
| --- | --- |
| `groupbox` | Parent `ReportSectionGroupBox` that contains this element. |
| `element_num` | Unique element identifier code. |
| `element_name` | Human-readable element name used for identification and administration. |
| `element_type` | Reference to `ReportElementLookup` describing how the element should render or behave. |
| `dataset` | Optional linked `ReportDataset` when the element needs live data. Leave empty for static content. |
| `field` | Name of the dataset field/column to bind to this element. Store the exact source field name expected by the dataset. |
| `label` | Optional display label shown to users instead of, or alongside, the raw field name. |
| `image_path` | Uploaded image file for image-based elements. Store report-specific assets here. |
| `config` | JSON settings for the element, such as formatting, width, alignment, font, colors, visibility rules, image scaling, or binding behavior. |
| `display_order` | Ordering value for elements within the group box. Lower values appear first. |
| `status` | Whether the element is active and should be rendered. |
| `created_at` | Auto-generated creation timestamp. |

## Suggested data entry rules

- Keep identifier fields consistent and unique across the system.
- Use lookup tables for reusable type definitions instead of hard-coding display values in multiple places.
- Store only source-specific logic in `query` and keep it reusable and maintainable.
- Keep `config` JSON focused on rendering and behavior details so models stay flexible without schema changes.
- Use `status` for soft deactivation instead of deleting records when historical reference matters.
