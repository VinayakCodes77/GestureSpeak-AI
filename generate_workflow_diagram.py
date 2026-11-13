import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_workflow_diagram():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Main Titles
    ax.text(8.0, 10.6, "GestureSpeak AI: Real-Time Operational Flowchart",
            fontsize=18, fontweight='bold', fontfamily='sans-serif',
            ha='center', va='center', color='#0F172A')
    ax.text(8.0, 10.25, "Continuous 30 FPS Video Pipeline: Perception, Neural Inference, Tri-Stage Filtering, and Auditory Dispatch",
            fontsize=11, fontfamily='sans-serif', fontstyle='italic',
            ha='center', va='center', color='#475569')

    # Helpers for diagram nodes
    def draw_proc(x, y, w, h, title, subtitle="", bg="#FFFFFF", border="#3B82F6", tcolor="#0F172A"):
        # Shadow
        shadow = patches.FancyBboxPatch((x + 0.05, y - 0.05), w, h,
                                       boxstyle="round,pad=0.08,rounding_size=0.12",
                                       facecolor='#CBD5E1', edgecolor='none', alpha=0.5, zorder=2)
        ax.add_patch(shadow)
        # Box
        box = patches.FancyBboxPatch((x, y), w, h,
                                     boxstyle="round,pad=0.08,rounding_size=0.12",
                                     facecolor=bg, edgecolor=border, linewidth=1.8, zorder=3)
        ax.add_patch(box)
        # Text
        ax.text(x + w/2, y + h/2 + (0.12 if subtitle else 0), title,
                fontsize=9.5, fontweight='bold', fontfamily='sans-serif',
                ha='center', va='center', color=tcolor, zorder=4)
        if subtitle:
            ax.text(x + w/2, y + h/2 - 0.16, subtitle,
                    fontsize=8.0, fontfamily='sans-serif', fontstyle='italic',
                    ha='center', va='center', color='#64748B', zorder=4)

    def draw_decision(x, y, w, h, title, subtitle="", bg="#FEF3C7", border="#D97706", tcolor="#92400E"):
        # Polygon diamond
        cx, cy = x + w/2, y + h/2
        pts = np.array([[cx, y + h], [x + w, cy], [cx, y], [x, cy]])
        # Shadow
        shadow_pts = pts + np.array([0.05, -0.05])
        shadow = patches.Polygon(shadow_pts, facecolor='#CBD5E1', edgecolor='none', alpha=0.5, zorder=2)
        ax.add_patch(shadow)
        # Main diamond
        diamond = patches.Polygon(pts, facecolor=bg, edgecolor=border, linewidth=1.8, zorder=3)
        ax.add_patch(diamond)
        # Text
        ax.text(cx, cy + (0.12 if subtitle else 0), title,
                fontsize=9.0, fontweight='bold', fontfamily='sans-serif',
                ha='center', va='center', color=tcolor, zorder=4)
        if subtitle:
            ax.text(cx, cy - 0.16, subtitle,
                    fontsize=7.8, fontfamily='sans-serif', fontstyle='italic',
                    ha='center', va='center', color='#B45309', zorder=4)

    def draw_terminal(x, y, w, h, title, bg="#E2E8F0", border="#475569", tcolor="#0F172A"):
        shadow = patches.FancyBboxPatch((x + 0.05, y - 0.05), w, h,
                                       boxstyle="round,pad=0.08,rounding_size=0.35",
                                       facecolor='#CBD5E1', edgecolor='none', alpha=0.5, zorder=2)
        ax.add_patch(shadow)
        box = patches.FancyBboxPatch((x, y), w, h,
                                     boxstyle="round,pad=0.08,rounding_size=0.35",
                                     facecolor=bg, edgecolor=border, linewidth=1.8, zorder=3)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, title,
                fontsize=10.0, fontweight='bold', fontfamily='sans-serif',
                ha='center', va='center', color=tcolor, zorder=4)

    # 3 Column Container Panels
    # COL 1: Perception & Feature Extraction
    p1 = patches.FancyBboxPatch((0.5, 0.4), 4.7, 9.4,
                               boxstyle="round,pad=0.1,rounding_size=0.15",
                               facecolor='#F1F5F9', edgecolor='#CBD5E1', linewidth=1.2, zorder=1)
    ax.add_patch(p1)
    ax.text(2.85, 9.55, "STAGE I: PERCEPTION & INFERENCE", fontsize=11, fontweight='bold', color='#1E293B', ha='center', zorder=2)

    # COL 2: Tri-Stage Filtration Engine
    p2 = patches.FancyBboxPatch((5.65, 0.4), 4.7, 9.4,
                               boxstyle="round,pad=0.1,rounding_size=0.15",
                               facecolor='#FEF2F2', edgecolor='#FECACA', linewidth=1.2, zorder=1)
    ax.add_patch(p2)
    ax.text(8.0, 9.55, "STAGE II: TRI-STAGE FILTRATION", fontsize=11, fontweight='bold', color='#991B1B', ha='center', zorder=2)

    # COL 3: Sentence Buffer, GUI & Speech
    p3 = patches.FancyBboxPatch((10.8, 0.4), 4.7, 9.4,
                               boxstyle="round,pad=0.1,rounding_size=0.15",
                               facecolor='#F0FDF4', edgecolor='#BBF7D0', linewidth=1.2, zorder=1)
    ax.add_patch(p3)
    ax.text(13.15, 9.55, "STAGE III: UI & AUDIO SYNTHESIS", fontsize=11, fontweight='bold', color='#166534', ha='center', zorder=2)

    # ==================== COLUMN 1 NODES ====================
    draw_terminal(1.35, 8.7, 3.0, 0.6, "Camera Stream Start (30 FPS)", bg="#E0F2FE", border="#0284C7", tcolor="#0369A1")
    draw_proc(1.35, 7.6, 3.0, 0.75, "Video Frame Capture", "OpenCV cv2.flip (Horizontal RGB)", bg="#FFFFFF", border="#0284C7")
    draw_decision(1.2, 6.2, 3.3, 0.95, "Hand Detected?", "MediaPipe Palm Detector", bg="#FEF3C7", border="#D97706", tcolor="#92400E")
    draw_proc(1.35, 4.9, 3.0, 0.8, "Landmark Localization", "Extract 21 3D Spatial Landmarks", bg="#FFFFFF", border="#0284C7")
    draw_proc(1.35, 3.6, 3.0, 0.85, "Wrist Normalization", "x'_i = x_i - x_0 (63D Vector)", bg="#FFFFFF", border="#0284C7")
    draw_proc(1.35, 2.3, 3.0, 0.85, "Deep MLP Inference", "Predict Class & Probabilities", bg="#EDE9FE", border="#7C3AED", tcolor="#5B21B6")
    draw_proc(1.35, 0.9, 3.0, 0.95, "Extract Raw Prediction", "P(class | landmarks) & Conf Score", bg="#FFFFFF", border="#7C3AED")

    # Arrows in Col 1
    arr_b = dict(arrowstyle="->", lw=1.8, color="#0284C7", mutation_scale=12)
    ax.annotate("", xy=(2.85, 8.35), xytext=(2.85, 8.7), arrowprops=arr_b, zorder=5)
    ax.annotate("", xy=(2.85, 7.15), xytext=(2.85, 7.6), arrowprops=arr_b, zorder=5)
    ax.annotate("", xy=(2.85, 5.7), xytext=(2.85, 6.2), arrowprops=arr_b, zorder=5)
    ax.text(3.05, 5.9, "Yes", fontsize=8.5, fontweight='bold', color="#059669", zorder=5)

    # No Hand -> Reset
    ax.annotate("No", xy=(0.8, 6.67), xytext=(1.2, 6.67),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#DC2626"),
                fontsize=8.5, fontweight='bold', color="#DC2626", zorder=5)
    ax.text(0.8, 7.1, "Display 'Hand: None'\nReset Stability Count", fontsize=7.5, color="#DC2626", ha='center', zorder=5)

    ax.annotate("", xy=(2.85, 4.45), xytext=(2.85, 4.9), arrowprops=arr_b, zorder=5)
    ax.annotate("", xy=(2.85, 3.15), xytext=(2.85, 3.6), arrowprops=arr_b, zorder=5)
    ax.annotate("", xy=(2.85, 1.85), xytext=(2.85, 2.3), arrowprops=dict(arrowstyle="->", lw=1.8, color="#7C3AED", mutation_scale=12), zorder=5)

    # Col 1 to Col 2 Transition
    ax.annotate("", xy=(6.0, 1.38), xytext=(4.35, 1.38),
                arrowprops=dict(arrowstyle="->", lw=2, color="#4338CA", mutation_scale=14), zorder=5)

    # ==================== COLUMN 2 NODES ====================
    draw_decision(6.2, 0.9, 3.6, 0.95, "Prediction is 'D' or 'O'?", "Ambiguity Check", bg="#FFFBEB", border="#F59E0B")
    draw_proc(6.5, 2.35, 3.0, 0.9, "Heuristic Disambiguation", "Index Tip vs PIP Y-Coord (y_tip < y_pip - 0.05)", bg="#FEF3C7", border="#D97706")
    draw_decision(6.2, 3.75, 3.6, 0.95, "Handedness Valid?", "L=A-Z, R=Commands", bg="#FEE2E2", border="#EF4444", tcolor="#B91C1C")
    draw_decision(6.2, 5.2, 3.6, 0.95, "Confidence >= 85%?", "Threshold Verification", bg="#FEE2E2", border="#EF4444", tcolor="#B91C1C")
    draw_decision(6.2, 6.65, 3.6, 1.0, "Stable for >= 10 Frames?", "~330ms Moving Window", bg="#FEE2E2", border="#EF4444", tcolor="#B91C1C")
    draw_decision(6.2, 8.15, 3.6, 0.95, "Cooldown Expired?", "30 frames OR new char", bg="#DCFCE7", border="#16A34A", tcolor="#15803D")

    # Arrows in Col 2
    ax.annotate("", xy=(8.0, 2.35), xytext=(8.0, 1.85),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#D97706", mutation_scale=12), zorder=5)
    ax.text(8.15, 2.05, "Yes", fontsize=8.5, fontweight='bold', color="#D97706", zorder=5)

    # Bypass heuristic if not D/O
    ax.annotate("", xy=(9.8, 3.75), xytext=(9.8, 1.85),
                arrowprops=dict(arrowstyle="->", lw=1.5, ls="--", color="#64748B",
                                connectionstyle="arc3,rad=-0.15"), zorder=5)
    ax.text(10.15, 2.8, "No (Not D/O)", fontsize=8.2, fontweight='bold', color="#64748B", zorder=5)

    ax.annotate("", xy=(8.0, 3.75), xytext=(8.0, 3.25),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#059669", mutation_scale=12), zorder=5)

    # Invalid Handedness -> Reject
    ax.annotate("No", xy=(5.8, 4.22), xytext=(6.2, 4.22),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#DC2626"),
                fontsize=8.5, fontweight='bold', color="#DC2626", zorder=5)
    ax.text(5.5, 4.6, "Reject: Conf=0.0\n'Use Other Hand!'", fontsize=7.2, color="#DC2626", ha='center', zorder=5)

    ax.annotate("", xy=(8.0, 5.2), xytext=(8.0, 4.7),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#059669", mutation_scale=12), zorder=5)
    ax.text(8.15, 4.95, "Yes", fontsize=8.5, fontweight='bold', color="#059669", zorder=5)

    # Low Confidence -> Reject
    ax.annotate("No", xy=(5.8, 5.67), xytext=(6.2, 5.67),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#DC2626"),
                fontsize=8.5, fontweight='bold', color="#DC2626", zorder=5)
    ax.text(5.5, 6.05, "Reject: Blurry or\nHand Transition", fontsize=7.2, color="#DC2626", ha='center', zorder=5)

    ax.annotate("", xy=(8.0, 6.65), xytext=(8.0, 6.15),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#059669", mutation_scale=12), zorder=5)
    ax.text(8.15, 6.4, "Yes", fontsize=8.5, fontweight='bold', color="#059669", zorder=5)

    # Not stable yet -> increment
    ax.annotate("No", xy=(5.8, 7.15), xytext=(6.2, 7.15),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#D97706"),
                fontsize=8.5, fontweight='bold', color="#D97706", zorder=5)
    ax.text(5.5, 7.6, "pending_frames += 1\nWait next frame", fontsize=7.2, color="#D97706", ha='center', zorder=5)

    ax.annotate("", xy=(8.0, 8.15), xytext=(8.0, 7.65),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#059669", mutation_scale=12), zorder=5)
    ax.text(8.15, 7.9, "Yes", fontsize=8.5, fontweight='bold', color="#059669", zorder=5)

    # Col 2 to Col 3 Transition
    ax.annotate("", xy=(11.5, 8.62), xytext=(9.8, 8.62),
                arrowprops=dict(arrowstyle="->", lw=2, color="#059669", mutation_scale=14), zorder=5)
    ax.text(10.65, 8.8, "Verified", fontsize=8.5, fontweight='bold', color="#059669", ha='center', zorder=5)

    # ==================== COLUMN 3 NODES ====================
    draw_decision(11.35, 8.15, 3.6, 0.95, "Action Dispatcher", "Branch by Character Type", bg="#DCFCE7", border="#16A34A")

    draw_proc(11.65, 6.9, 3.0, 0.75, "Append Alphabet (A-Z)", "sentence += char", bg="#FFFFFF", border="#16A34A")
    draw_proc(11.65, 5.75, 3.0, 0.75, "Execute Space Command", "sentence += ' '", bg="#FFFFFF", border="#16A34A")
    draw_proc(11.65, 4.6, 3.0, 0.75, "Execute Delete Command", "sentence = sentence[:-1]", bg="#FFFFFF", border="#EA580C")
    draw_proc(11.65, 3.45, 3.0, 0.75, "Execute Clear Command", "sentence = ''", bg="#FFFFFF", border="#DC2626")

    draw_proc(11.65, 2.05, 3.0, 0.95, "Update GUI Dashboard", "Refresh Textbox, Confidence Bar,\nHand Status & FPS Label", bg="#F3E8FF", border="#9333EA", tcolor="#581C87")

    draw_terminal(11.65, 0.75, 3.0, 0.85, "Voice Synthesis (pyttsx3)", bg="#FEF08A", border="#CA8A04", tcolor="#854D0E")

    # Arrows in Col 3
    arr_g = dict(arrowstyle="->", lw=1.6, color="#16A34A", mutation_scale=11)
    ax.annotate("", xy=(13.15, 7.65), xytext=(13.15, 8.15), arrowprops=arr_g, zorder=5)
    ax.annotate("", xy=(13.15, 6.5), xytext=(13.15, 6.9), arrowprops=arr_g, zorder=5)
    ax.annotate("", xy=(13.15, 5.35), xytext=(13.15, 5.75), arrowprops=arr_g, zorder=5)
    ax.annotate("", xy=(13.15, 4.2), xytext=(13.15, 4.6), arrowprops=arr_g, zorder=5)
    ax.annotate("", xy=(13.15, 3.0), xytext=(13.15, 3.45), arrowprops=arr_g, zorder=5)

    # To Voice Synthesis
    ax.annotate("", xy=(13.15, 1.6), xytext=(13.15, 2.05),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#9333EA", mutation_scale=12), zorder=5)
    ax.text(13.4, 1.82, "User clicks 'Speak'", fontsize=8.0, fontstyle='italic', color="#7E22CE", zorder=5)

    # Feedback loop: Col 3 back to Next Frame
    ax.annotate("", xy=(2.85, 0.5), xytext=(13.15, 0.75),
                arrowprops=dict(arrowstyle="->", lw=1.5, ls=":", color="#64748B",
                                connectionstyle="arc3,rad=0.15"), zorder=5)
    ax.text(8.0, 0.15, "Continuous Event Loop: Next Video Frame Grab (30 FPS)",
            fontsize=8.5, fontstyle='italic', color="#475569", ha='center', zorder=5)

    plt.tight_layout()
    output_path = r"C:\Users\vinay\.gemini\antigravity\scratch\GestureSpeakAI\workflow_diagram.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("New workflow_diagram.png saved successfully!")

if __name__ == '__main__':
    create_workflow_diagram()
