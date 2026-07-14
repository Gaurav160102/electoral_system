from django.shortcuts import render
from django.views.generic import ListView
from .models import Voter
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.http import HttpResponse
import os
from django.conf import settings
from io import BytesIO

class VoterListView(ListView):
    model = Voter
    template_name = 'voterlist/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 50  # Adjust as needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_male'] = self.model.objects.filter(gender='M').count()
        context['total_female'] = self.model.objects.filter(gender='F').count()
        context['total_voters'] = self.model.objects.count()
        return context

def generate_pdf(request):
    """Generate a PDF voter list similar to the provided image."""
    voters = Voter.objects.all().order_by('name')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # Header
    header = Paragraph("STATE OF SIKKIM<br/>PANCHAYAT ELECTORAL ROLL - 2025", styles['Heading1'])
    story.append(header)
    story.append(Paragraph("GP No. & Name: 11-LINGZYAK", styles['Normal']))
    story.append(Paragraph("Ward No. & Name: 2-SANGTENGI<br/>Polling Station: RANKA SR SEC SCHOOL - NEW BUILDING", styles['Normal']))
    story.append(Paragraph(f"Total Voters: Male {Voter.objects.filter(gender='M').count()} Female {Voter.objects.filter(gender='F').count()} Total {Voter.objects.count()}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Data for table: Serial No., Name (with photo), EPIC No., etc.
    data = [['Sl. No.', 'Name & Photo', 'Father/Husband', 'Gender', 'Age', 'EPIC No.']]

    for i, voter in enumerate(voters, 1):
        # Placeholder for photo (resize to fit)
        photo_path = ""
        if voter.photo:
            photo_path = str(voter.photo.path)
            if os.path.exists(photo_path):
                img = Image(photo_path, width=1*inch, height=1.2*inch)
            else:
                img = Paragraph("No Photo", styles['Normal'])
        else:
            img = Paragraph("No Photo", styles['Normal'])

        row = [
            str(i),
            [img, Paragraph(voter.name, styles['Normal'])],
            Paragraph(voter.father_husband_name, styles['Normal']),
            voter.gender,
            str(voter.age),
            voter.epic_no
        ]
        data.append(row)

    # Create table
    table = Table(data, colWidths=[0.5*inch, 2.5*inch, 2*inch, 0.5*inch, 0.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    story.append(table)

    doc.build(story)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="voter_list.pdf"'
    return response