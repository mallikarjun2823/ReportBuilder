from django.db import models
import os
from django.conf import settings


# -------------------------------
# File Upload Path
# -------------------------------
def report_image_upload_path(instance, filename):
    report_id = instance.groupbox_num.section_num.report_num.report_num
    path = os.path.join(settings.MEDIA_ROOT, report_id)

    if not os.path.exists(path):
        os.makedirs(path)

    return os.path.join(report_id, filename)


# -------------------------------
# REPORT (ROOT)
# -------------------------------
class Report(models.Model):
    report_num = models.CharField(max_length=20, primary_key=True)
    report_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report_name


# -------------------------------
# DATASETS
# -------------------------------
class ReportDataset(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='datasets')

    dataset_num = models.CharField(max_length=20, primary_key=True)
    dataset_name = models.CharField(max_length=100)

    source_type = models.CharField(max_length=20, default='PROCEDURE')  # PROCEDURE / SQL / API
    procedure_name = models.CharField(max_length=100, blank=True, null=True)
    query = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dataset_name


# -------------------------------
# SECTION LOOKUP
# -------------------------------
class ReportSectionLookup(models.Model):
    section_type_num = models.CharField(max_length=20, primary_key=True)
    section_type_name = models.CharField(max_length=100)

    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


# -------------------------------
# SECTIONS
# -------------------------------
class ReportSection(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='sections')

    section_num = models.CharField(max_length=20, primary_key=True)
    section_name = models.CharField(max_length=100)

    section_type = models.CharField(max_length=20, default='BODY')  # HEADER, BODY, FOOTER

    display_order = models.IntegerField(default=999)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.section_name


# -------------------------------
# GROUPBOX LOOKUP
# -------------------------------
class ReportGroupBoxLookup(models.Model):
    groupbox_type_num = models.CharField(max_length=20, primary_key=True)
    groupbox_type_name = models.CharField(max_length=100)

    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


# -------------------------------
# GROUPBOX (IMPORTANT FIX HERE)
# -------------------------------
class ReportSectionGroupBox(models.Model):
    section = models.ForeignKey(ReportSection, on_delete=models.CASCADE, related_name='groupboxes')

    groupbox_num = models.CharField(max_length=20, primary_key=True)
    groupbox_name = models.CharField(max_length=100)

    groupbox_type = models.ForeignKey(ReportGroupBoxLookup, on_delete=models.CASCADE)

    # For SUBREPORT
    subreport = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True, null=True)

    config = models.JSONField(default=dict, blank=True)

    display_order = models.IntegerField(default=999)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.groupbox_name


# -------------------------------
# ELEMENT LOOKUP
# -------------------------------
class ReportElementLookup(models.Model):
    element_type_num = models.CharField(max_length=20, primary_key=True)
    element_type_name = models.CharField(max_length=100)

    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


# -------------------------------
# ELEMENT (LEAF NODE - CLEANED)
# -------------------------------
class ReportSectionGroupBoxElement(models.Model):
    groupbox = models.ForeignKey(
        ReportSectionGroupBox,
        on_delete=models.CASCADE,
        related_name='elements'
    )

    element_num = models.CharField(max_length=20, primary_key=True)
    element_name = models.CharField(max_length=100)

    element_type = models.ForeignKey(ReportElementLookup, on_delete=models.CASCADE)

    # Optional dataset binding (not always needed now)
    dataset = models.ForeignKey(ReportDataset, on_delete=models.CASCADE, blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True)

    label = models.CharField(max_length=100, blank=True, null=True)

    # Image support
    image_path = models.ImageField(upload_to=report_image_upload_path, blank=True, null=True)

    config = models.JSONField(default=dict, blank=True)

    display_order = models.IntegerField(default=999)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.element_name