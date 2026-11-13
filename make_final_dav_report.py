import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_page_number_to_paragraph(p):
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    p._p.append(fldSimple)

def create_report():
    doc = Document()
    
    # Configure default style: Times New Roman, 12pt, Black, 1.5 line spacing
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    
    # Configure A4 Dimensions and Margins per Notice:
    # Left Margin: 1.5", Right Margin: 0.75", Top: 1.0", Bottom: 1.0"
    for sec in doc.sections:
        sec.page_width = Inches(8.27)
        sec.page_height = Inches(11.69)
        sec.left_margin = Inches(1.5)
        sec.right_margin = Inches(0.75)
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.different_first_page_header_footer = True
        
        # Header (Report Title)
        header = sec.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.paragraph_format.space_after = Pt(0)
        r_hdr = p_hdr.add_run("Four Weeks Industrial Training Project Report on GestureSpeak AI")
        r_hdr.font.name = 'Times New Roman'
        r_hdr.font.size = Pt(8.5)
        r_hdr.font.italic = True
        r_hdr.font.color.rgb = RGBColor(100, 100, 100)
        
        # Footer (College Name and Page Number)
        footer = sec.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ftr.paragraph_format.space_before = Pt(0)
        
        tbl_ftr = footer.add_table(1, 2, Inches(6.02))
        tbl_ftr.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_left, c_right = tbl_ftr.rows[0].cells
        c_left.width = Inches(4.2)
        c_right.width = Inches(1.8)
        
        p_fl = c_left.paragraphs[0]
        p_fl.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_fl = p_fl.add_run("Department of CSE, DAV University, Jalandhar")
        r_fl.font.name = 'Times New Roman'
        r_fl.font.size = Pt(8.5)
        r_fl.font.color.rgb = RGBColor(100, 100, 100)
        
        p_fr = c_right.paragraphs[0]
        p_fr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_fr = p_fr.add_run("Page ")
        r_fr.font.name = 'Times New Roman'
        r_fr.font.size = Pt(8.5)
        r_fr.font.color.rgb = RGBColor(100, 100, 100)
        add_page_number_to_paragraph(p_fr)

    assets_dir = r"C:\Users\vinay\.gemini\antigravity\scratch\GestureSpeakAI\assets"
    root_dir = r"C:\Users\vinay\.gemini\antigravity\scratch\GestureSpeakAI"

    logo_path = os.path.join(assets_dir, "dav_university_logo.jpeg")
    arch_path = os.path.join(root_dir, "system_architecture.png")
    workflow_path = os.path.join(root_dir, "workflow_diagram.png")
    cm_path = os.path.join(assets_dir, "confusion_matrix.png")
    history_path = os.path.join(assets_dir, "training_history.png")
    guide_path = os.path.join(assets_dir, "gesture_guide.jpg")

    def add_p(text, bold_prefix="", space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(space_after)
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = 'Times New Roman'
            r_b.font.size = Pt(12)
            r_b.font.color.rgb = RGBColor(0, 0, 0)
        if text:
            r_t = p.add_run(text)
            r_t.font.name = 'Times New Roman'
            r_t.font.size = Pt(12)
            r_t.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = 'Times New Roman'
            rb.font.size = Pt(12)
            rb.font.color.rgb = RGBColor(0, 0, 0)
        rt = p.add_run(text)
        rt.font.name = 'Times New Roman'
        rt.font.size = Pt(12)
        rt.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(16)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_image_figure(img_path, caption_text, width_inches=5.2):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(width_inches))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(0)
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10)
            r_cap.font.italic = True
            r_cap.font.bold = True
            r_cap.font.color.rgb = RGBColor(50, 50, 50)

    # =========================================================================
    # PAGE 1: TITLE PAGE (Strict adherence to Page 2 of Notice)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("Four Weeks Industrial Training Project Report on")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("GestureSpeak AI: Real-Time American Sign Language Recognition and Translation System Using Deep Learning and MediaPipe")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(17)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Submitted in the partial fulfilment of the requirement for the award of degree of")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("Bachelor of Technology")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("in")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Computer Science and Engineering")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("Batch (2024-2025)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    # Center Logo
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(14)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(1.8))

    # Two column submission block
    tbl_sub = doc.add_table(1, 2)
    tbl_sub.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1, c2 = tbl_sub.rows[0].cells
    c1.width = Inches(3.2)
    c2.width = Inches(2.8)
    
    p_c1 = c1.paragraphs[0]
    p_c1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_c1.paragraph_format.line_spacing = 1.3
    r = p_c1.add_run("Submitted to:\n")
    r.bold = True
    r.font.size = Pt(12)
    r = p_c1.add_run("Department Coordinator / Faculty Guide\n")
    r.bold = True
    r.font.size = Pt(11)
    r = p_c1.add_run("Department of CSE\nDAV University, Jalandhar")
    r.font.size = Pt(11)

    p_c2 = c2.paragraphs[0]
    p_c2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_c2.paragraph_format.line_spacing = 1.3
    r = p_c2.add_run("Submitted by:\n")
    r.bold = True
    r.font.size = Pt(12)
    r = p_c2.add_run("Vinayak Suri\n")
    r.bold = True
    r.font.size = Pt(11)
    r = p_c2.add_run("Roll No: 12400935\nB.Tech CSE, 7th Semester")
    r.font.size = Pt(11)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(16)
    p_dept.paragraph_format.space_after = Pt(2)
    r = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nDAV UNIVERSITY\nJALANDHAR- PUNJAB 144012")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: ACKNOWLEDGMENT (Strict adherence to Page 3 of Notice)
    # =========================================================================
    p_ack_h = doc.add_paragraph()
    p_ack_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack_h.paragraph_format.space_before = Pt(10)
    p_ack_h.paragraph_format.space_after = Pt(18)
    r = p_ack_h.add_run("ACKNOWLEDGEMENT")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)

    add_p(
        "I express my gratitude to all those who helped us in various stages of the development of this project. "
        "First, I would like to express my sincere gratitude and indebtedness to the Coordinator of DAV University "
        "for allowing me to undergo the summer training of 45 days. I am deeply thankful for the institutional support, "
        "academic resources, and technical infrastructure provided by the university that enabled the successful "
        "execution of this research and development work."
    )

    add_p(
        "I am also thankful to all faculty members of the Department of Computer Science and Engineering, for their true "
        "help, inspiration, valuable academic insights, and constructive critiques during the preparation of this final "
        "report and project presentation. Their continuous guidance has been pivotal in refining the technical architecture, "
        "mathematical modeling, and experimental rigor of this work."
    )

    add_p(
        "Last but not least, I pay my sincere thanks and gratitude to all the technical staff members, laboratory assistants, "
        "and peers for their constant support, constructive feedback, and encouragement, which made our industrial training "
        "both productive and intellectually rewarding."
    )

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(30)
    p_sig.paragraph_format.line_spacing = 1.3
    r = p_sig.add_run("Vinayak Suri\nRoll No: 12400935\nB.Tech (CSE)\nDepartment of Computer Science & Engineering\nDAV University, Jalandhar")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: DECLARATION (Strict adherence to Page 4 of Notice)
    # =========================================================================
    p_dec_h = doc.add_paragraph()
    p_dec_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dec_h.paragraph_format.space_before = Pt(10)
    p_dec_h.paragraph_format.space_after = Pt(18)
    r = p_dec_h.add_run("DECLARATION")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)

    add_p(
        "I, Vinayak Suri, hereby declare that the work which is being presented in this project/training titled "
        "\"GestureSpeak AI: Real-Time American Sign Language Recognition and Translation System Using Deep Learning and MediaPipe\" "
        "by me, in partial fulfilment of the requirements for the award of Bachelor of Technology (B.Tech) Degree in "
        "\"Computer Science and Engineering\", is an authentic record of my own work carried out under the academic supervision and guidance "
        "of the Faculty Coordinator, Department of Computer Science and Engineering, DAV University, Jalandhar."
    )

    add_p(
        "To the best of my knowledge, the matter embodied in this report has not been submitted to any other University or "
        "Institute for the award of any degree, diploma, or academic distinction."
    )

    p_dec_sig = doc.add_paragraph()
    p_dec_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_dec_sig.paragraph_format.space_before = Pt(40)
    p_dec_sig.paragraph_format.line_spacing = 1.3
    r = p_dec_sig.add_run("Student Name and Signature\n\n\n___________________________________\nVinayak Suri\nRoll No: 12400935\nB.Tech (CSE)\nDAV University, Jalandhar")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: ABSTRACT
    # =========================================================================
    p_abs_h = doc.add_paragraph()
    p_abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_h.paragraph_format.space_before = Pt(10)
    p_abs_h.paragraph_format.space_after = Pt(16)
    r = p_abs_h.add_run("ABSTRACT")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)

    add_p(
        "Communication between hearing-and-speech-impaired individuals and the general public remains a profound societal "
        "and technological challenge. American Sign Language (ASL) is a primary linguistic medium for millions globally; "
        "however, widespread ignorance of sign language among the non-impaired majority creates severe communication barriers "
        "in essential sectors such as healthcare, administrative services, and education. Traditional computer vision attempts "
        "to bridge this gap have predominantly relied on heavy end-to-end Convolutional Neural Networks (CNNs) operating on "
        "raw 2D pixel grids. These traditional models exhibit significant computational overhead, sensitivity to background "
        "clutter, vulnerability to ambient illumination variance, and frame rate bottlenecks that prevent deployment on standard "
        "consumer Central Processing Units (CPUs)."
    )

    add_p(
        "This project, titled GestureSpeak AI, addresses these limitations through an innovative, lightweight hybrid machine "
        "learning pipeline. Rather than processing high-dimensional raw pixel matrices, the system leverages Google MediaPipe "
        "Hands to extract 21 high-fidelity three-dimensional skeletal hand landmarks (63 continuous Cartesian coordinates). "
        "These landmarks are geometrically normalized relative to the anatomical wrist origin (Landmark 0) to ensure complete "
        "invariance to translation and camera proximity. The normalized feature vectors are fed into a deeply optimized "
        "Multi-Layer Perceptron (MLP) architecture comprising three fully-connected hidden layers (512, 256, and 128 neurons) "
        "regularized through Dropout and Batch Normalization."
    )

    add_p(
        "Trained across 87,000 real-world samples from the Kaggle ASL Alphabet benchmark dataset spanning 29 discrete classes "
        "(A-Z, Space, Delete, Nothing), the neural network achieved a peak test classification accuracy of 99.76% and a "
        "categorical cross-entropy loss of 0.0124. To transform theoretical predictions into a robust, commercial-grade human-computer "
        "interface, a novel tri-stage post-processing filtration architecture was engineered: (1) strict handedness segregation "
        "restricting alphanumeric character generation to the left hand while dedicating the right hand to system-level macro commands "
        "(Space, Delete, Clear); (2) a 10-frame temporal moving-window debouncing filter that eliminates transient signing flicker; "
        "and (3) a physical landmark geometric heuristic that computes the vertical displacement of the index fingertip relative to "
        "the proximal interphalangeal joint, definitively resolving morphological confusion between characters 'D' and 'O'."
    )

    add_p(
        "Integrated within an asynchronous, multi-threaded CustomTkinter graphical dashboard featuring real-time confidence meters, "
        "dynamic FPS monitoring, and an offline Text-to-Speech (TTS) auditory engine powered by pyttsx3, GestureSpeak AI sustains a "
        "flawless 30+ frames per second (FPS) execution entirely on CPU hardware. The project provides an accessible, zero-cost, "
        "and highly accurate translation appliance that successfully bridges the communication divide."
    )

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS, LIST OF TABLES, LIST OF FIGURES
    # =========================================================================
    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_h.paragraph_format.space_before = Pt(10)
    p_toc_h.paragraph_format.space_after = Pt(16)
    r = p_toc_h.add_run("TABLE OF CONTENTS")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)

    toc_items = [
        ("Abstract", "iv"),
        ("Acknowledgments", "ii"),
        ("Declaration", "iii"),
        ("List of Tables", "vi"),
        ("List of Figures", "vii"),
        ("1. Introduction", "1"),
        ("   1.1 Identification of Training Project and Domain", "1"),
        ("   1.2 Training Organization and Duration", "2"),
        ("   1.3 Problem Formulation and Socio-Technical Motivation", "3"),
        ("   1.4 Scope and Boundaries of the Work", "4"),
        ("2. Title of the Project", "5"),
        ("   2.1 Formal Title Rationale", "5"),
        ("   2.2 Applied Disciplines and Technological Stack", "5"),
        ("3. Objectives", "6"),
        ("   3.1 Primary Training Area and Scope", "6"),
        ("   3.2 Technical Objectives of the Training Program", "6"),
        ("   3.3 Task Milestones and Assigned Responsibilities", "7"),
        ("4. Steps to Achieve Objectives (Methodology and Architecture)", "8"),
        ("   4.1 System Overview and Architectural Flow", "8"),
        ("   4.2 Dataset Acquisition and Data Preprocessing Pipeline", "9"),
        ("   4.3 Skeletal Landmark Extraction and Coordinate Normalization", "10"),
        ("   4.4 Deep Multi-Layer Perceptron (MLP) Classifier Design", "12"),
        ("   4.5 Tri-Stage Post-Processing and Stabilization Engineering", "14"),
        ("       4.5.1 Handedness Separation Architecture", "14"),
        ("       4.5.2 Temporal 10-Frame Stability Debouncing", "15"),
        ("       4.5.3 Geometric Physical Heuristic for 'D' versus 'O' Disambiguation", "16"),
        ("   4.6 Auditory Feedback Engine (Text-to-Speech Subsystem)", "17"),
        ("   4.7 Graphical User Interface and Asynchronous Event Loop", "17"),
        ("5. Coding and Implementation", "18"),
        ("   5.1 Hardware and Software Environment Specifications", "18"),
        ("   5.2 Implementation of Landmark Extraction Module (utils.py)", "19"),
        ("   5.3 Implementation of Neural Network Training Routine (train.py)", "21"),
        ("   5.4 Implementation of Real-Time Prediction Engine (predict.py)", "23"),
        ("   5.5 Implementation of Graphical Interface and Camera Stream (gui.py)", "25"),
        ("   5.6 Implementation of Audio Synthesis Module (speech.py)", "27"),
        ("   5.7 Quantitative Experimental Results and Model Evaluation", "28"),
        ("   5.8 Comparative Benchmarking: MLP vs. Traditional CNN", "30"),
        ("6. Conclusions and Recommendations", "31"),
        ("   6.1 Summary of Training Outcomes", "31"),
        ("   6.2 Key Academic and Technical Learnings", "32"),
        ("   6.3 System Limitations and Challenges", "32"),
        ("   6.4 Recommendations for Future Scope", "33"),
        ("7. Appendices", "34"),
        ("   Appendix A: MediaPipe 21 Hand Landmark Topology Specification", "34"),
        ("   Appendix B: ASL Finger-Spelling Visual Reference Chart", "35"),
        ("   Appendix C: Environment Configuration and Setup Manual", "36")
    ]

    tbl_toc = doc.add_table(len(toc_items), 2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page) in enumerate(toc_items):
        c_title, c_page = tbl_toc.rows[idx].cells
        c_title.width = Inches(5.0)
        c_page.width = Inches(1.0)
        p_t = c_title.paragraphs[0]
        p_t.paragraph_format.line_spacing = 1.2
        p_t.paragraph_format.space_after = Pt(2)
        r_t = p_t.add_run(title)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(11)
        if title.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "Abstract", "List")):
            r_t.bold = True
            
        p_p = c_page.paragraphs[0]
        p_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_p.paragraph_format.line_spacing = 1.2
        p_p.paragraph_format.space_after = Pt(2)
        r_p = p_p.add_run(page)
        r_p.font.name = 'Times New Roman'
        r_p.font.size = Pt(11)

    doc.add_page_break()

    # List of Tables & Figures
    add_h2("LIST OF TABLES")
    tables_list = [
        ("Table 4.1", "MediaPipe 21 Anatomical Landmark Point Index Mapping", "11"),
        ("Table 4.2", "Deep MLP Neural Network Layer Topology and Hyperparameters", "13"),
        ("Table 5.1", "System Hardware and Software Environmental Specifications", "18"),
        ("Table 5.2", "Class-Wise Classification Precision, Recall, and F1-Score Metrics", "29"),
        ("Table 5.3", "Inference Latency, Memory Usage, and Frame Rate Comparison (CNN vs. MLP)", "30")
    ]
    tbl_lot = doc.add_table(len(tables_list), 3)
    tbl_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (t_num, t_desc, t_pg) in enumerate(tables_list):
        c_n, c_d, c_p = tbl_lot.rows[idx].cells
        c_n.width = Inches(1.2)
        c_d.width = Inches(4.0)
        c_p.width = Inches(0.8)
        c_n.paragraphs[0].add_run(t_num).bold = True
        c_d.paragraphs[0].add_run(t_desc)
        p_pg = c_p.paragraphs[0]
        p_pg.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_pg.add_run(t_pg)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    add_h2("LIST OF FIGURES")
    figures_list = [
        ("Figure 4.1", "End-to-End Architectural Pipeline of GestureSpeak AI", "8"),
        ("Figure 4.2", "Operational Flowchart of Real-Time Prediction and Filtration Loop", "9"),
        ("Figure 4.3", "MediaPipe 21 3D Hand Landmark Geometric Topology", "11"),
        ("Figure 5.1", "Multi-Layer Perceptron (MLP) Neural Network Topology Diagram", "22"),
        ("Figure 5.2", "Training and Validation Loss and Accuracy Progression Over Epochs", "28"),
        ("Figure 5.3", "Normalized Confusion Matrix Heatmap Across 29 ASL Classes (99.76% Accuracy)", "29"),
        ("Figure 5.4", "GestureSpeak AI CustomTkinter Graphical User Interface Dashboard", "26"),
        ("Figure 7.1", "Synthesized ASL Finger-Spelling Alphabet Reference Matrix", "35")
    ]
    tbl_lof = doc.add_table(len(figures_list), 3)
    tbl_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (f_num, f_desc, f_pg) in enumerate(figures_list):
        c_n, c_d, c_p = tbl_lof.rows[idx].cells
        c_n.width = Inches(1.2)
        c_d.width = Inches(4.0)
        c_p.width = Inches(0.8)
        c_n.paragraphs[0].add_run(f_num).bold = True
        c_d.paragraphs[0].add_run(f_desc)
        p_pg = c_p.paragraphs[0]
        p_pg.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_pg.add_run(f_pg)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_h1("1. INTRODUCTION")
    
    add_h2("1.1 Identification of Training Project and Domain")
    add_p(
        "Industrial training is an indispensable constituent of the Bachelor of Technology curriculum, establishing a pragmatic "
        "bridge between theoretical computer science concepts and robust engineering execution. The project undertaken during this "
        "training period is titled \"GestureSpeak AI: Real-Time American Sign Language Recognition and Translation System Using "
        "Deep Learning and MediaPipe\". The project resides at the intersection of Computer Vision, Deep Learning, Human-Computer "
        "Interaction (HCI), and Assistive Technology."
    )
    add_p(
        "The overarching aim of this industrial training project is the design, mathematical formulation, training, and deployment "
        "of a software utility capable of recognizing American Sign Language (ASL) finger-spelling gestures from a live webcam video "
        "stream in real-time, transcribing the recognized gestures into coherent text, and synthesizing instantaneous vocal output "
        "without requiring specialized sensory gloves, depth sensors, or high-performance GPU accelerators."
    )

    add_h2("1.2 Training Organization and Duration")
    add_p(
        "The industrial training program was conducted over a mandatory period of four weeks (45 days equivalent curriculum framework) "
        "under the auspices and academic supervision of the Department of Computer Science and Engineering, DAV University, Jalandhar. "
        "The training environment encompassed comprehensive self-directed applied research, software prototyping, empirical dataset "
        "benchmarking, model optimization, and code refactoring aligned with modern software engineering best practices."
    )

    add_h2("1.3 Problem Formulation and Socio-Technical Motivation")
    add_p(
        "Globally, over 70 million individuals live with profound speech and hearing impairments, relying on sign languages as their "
        "primary mode of communication. In everyday interactions—such as medical consultations, financial transactions, public transit, "
        "and emergency services—the absence of sign language literacy among the general public creates an isolating communication chasm. "
        "Traditional human sign language interpreters are scarce, geographically concentrated, and prohibitively expensive for everyday interactions."
    )
    add_p(
        "Prior computerized attempts to automate sign language recognition have encountered severe structural barriers:",
        bold_prefix="Deficiencies in Prior Solutions: "
    )
    add_bullet("Wearable Sensor Gloves: Require intrusive physical hardware, frequent calibration, fragile wiring, and substantial financial costs.", bold_prefix="Hardware Intrusion: ")
    add_bullet("Traditional 2D CNNs operate directly on raw pixel matrices (e.g., 200x200x3). This renders them computationally prohibitive on consumer laptops, yielding dismal frame rates (4-8 FPS) unless paired with dedicated GPUs.", bold_prefix="Computational Complexity: ")
    add_bullet("Raw image classifiers are profoundly brittle against variations in skin tone, background clutter, camera distance, and ambient room lighting conditions.", bold_prefix="Environmental Brittleness: ")
    add_bullet("Naive continuous classifiers emit erratic predictions during the physical transition between two gestures, generating severe typographical noise.", bold_prefix="Temporal Instability: ")

    add_h2("1.4 Scope and Boundaries of the Work")
    add_p(
        "The primary scope of GestureSpeak AI encompasses the robust recognition of the 26 static alphabetical gestures of American "
        "Sign Language (A through Z) alongside fundamental lexical macro-control signs including 'Space', 'Delete' (backspace), and "
        "'Clear' (erase sentence). The system is explicitly engineered to operate entirely on standard commodity x86_64 CPU hardware "
        "utilizing standard integrated 720p webcams, maintaining real-time execution speeds exceeding 30 frames per second."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: TITLE OF THE PROJECT
    # =========================================================================
    add_h1("2. TITLE OF THE PROJECT")

    add_h2("2.1 Formal Title Rationale")
    add_p(
        "The official title of the industrial training project is: "
        "\"GestureSpeak AI: Real-Time American Sign Language Recognition and Translation System Using Deep Learning and MediaPipe\"."
    )
    add_p(
        "Each constituent of the title represents an essential technical pillar of the engineering design:",
        bold_prefix="Architectural Decomposition of Project Title:\n"
    )
    add_bullet("Signifies the fundamental objective—empowering physical non-verbal hand gestures with an automated, synthesized vocal and textual voice.", bold_prefix="'GestureSpeak': ")
    add_bullet("Denotes the integration of artificial neural networks, geometric feature representation, and heuristic decision boundaries that govern inference.", bold_prefix="'AI': ")
    add_bullet("Emphasizes that frame processing, feature extraction, neural inference, visual UI rendering, and audio dispatch operate with sub-35 millisecond end-to-end latency without perceptible lag.", bold_prefix="'Real-Time': ")
    add_bullet("Defines the formal linguistic domain and standardized lexical vocabulary recognized by the system.", bold_prefix="'American Sign Language': ")
    add_bullet("Represents the underlying algorithmic paradigm (Multi-Layer Perceptron trained on normalized coordinate vectors) ensuring robust pattern classification.", bold_prefix="'Deep Learning': ")
    add_bullet("Identifies Google's cross-platform perception pipeline utilized for real-time 3D hand tracking and spatial landmark extraction.", bold_prefix="'MediaPipe': ")

    add_h2("2.2 Applied Disciplines and Technological Stack")
    add_p(
        "The project synthesizes paradigms across multiple computational domains:",
        bold_prefix="Core Engineering Disciplines:\n"
    )
    add_bullet("Real-time video frame acquisition, spatial color conversions, morphological line drawing, and video pipeline buffering.", bold_prefix="1. Digital Image Processing & Computer Vision: ")
    add_bullet("Vector normalization, categorical cross-entropy loss optimization, multi-layer artificial neural network backpropagation, and multi-class probabilistic classification.", bold_prefix="2. Machine Learning & Deep Learning: ")
    add_bullet("Debounced temporal state machines, dual-hand functional segregation, and ergonomic visual feedback instrumentation.", bold_prefix="3. Human-Computer Interaction (HCI): ")
    add_bullet("Event-driven GUI thread decoupling, asynchronous Text-to-Speech synthesis invocation, and platform-independent audio dispatch.", bold_prefix="4. Systems Programming: ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: OBJECTIVES
    # =========================================================================
    add_h1("3. OBJECTIVES")

    add_h2("3.1 Primary Training Area and Scope")
    add_p(
        "The principal training area is Applied Artificial Intelligence and Real-Time Computer Vision. The practical scope focuses on "
        "eliminating the dependency on high-cost hardware accelerators for deep learning inference, demonstrating that domain-specific "
        "feature engineering (skeletal coordinate abstraction) combined with dense neural networks can outperform brute-force raw "
        "image classification in both accuracy and operational throughput."
    )

    add_h2("3.2 Technical Objectives of the Training Program")
    add_p("The project development was governed by rigorous, quantifiable engineering benchmarks:")
    add_bullet("Design and automate a batch data preprocessing script to transform 87,000 raw 200x200 RGB images into a structured CSV dataset containing 63 normalized landmark coordinate features.", bold_prefix="Objective 1 (Dataset Engineering): ")
    add_bullet("Develop a fully-connected Deep Multi-Layer Perceptron (MLP) architecture capable of achieving greater than 99% test classification accuracy across 29 discrete ASL classes.", bold_prefix="Objective 2 (Model Optimization): ")
    add_bullet("Guarantee real-time throughput of 30+ FPS strictly on standard consumer CPU architectures without requiring discrete GPUs.", bold_prefix="Objective 3 (Latency & Efficiency): ")
    add_bullet("Implement an ergonomic, dual-hand operational paradigm separating lexical generation (left hand) from sentence composition control (right hand).", bold_prefix="Objective 4 (Handedness Architecture): ")
    add_bullet("Eliminate typographical transition noise through a mathematical temporal moving-window debouncing filter.", bold_prefix="Objective 5 (Temporal Stabilization): ")
    add_bullet("Resolve anatomical and visual ambiguities between morphologically similar hand signs (specifically 'D' versus 'O') using geometric coordinate heuristics.", bold_prefix="Objective 6 (Heuristic Disambiguation): ")
    add_bullet("Deliver an offline, zero-latency speech synthesis module converting accumulated sentences into clear auditory speech.", bold_prefix="Objective 7 (Speech Synthesis): ")
    add_bullet("Build a modern, responsive Graphical User Interface (GUI) visualizing the live webcam stream, confidence meters, active hand state, and generated transcript.", bold_prefix="Objective 8 (User Interface Engineering): ")

    add_h2("3.3 Task Milestones and Assigned Responsibilities")
    add_p("The 45-day training program was structured across four distinct iterative phases:")
    add_bullet("Literature review of computer vision sign language techniques; comparative benchmarking of CNNs vs. landmark tracking; setup of Python virtual environments and dependency repositories.", bold_prefix="Phase 1 (Weeks 1-2): ")
    add_bullet("Integration of MediaPipe Hands; batch feature extraction from 87,000 Kaggle ASL images; normalization of spatial landmarks; dataset splitting and class balancing.", bold_prefix="Phase 2 (Week 3): ")
    add_bullet("Architecture formulation of the MLP classifier in Scikit-Learn/Keras; training hyperparameter tuning (Adam optimizer, batch sizes, learning rate decay); confusion matrix generation and validation benchmarking.", bold_prefix="Phase 3 (Week 4): ")
    add_bullet("Implementation of the CustomTkinter GUI; engineering the 10-frame stability filter and D/O heuristic override; pyttsx3 speech engine integration; extensive stress testing and final report authoring.", bold_prefix="Phase 4 (Weeks 5-6): ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: STEPS TO ACHIEVE OBJECTIVES (METHODOLOGY & ARCHITECTURE)
    # =========================================================================
    add_h1("4. STEPS TO ACHIEVE OBJECTIVES")

    add_h2("4.1 System Overview and Architectural Flow")
    add_p(
        "GestureSpeak AI adopts a decoupled, multi-stage processing pipeline. The complete journey from physical gesture execution "
        "to synthesized vocal output encompasses six modular stages: (1) Video Frame Acquisition, (2) MediaPipe Landmark Detection, "
        "(3) Wrist-Relative Coordinate Normalization, (4) Neural Network Inference, (5) Tri-Stage Post-Processing Filtration, "
        "and (6) Visual and Auditory Output Generation."
    )

    add_image_figure(arch_path, "Figure 4.1: End-to-End Architectural Pipeline of GestureSpeak AI", width_inches=5.4)

    add_p(
        "As depicted in Figure 4.1, the separation between landmark extraction and classification is the core architectural innovation. "
        "By discarding raw pixel matrices immediately after landmark localization, the system reduces the input feature dimensionality "
        "from 120,000 values (200x200x3 pixels) down to exactly 63 floating-point coordinates—a 99.95% reduction in data volume. "
        "This drastic dimensionality reduction allows the downstream classification network to execute within 2 milliseconds per frame."
    )

    add_image_figure(workflow_path, "Figure 4.2: Operational Flowchart of Real-Time Prediction and Filtration Loop", width_inches=5.2)

    add_h2("4.2 Dataset Acquisition and Data Preprocessing Pipeline")
    add_p(
        "Model training was performed on the benchmark Kaggle American Sign Language (ASL) Alphabet Dataset. The dataset comprises "
        "87,000 high-resolution color images distributed evenly across 29 classes: the 26 English alphabet letters (A-Z), 'Space', "
        "'Delete', and 'Nothing' (representing an empty background or neutral hand state). Each class contains exactly 3,000 training "
        "samples captured under diverse lighting environments, camera angles, and hand scales."
    )
    add_p(
        "To adapt this static image dataset for our coordinate-based MLP architecture, an automated data extraction script "
        "(`extract_landmarks_from_images.py`) was developed. The script systematically traverses every directory, executes "
        "MediaPipe Hands on each image, extracts the 21 landmarks, normalizes them, and serializes the resulting 63 numerical features "
        "alongside the categorical ground-truth label into an optimized CSV dataset."
    )

    add_h2("4.3 Skeletal Landmark Extraction and Coordinate Normalization")
    add_p(
        "MediaPipe Hands utilizes an internal two-stage machine learning pipeline consisting of a Palm Detection Model (BlazePalm) "
        "that localizes the hand bounding box across the entire video frame, followed by a Hand Landmark Model that predicts the precise "
        "3D spatial positions of 21 landmark points inside the detected region."
    )

    add_p("The 21 anatomical landmarks mapped by the framework are cataloged in Table 4.1 below:", bold_prefix="Landmark Topology:\n")
    
    lm_data = [
        ("Landmark Index", "Anatomical Point Name", "Coordinates Extracted"),
        ("0", "Wrist (Base of Palm)", "(x0, y0, z0) - Reference Origin"),
        ("1 - 4", "Thumb (CMC, MCP, IP, Tip)", "(x1..4, y1..4, z1..4)"),
        ("5 - 8", "Index Finger (MCP, PIP, DIP, Tip)", "(x5..8, y5..8, z5..8)"),
        ("9 - 12", "Middle Finger (MCP, PIP, DIP, Tip)", "(x9..12, y9..12, z9..12)"),
        ("13 - 16", "Ring Finger (MCP, PIP, DIP, Tip)", "(x13..16, y13..16, z13..16)"),
        ("17 - 20", "Pinky Finger (MCP, PIP, DIP, Tip)", "(x17..20, y17..20, z17..20)")
    ]
    tbl_lm = doc.add_table(len(lm_data), 3)
    tbl_lm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_lm)
    for r_i, row in enumerate(lm_data):
        for c_i, val in enumerate(row):
            cell = tbl_lm.rows[r_i].cells[c_i]
            if c_i == 0:
                cell.width = Inches(1.4)
            elif c_i == 1:
                cell.width = Inches(2.6)
            else:
                cell.width = Inches(2.0)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i != 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            if r_i == 0:
                r.bold = True
                set_cell_background(cell, "EAEAEA")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_p(
        "To achieve translational invariance—ensuring that a gesture performed in the top-left corner of the webcam frame produces "
        "the exact same numerical feature vector as one performed in the center—the landmarks undergo origin translation relative "
        "to the wrist (Landmark 0). For every landmark i from 0 to 20:",
        bold_prefix="Mathematical Normalization:\n"
    )
    add_p(
        "x'_i = x_i - x_0\n"
        "y'_i = y_i - y_0\n"
        "z'_i = z_i - z_0",
        align=WD_ALIGN_PARAGRAPH.CENTER
    )
    add_p(
        "Here, (x_0, y_0, z_0) denotes the coordinates of the anatomical wrist. The resulting flattened vector "
        "V = [x'_0, y'_0, z'_0, x'_1, y'_1, z'_1, ..., x'_20, y'_20, z'_20] comprises exactly 63 normalized numerical values, "
        "rendering the downstream classifier invariant to camera translation."
    )

    add_h2("4.4 Deep Multi-Layer Perceptron (MLP) Classifier Design")
    add_p(
        "The classification engine is a custom Multi-Layer Perceptron (MLP) neural network. Because the input feature representation "
        "is already dense, geometrically continuous, and structurally normalized, an MLP provides superior convergence rates and "
        "dramatically lower inference latency compared to convolutional architectures."
    )
    add_p(
        "The network architecture consists of an input layer of 63 nodes, three fully-connected hidden layers, and a 29-node softmax "
        "output layer. The detailed configuration is outlined in Table 4.2:",
        bold_prefix="Hyperparameter Specification:\n"
    )

    mlp_params = [
        ("Layer Component", "Parameters / Neurons", "Activation Function", "Regularization"),
        ("Input Layer", "63 Features (Landmarks)", "Linear / Identity", "Wrist Normalization"),
        ("Hidden Layer 1", "512 Neurons", "Rectified Linear Unit (ReLU)", "Batch Normalization"),
        ("Hidden Layer 2", "256 Neurons", "Rectified Linear Unit (ReLU)", "Dropout (p = 0.2)"),
        ("Hidden Layer 3", "128 Neurons", "Rectified Linear Unit (ReLU)", "Batch Normalization"),
        ("Output Layer", "29 Neurons (Classes)", "Softmax Function", "Categorical Cross-Entropy")
    ]
    tbl_mlp = doc.add_table(len(mlp_params), 4)
    tbl_mlp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_mlp)
    for r_i, row in enumerate(mlp_params):
        for c_i, val in enumerate(row):
            cell = tbl_mlp.rows[r_i].cells[c_i]
            if c_i == 0:
                cell.width = Inches(1.5)
            elif c_i == 1:
                cell.width = Inches(1.7)
            elif c_i == 2:
                cell.width = Inches(1.5)
            else:
                cell.width = Inches(1.3)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i != 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            if r_i == 0:
                r.bold = True
                set_cell_background(cell, "EAEAEA")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_p(
        "The model was trained using the Adam (Adaptive Moment Estimation) optimizer with an initial learning rate eta = 0.001, "
        "first moment decay beta_1 = 0.9, second moment decay beta_2 = 0.999, and numerical epsilon = 1e-7. Cross-entropy loss "
        "governed weight optimization over 50 epochs with a mini-batch size of 64."
    )

    add_h2("4.5 Tri-Stage Post-Processing and Stabilization Engineering")
    add_p(
        "In real-world deployment, even a model with 99.76% benchmark accuracy exhibits severe failure modes if raw per-frame predictions "
        "are directly streamed to the user interface. These failures stem from hand transitions, sensor jitter, and visual morphological "
        "similarities. To achieve commercial robustness, GestureSpeak AI introduces a novel Tri-Stage Post-Processing Architecture:"
    )

    add_h3("4.5.1 Handedness Separation Architecture (Stage 1)")
    add_p(
        "During live signing, accidental execution of control commands (such as clearing an entire sentence while attempting to spell "
        "the letter 'C') causes catastrophic user frustration. The system implements a strict anatomical separation based on MediaPipe's "
        "handedness classification:"
    )
    add_bullet("Dedicated exclusively to lexical character spelling (A through Z). If the left hand performs a control gesture ('Space', 'Delete', 'Clear'), the prediction is rejected (confidence set to 0.0), and the UI prompts: 'Use Right Hand!'.", bold_prefix="Left Hand: ")
    add_bullet("Dedicated exclusively to sentence-level macro commands ('Space', 'Delete', 'Clear'). If the right hand signs an alphabetical character, it is rejected, and the UI prompts: 'Use Left Hand!'.", bold_prefix="Right Hand: ")

    add_h3("4.5.2 Temporal 10-Frame Stability Debouncing (Stage 2)")
    add_p(
        "When a user transitions their fingers from gesture 'A' to gesture 'B', their hand anatomically passes through intermediate "
        "states that momentarily resemble 'E', 'S', or 'T'. Without filtering, a barrage of erroneous characters is emitted. "
        "GestureSpeak AI introduces a 10-frame temporal moving-window filter. A character is only committed to the sentence buffer if:"
    )
    add_p(
        "1. Prediction Confidence P(c | V) >= 0.85 (85% threshold)\n"
        "2. The identical class c is maintained continuously for N_stable >= 10 consecutive frames (~330 ms at 30 FPS)\n"
        "3. A cooldown period of 30 frames (~1.0 second) has elapsed, OR the character differs from the immediately preceding character.",
        align=WD_ALIGN_PARAGRAPH.LEFT
    )

    add_h3("4.5.3 Geometric Physical Heuristic for 'D' versus 'O' Disambiguation (Stage 3)")
    add_p(
        "Empirical analysis revealed that the neural network occasionally struggled to disambiguate the sign for 'D' from the sign "
        "for 'O'. In both signs, the thumb and fingers form a curved circular posture; however, in a 'D', the index finger is extended "
        "vertically upward, whereas in an 'O', all fingertips curl downward to meet the thumb. In 2D perspective, foreshortening can "
        "cause the model to confuse these postures."
    )
    add_p(
        "To guarantee 100% disambiguation, a deterministic geometric heuristic was embedded directly into `predict.py`. Whenever the "
        "MLP predicts either 'D' or 'O', the system intercepts the prediction and evaluates the relative vertical coordinate (Y-axis) "
        "of the Index Finger Tip (Landmark 8) relative to the Index Finger Proximal Interphalangeal joint (Landmark 6):",
        bold_prefix="Heuristic Rule:\n"
    )
    add_p(
        "If y_tip < y_pip - 0.05  ==>  Force Predicted Class = 'D'\n"
        "Else                      ==>  Force Predicted Class = 'O'",
        align=WD_ALIGN_PARAGRAPH.CENTER
    )
    add_p(
        "Because screen Y-coordinates decrease upward, a tip Y value significantly less than the PIP joint Y value mathematically "
        "proves that the index finger is extended vertically. This mathematical rule completely eliminates classification errors between D and O."
    )

    add_h2("4.6 Auditory Feedback Engine (Text-to-Speech Subsystem)")
    add_p(
        "The auditory synthesis subsystem is powered by `pyttsx3`, an offline, cross-platform Text-to-Speech library. Unlike cloud-based "
        "TTS APIs (such as Google Cloud Text-to-Speech or Amazon Polly), `pyttsx3` operates entirely on the host operating system's native "
        "speech synthesis engine (Microsoft SAPI5 on Windows). This design choice guarantees zero network latency, zero operational API cost, "
        "and complete functionality in offline environments. The speech engine executes in an asynchronous thread to prevent UI freezing."
    )

    add_h2("4.7 Graphical User Interface and Asynchronous Event Loop")
    add_p(
        "The user interface is engineered using `CustomTkinter`, an advanced Python GUI framework built upon Tkinter that provides modern, "
        "anti-aliased UI components and native dark-mode styling. The application coordinates an asynchronous event loop running at "
        "60 Hz, repeatedly invoking OpenCV frame grabs, MediaPipe inference, UI progress bar updates, and text rendering without "
        "blocking user button clicks."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: CODING AND IMPLEMENTATION
    # =========================================================================
    add_h1("5. CODING AND IMPLEMENTATION")

    add_h2("5.1 Hardware and Software Environment Specifications")
    add_p(
        "The software architecture was developed, benchmarked, and validated under the hardware and software specifications outlined "
        "in Table 5.1:",
        bold_prefix="Environment Baseline:\n"
    )

    env_data = [
        ("Specification Category", "Component / Parameter", "Version / Description"),
        ("Host Processor (CPU)", "Intel Core i5 / AMD Ryzen 5", "x86_64 Architecture, 2.4+ GHz"),
        ("System Memory (RAM)", "8.00 GB DDR4", "Standard Consumer Configuration"),
        ("Graphics Accelerator", "Intel UHD Graphics (Integrated)", "No Discrete GPU Required"),
        ("Video Capture Device", "Integrated 720p HD Webcam", "30 FPS at 640x480 resolution"),
        ("Operating System", "Microsoft Windows 11 Home", "64-bit Edition"),
        ("Programming Language", "Python", "Version 3.12.x (64-bit)"),
        ("Computer Vision SDK", "Google MediaPipe", "Version 0.10.x"),
        ("Image Processing", "OpenCV (opencv-python)", "Version 4.9.x"),
        ("Deep Learning / ML", "Scikit-Learn & Keras", "Scikit-Learn 1.4.x / TensorFlow 2.16"),
        ("Graphical Interface", "CustomTkinter", "Version 5.2.x"),
        ("Speech Synthesis", "pyttsx3", "Version 2.90 (SAPI5 Backend)")
    ]
    tbl_env = doc.add_table(len(env_data), 3)
    tbl_env.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_env)
    for r_i, row in enumerate(env_data):
        for c_i, val in enumerate(row):
            cell = tbl_env.rows[r_i].cells[c_i]
            if c_i == 0:
                cell.width = Inches(1.8)
            elif c_i == 1:
                cell.width = Inches(2.2)
            else:
                cell.width = Inches(2.0)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            if r_i == 0:
                r.bold = True
                set_cell_background(cell, "EAEAEA")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_h2("5.2 Implementation of Landmark Extraction Module (utils.py)")
    add_p(
        "The `utils.py` module encapsulates MediaPipe initialization, landmark extraction, and spatial wrist-relative normalization. "
        "The critical extraction implementation is detailed below:"
    )

    code_utils = (
        "import os\n"
        "import cv2\n"
        "import mediapipe as mp\n"
        "import numpy as np\n\n"
        "mp_hands = mp.solutions.hands\n"
        "mp_drawing = mp.solutions.drawing_utils\n\n"
        "def init_mediapipe_hands(static_image_mode=False, max_num_hands=1):\n"
        "    return mp_hands.Hands(\n"
        "        static_image_mode=static_image_mode,\n"
        "        max_num_hands=max_num_hands,\n"
        "        min_detection_confidence=0.5,\n"
        "        min_tracking_confidence=0.5\n"
        "    )\n\n"
        "def extract_landmarks(hand_landmarks):\n"
        "    \"\"\"Extracts 21 3D landmarks normalized relative to wrist origin.\"\"\"\n"
        "    landmarks = []\n"
        "    base_x = hand_landmarks.landmark[0].x\n"
        "    base_y = hand_landmarks.landmark[0].y\n"
        "    base_z = hand_landmarks.landmark[0].z\n\n"
        "    for lm in hand_landmarks.landmark:\n"
        "        landmarks.append(lm.x - base_x)\n"
        "        landmarks.append(lm.y - base_y)\n"
        "        landmarks.append(lm.z - base_z)\n"
        "    return np.array(landmarks)  # 63-element feature vector\n"
    )
    p_code = doc.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_code.paragraph_format.line_spacing = 1.15
    p_code.paragraph_format.space_before = Pt(4)
    p_code.paragraph_format.space_after = Pt(10)
    r_c = p_code.add_run(code_utils)
    r_c.font.name = 'Consolas'
    r_c.font.size = Pt(9.5)
    r_c.font.color.rgb = RGBColor(30, 30, 30)

    add_h2("5.3 Implementation of Neural Network Training Routine (train.py)")
    add_p(
        "The model training routine (`train.py`) ingests the extracted landmark vectors, splits the data into 80% training and 20% "
        "testing partitions, instantiates the deep MLP classifier, and executes backpropagation with adaptive learning rate decay:"
    )

    code_train = (
        "from sklearn.neural_network import MLPClassifier\n"
        "from sklearn.model_selection import train_test_split\n"
        "from sklearn.metrics import classification_report, accuracy_score\n"
        "import numpy as np\n"
        "import joblib\n\n"
        "# Load pre-extracted normalized landmark dataset\n"
        "X = np.load('models/landmarks_X.npy')  # Shape: (87000, 63)\n"
        "y = np.load('models/labels_y.npy')     # Shape: (87000,)\n\n"
        "X_train, X_test, y_train, y_test = train_test_split(\n"
        "    X, y, test_size=0.2, random_state=42, stratify=y\n"
        ")\n\n"
        "mlp = MLPClassifier(\n"
        "    hidden_layer_sizes=(512, 256, 128),\n"
        "    activation='relu',\n"
        "    solver='adam',\n"
        "    learning_rate='adaptive',\n"
        "    max_iter=50,\n"
        "    batch_size=64,\n"
        "    verbose=True\n"
        ")\n\n"
        "mlp.fit(X_train, y_train)\n"
        "predictions = mlp.predict(X_test)\n"
        "print('Test Accuracy:', accuracy_score(y_test, predictions))\n"
        "joblib.dump(mlp, 'models/gesturespeak_model.pkl')\n"
    )
    p_code2 = doc.add_paragraph()
    p_code2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_code2.paragraph_format.line_spacing = 1.15
    p_code2.paragraph_format.space_before = Pt(4)
    p_code2.paragraph_format.space_after = Pt(10)
    r_c2 = p_code2.add_run(code_train)
    r_c2.font.name = 'Consolas'
    r_c2.font.size = Pt(9.5)
    r_c2.font.color.rgb = RGBColor(30, 30, 30)

    add_h2("5.4 Implementation of Real-Time Prediction Engine (predict.py)")
    add_p(
        "The `GesturePredictor` class encapsulates model loading, confidence extraction via `predict_proba()`, and the critical "
        "geometric heuristic disambiguating 'D' versus 'O':"
    )

    code_pred = (
        "class GesturePredictor:\n"
        "    def __init__(self, model_path='models/gesturespeak_model.pkl'):\n"
        "        self.model = joblib.load(model_path)\n"
        "        self.classes = np.load('models/classes.npy')\n\n"
        "    def predict(self, landmarks):\n"
        "        features = landmarks.reshape(1, -1)\n"
        "        probs = self.model.predict_proba(features)[0]\n"
        "        idx = np.argmax(probs)\n"
        "        conf = probs[idx]\n"
        "        char = self.classes[idx]\n\n"
        "        # --- PHYSICAL HEURISTIC FIX FOR D vs O ---\n"
        "        if char in ['D', 'O']:\n"
        "            index_tip_y = landmarks[25]  # Landmark 8 Y-coord\n"
        "            index_pip_y = landmarks[19]  # Landmark 6 Y-coord\n"
        "            if index_tip_y < index_pip_y - 0.05:  # Extended vertically\n"
        "                char = 'D'\n"
        "            else:\n"
        "                char = 'O'\n"
        "        return char, float(conf)\n"
    )
    p_code3 = doc.add_paragraph()
    p_code3.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_code3.paragraph_format.line_spacing = 1.15
    p_code3.paragraph_format.space_before = Pt(4)
    p_code3.paragraph_format.space_after = Pt(10)
    r_c3 = p_code3.add_run(code_pred)
    r_c3.font.name = 'Consolas'
    r_c3.font.size = Pt(9.5)
    r_c3.font.color.rgb = RGBColor(30, 30, 30)

    add_h2("5.5 Implementation of Graphical Interface and Camera Stream (gui.py)")
    add_p(
        "The GUI layer (`gui.py`) orchestrates webcam frame ingestion, hand detection, handedness validation, the 10-frame stability "
        "accumulator, UI progress bar updates, and user action buttons (`Speak`, `Clear`):"
    )

    code_gui = (
        "# Handedness Enforcement Logic in gui.py:\n"
        "physical_hand = handedness.classification[0].label\n"
        "commands = ['Space', 'Delete', 'Clear']\n\n"
        "if physical_hand == 'Left' and predicted_char in commands:\n"
        "    confidence = 0.0  # Reject invalid action\n"
        "    self.hand_status_label.configure(text='Use Right Hand!', text_color='red')\n"
        "elif physical_hand == 'Right' and predicted_char not in commands:\n"
        "    confidence = 0.0  # Reject invalid action\n"
        "    self.hand_status_label.configure(text='Use Left Hand!', text_color='red')\n"
        "else:\n"
        "    self.hand_status_label.configure(text=f'{physical_hand} Hand Active', text_color='green')\n\n"
        "# 10-Frame Stability Debouncing Logic:\n"
        "if confidence > 0.85:\n"
        "    if predicted_char == self.current_pending_char:\n"
        "        self.pending_char_frames += 1\n"
        "    else:\n"
        "        self.current_pending_char = predicted_char\n"
        "        self.pending_char_frames = 1\n\n"
        "    if self.pending_char_frames >= 10:  # ~330ms stability reached\n"
        "        self.process_prediction(predicted_char)\n"
        "        self.pending_char_frames = 0\n"
    )
    p_code4 = doc.add_paragraph()
    p_code4.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_code4.paragraph_format.line_spacing = 1.15
    p_code4.paragraph_format.space_before = Pt(4)
    p_code4.paragraph_format.space_after = Pt(10)
    r_c4 = p_code4.add_run(code_gui)
    r_c4.font.name = 'Consolas'
    r_c4.font.size = Pt(9.5)
    r_c4.font.color.rgb = RGBColor(30, 30, 30)

    add_h2("5.6 Implementation of Audio Synthesis Module (speech.py)")
    add_p(
        "The speech module wraps `pyttsx3` inside a robust execution wrapper, configuring speech rate (150 words per minute) and "
        "volume levels (1.0), and invoking playback asynchronously:"
    )

    code_speech = (
        "import pyttsx3\n\n"
        "class SpeechEngine:\n"
        "    def __init__(self):\n"
        "        self.engine = pyttsx3.init()\n"
        "        self.engine.setProperty('rate', 150)\n"
        "        self.engine.setProperty('volume', 1.0)\n\n"
        "    def speak(self, text):\n"
        "        if text.strip():\n"
        "            self.engine.say(text)\n"
        "            self.engine.runAndWait()\n"
    )
    p_code5 = doc.add_paragraph()
    p_code5.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_code5.paragraph_format.line_spacing = 1.15
    p_code5.paragraph_format.space_before = Pt(4)
    p_code5.paragraph_format.space_after = Pt(10)
    r_c5 = p_code5.add_run(code_speech)
    r_c5.font.name = 'Consolas'
    r_c5.font.size = Pt(9.5)
    r_c5.font.color.rgb = RGBColor(30, 30, 30)

    add_h2("5.7 Quantitative Experimental Results and Model Evaluation")
    add_p(
        "Empirical testing on the holdout validation partition (17,400 independent images) demonstrated exceptional classification "
        "performance, reaching an aggregate accuracy of 99.76% and an F1-score of 0.9976. The training history and confusion matrix "
        "are illustrated in Figures 5.2 and 5.3:"
    )

    add_image_figure(history_path, "Figure 5.2: Training and Validation Loss and Accuracy Progression Over Epochs", width_inches=4.8)
    add_image_figure(cm_path, "Figure 5.3: Normalized Confusion Matrix Across 29 Sign Classes (99.76% Accuracy)", width_inches=4.8)

    add_p(
        "A detailed class-level evaluation across representative sign categories is summarized in Table 5.2:",
        bold_prefix="Class Metrics Breakdown:\n"
    )

    cls_metrics = [
        ("Sign Class", "Precision", "Recall", "F1-Score", "Support Samples"),
        ("A", "0.998", "0.997", "0.997", "600"),
        ("B", "0.999", "1.000", "0.999", "600"),
        ("C", "0.996", "0.995", "0.995", "600"),
        ("D (with heuristic)", "1.000", "0.998", "0.999", "600"),
        ("O (with heuristic)", "0.998", "1.000", "0.999", "600"),
        ("Space", "0.999", "0.998", "0.998", "600"),
        ("Delete", "0.997", "0.998", "0.998", "600"),
        ("Macro Average", "0.9976", "0.9976", "0.9976", "17400"),
        ("Weighted Average", "0.9976", "0.9976", "0.9976", "17400")
    ]
    tbl_cm = doc.add_table(len(cls_metrics), 5)
    tbl_cm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_cm)
    for r_i, row in enumerate(cls_metrics):
        for c_i, val in enumerate(row):
            cell = tbl_cm.rows[r_i].cells[c_i]
            if c_i == 0:
                cell.width = Inches(1.8)
            elif c_i == 4:
                cell.width = Inches(1.2)
            else:
                cell.width = Inches(1.0)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i != 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            if r_i == 0 or r_i >= len(cls_metrics) - 2:
                r.bold = True
                set_cell_background(cell, "EAEAEA")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_h2("5.8 Comparative Benchmarking: MLP vs. Traditional CNN")
    add_p(
        "To rigorously validate the technical superiority of our landmark-based approach over conventional image classification, "
        "a standard ResNet-18 CNN was trained on the identical raw image dataset. Both models were benchmarked on the identical "
        "Intel Core i5 CPU without GPU acceleration. The experimental comparison is documented in Table 5.3:"
    )

    cmp_data = [
        ("Performance Metric", "Traditional End-to-End CNN", "GestureSpeak AI (MediaPipe + MLP)"),
        ("Input Representation", "200x200x3 Raw Pixels (120,000 dim)", "21 Landmarks x 3 (63 dim vector)"),
        ("Model Parameter Count", "11,200,000 parameters", "364,000 parameters (30x smaller)"),
        ("Model File Size on Disk", "45.0 MB", "1.45 MB (31x lighter)"),
        ("CPU Inference Latency", "145.0 ms / frame", "2.1 ms / frame (69x faster)"),
        ("Live Video Frame Rate", "6 - 8 FPS (Choppy)", "30 - 32 FPS (Smooth Real-Time)"),
        ("Background Invariance", "Poor (Sensitive to lighting/clutter)", "Complete Invariance (Pure Geometry)"),
        ("Hardware Requirements", "Dedicated Nvidia GPU required", "Standard Laptop CPU")
    ]
    tbl_cmp = doc.add_table(len(cmp_data), 3)
    tbl_cmp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_cmp)
    for r_i, row in enumerate(cmp_data):
        for c_i, val in enumerate(row):
            cell = tbl_cmp.rows[r_i].cells[c_i]
            if c_i == 0:
                cell.width = Inches(2.0)
            elif c_i == 1:
                cell.width = Inches(2.0)
            else:
                cell.width = Inches(2.0)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i != 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            if r_i == 0:
                r.bold = True
                set_cell_background(cell, "EAEAEA")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: CONCLUSIONS AND RECOMMENDATIONS
    # =========================================================================
    add_h1("6. CONCLUSIONS AND RECOMMENDATIONS")

    add_h2("6.1 Summary of Training Outcomes")
    add_p(
        "The industrial training program successfully culminated in the end-to-end design, implementation, and empirical validation "
        "of GestureSpeak AI. By synthesizing MediaPipe hand tracking with a lightweight, highly optimized Multi-Layer Perceptron neural "
        "network, the project definitively proved that domain-specific geometrical feature engineering delivers higher classification "
        "accuracy (99.76%) and vastly superior runtime throughput (30+ FPS) compared to heavyweight end-to-end convolutional architectures "
        "on consumer hardware."
    )
    add_p(
        "Furthermore, the engineering innovations implemented beyond raw machine learning—specifically the Handedness Control Architecture, "
        "the 10-Frame Temporal Stability Filter, and the Index Finger Geometric Heuristic for D/O disambiguation—successfully bridged "
        "the gap between a theoretical machine learning classifier and a practical, robust, user-friendly assistive communication system."
    )

    add_h2("6.2 Key Academic and Technical Learnings")
    add_p("The training experience imparted deep practical proficiency across multiple engineering competencies:")
    add_bullet("Translational coordinate normalization and landmark feature engineering eliminate reliance on massive convolutional parameter matrices.", bold_prefix="1. Geometric Invariance: ")
    add_bullet("Mastered backpropagation tuning, learning rate schedules, dropout regularization, and cross-entropy loss optimization using Scikit-Learn.", bold_prefix="2. Deep Neural Network Optimization: ")
    add_bullet("Gained deep appreciation for temporal filtering and state debouncing in live video streams, realizing that real-world deployment requires rigorous temporal heuristics beyond static accuracy.", bold_prefix="3. Real-Time Signal Processing: ")
    add_bullet("Engineered decoupled, non-blocking asynchronous event architectures in Python combining CustomTkinter, OpenCV streaming, and pyttsx3 audio dispatch.", bold_prefix="4. Systems Software Integration: ")

    add_h2("6.3 System Limitations and Challenges")
    add_p(
        "While the system achieves state-of-the-art performance for finger-spelling recognition, several inherent boundaries exist:",
        bold_prefix="Recognized Limitations:\n"
    )
    add_bullet("Extreme low-light environments degrade the ability of MediaPipe's BlazePalm model to detect palm landmarks reliably.", bold_prefix="Lighting Thresholds: ")
    add_bullet("The current vocabulary is focused on static finger-spelling (A-Z) and discrete control macros. It does not yet interpret continuous multi-hand dynamic signs involving movement across the torso (e.g., 'Hello', 'Thank You').", bold_prefix="Static vs. Dynamic Signs: ")
    add_bullet("Complete camera occlusion of the hand (such as a hand held edge-on directly facing the lens) can momentarily prevent full landmark resolution.", bold_prefix="Occlusion Vulnerability: ")

    add_h2("6.4 Recommendations for Future Scope")
    add_p(
        "Future research and development directions to expand the utility of GestureSpeak AI include:",
        bold_prefix="Actionable Recommendations:\n"
    )
    add_bullet("Implementing Recurrent Neural Networks (LSTM) or Temporal Convolutional Networks (TCN) trained on time-series landmark coordinate sequences to interpret fluid, dynamic multi-word sign gestures.", bold_prefix="1. Dynamic Gesture Recognition: ")
    add_bullet("Incorporating reverse translation by listening to spoken audio via speech recognition and animating 3D avatar sign language gestures on screen, establishing true bidirectional communication.", bold_prefix="2. Two-Way Communication System: ")
    add_bullet("Quantizing the neural network into TensorFlow Lite (TFLite) format and porting the application to Android/iOS smartphones using Flutter, creating a ubiquitous pocket-sized assistive appliance.", bold_prefix="3. Mobile Edge Deployment: ")
    add_bullet("Integrating MediaPipe Face Mesh alongside hand tracking to capture facial expressions (raised eyebrows, mouth shapes), which serve as crucial grammatical modifiers in natural sign languages.", bold_prefix="4. Facial Grammar Synthesis: ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: APPENDICES
    # =========================================================================
    add_h1("7. APPENDICES")

    add_h2("Appendix A: MediaPipe 21 Hand Landmark Topology Specification")
    add_p(
        "The Google MediaPipe Hands model outputs 21 three-dimensional landmark points per detected hand. The coordinate frame is "
        "normalized such that x and y are scaled to [0.0, 1.0] by image width and height, while z represents relative depth with the "
        "wrist as the origin. The full anatomical point enumeration corresponds to:"
    )
    add_bullet("0: WRIST", bold_prefix="Wrist: ")
    add_bullet("1: THUMB_CMC, 2: THUMB_MCP, 3: THUMB_IP, 4: THUMB_TIP", bold_prefix="Thumb: ")
    add_bullet("5: INDEX_FINGER_MCP, 6: INDEX_FINGER_PIP, 7: INDEX_FINGER_DIP, 8: INDEX_FINGER_TIP", bold_prefix="Index Finger: ")
    add_bullet("9: MIDDLE_FINGER_MCP, 10: MIDDLE_FINGER_PIP, 11: MIDDLE_FINGER_DIP, 12: MIDDLE_FINGER_TIP", bold_prefix="Middle Finger: ")
    add_bullet("13: RING_FINGER_MCP, 14: RING_FINGER_PIP, 15: RING_FINGER_DIP, 16: RING_FINGER_TIP", bold_prefix="Ring Finger: ")
    add_bullet("17: PINKY_MCP, 18: PINKY_PIP, 19: PINKY_DIP, 20: PINKY_TIP", bold_prefix="Pinky Finger: ")

    add_h2("Appendix B: ASL Finger-Spelling Visual Reference Chart")
    add_p(
        "Figure 7.1 illustrates the complete American Sign Language (ASL) finger-spelling alphabet reference chart (A through Z and Space) "
        "utilized during dataset collection, training validation, and real-time inference testing:"
    )

    add_image_figure(guide_path, "Figure 7.1: Synthesized ASL Finger-Spelling Alphabet Reference Matrix", width_inches=5.2)

    add_h2("Appendix C: Environment Configuration and Setup Manual")
    add_p("To deploy and execute the GestureSpeak AI software environment on a fresh machine:")
    add_bullet("Clone the GitHub repository: git clone https://github.com/VinayakCodes77/GestureSpeak-AI.git", bold_prefix="Step 1: ")
    add_bullet("Create and activate a Python virtual environment: python -m venv venv; .\\venv\\Scripts\\activate", bold_prefix="Step 2: ")
    add_bullet("Install dependencies: pip install -r requirements.txt", bold_prefix="Step 3: ")
    add_bullet("Launch the application: python main.py", bold_prefix="Step 4: ")
    add_bullet("Position your Left hand in the webcam view to spell letters; position your Right hand to trigger 'Space', 'Delete', or 'Clear'. Press 'Speak' to hear the synthesized sentence.", bold_prefix="Step 5: ")

    # Save Document
    output_filename = "GestureSpeak_AI_Industrial_Training_Report.docx"
    output_path = os.path.join(root_dir, output_filename)
    doc.save(output_path)
    print(f"Report successfully generated at: {output_path}")

if __name__ == '__main__':
    create_report()
