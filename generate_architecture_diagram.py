import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_system_architecture():
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Main Title
    ax.text(8.0, 9.6, "GestureSpeak AI: End-to-End System Architectural Pipeline",
            fontsize=18, fontweight='bold', fontfamily='sans-serif',
            ha='center', va='center', color='#0F172A')
    ax.text(8.0, 9.25, "Decoupled Hybrid Architecture: Offline Deep Learning Training vs. Online Real-Time Inference",
            fontsize=11, fontfamily='sans-serif', fontstyle='italic',
            ha='center', va='center', color='#475569')

    # Function to draw styled rounded box with shadow
    def draw_box(x, y, w, h, title, subtitle="", items=None, bg_color="#FFFFFF", border_color="#3B82F6", title_color="#0F172A"):
        # Shadow
        shadow = patches.FancyBboxPatch((x + 0.06, y - 0.06), w, h,
                                       boxstyle="round,pad=0.1,rounding_size=0.15",
                                       facecolor='#CBD5E1', edgecolor='none', alpha=0.5, zorder=2)
        ax.add_patch(shadow)
        # Main box
        box = patches.FancyBboxPatch((x, y), w, h,
                                     boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor=bg_color, edgecolor=border_color, linewidth=2, zorder=3)
        ax.add_patch(box)
        # Title
        ax.text(x + w/2, y + h - 0.28, title, fontsize=10.5, fontweight='bold', fontfamily='sans-serif',
                ha='center', va='center', color=title_color, zorder=4)
        curr_y = y + h - 0.52
        if subtitle:
            ax.text(x + w/2, curr_y, subtitle, fontsize=8.5, fontstyle='italic', fontfamily='sans-serif',
                    ha='center', va='center', color='#64748B', zorder=4)
            curr_y -= 0.25
        if items:
            for itm in items:
                ax.text(x + 0.15, curr_y, itm, fontsize=8.2, fontfamily='sans-serif',
                        ha='left', va='center', color='#334155', zorder=4)
                curr_y -= 0.22

    # Draw section headers
    # PANEL 1: OFFLINE TRAINING PIPELINE
    panel1_bg = patches.FancyBboxPatch((0.4, 4.9), 15.2, 3.9,
                                      boxstyle="round,pad=0.15,rounding_size=0.2",
                                      facecolor='#EFF6FF', edgecolor='#BFDBFE', linewidth=1.5, zorder=1)
    ax.add_patch(panel1_bg)
    ax.text(0.8, 8.55, "PHASE 1: OFFLINE DATA ENGINEERING & MODEL TRAINING PIPELINE",
            fontsize=12, fontweight='bold', color='#1E40AF', zorder=2)

    # Boxes in Phase 1
    draw_box(0.6, 5.2, 2.6, 2.9, "1. Kaggle ASL Dataset",
             subtitle="Raw Image Corpus",
             items=["- 87,000 RGB Images", "- 29 Distinct Classes", "- 26 Letters (A-Z)", "- Space, Delete, Nothing", "- 3,000 images per class"],
             bg_color="#FFFFFF", border_color="#3B82F6")

    draw_box(3.6, 5.2, 2.7, 2.9, "2. Feature Extraction",
             subtitle="extract_landmarks.py",
             items=["- MediaPipe BlazePalm", "- 21 3D Hand Landmarks", "- Continuous extraction", "- 63 raw Cartesian coordinates", "- Discards raw pixel data"],
             bg_color="#FFFFFF", border_color="#0284C7")

    draw_box(6.7, 5.2, 2.7, 2.9, "3. Data Normalization",
             subtitle="Translational Invariance",
             items=["- Wrist point 0 as origin", "- x'_i = x_i - x_0", "- y'_i = y_i - y_0", "- z'_i = z_i - z_0", "- Invariant to distance/scale"],
             bg_color="#FFFFFF", border_color="#0D9488")

    draw_box(9.8, 5.2, 2.7, 2.9, "4. Deep MLP Training",
             subtitle="train_model.py",
             items=["- 3 Dense Hidden Layers", "- Topology: 512-256-128", "- ReLU Activations", "- Adam Optimizer (lr=1e-3)", "- Categorical Cross-Entropy"],
             bg_color="#FFFFFF", border_color="#7C3AED")

    draw_box(12.9, 5.2, 2.5, 2.9, "5. Trained Model",
             subtitle="gesturespeak_model.pkl",
             items=["- 99.76% Test Accuracy", "- 1.45 MB Model Size", "- 2.1 ms CPU Latency", "- Serialized with Joblib", "- 29 Output Probabilities"],
             bg_color="#FEF3C7", border_color="#D97706", title_color="#B45309")

    # Connect Phase 1 with arrows
    arrow_props = dict(arrowstyle="->", lw=2, color="#2563EB", mutation_scale=15)
    ax.annotate("", xy=(3.6, 6.65), xytext=(3.2, 6.65), arrowprops=arrow_props, zorder=5)
    ax.annotate("", xy=(6.7, 6.65), xytext=(6.3, 6.65), arrowprops=arrow_props, zorder=5)
    ax.annotate("", xy=(9.8, 6.65), xytext=(9.4, 6.65), arrowprops=arrow_props, zorder=5)
    ax.annotate("", xy=(12.9, 6.65), xytext=(12.5, 6.65), arrowprops=arrow_props, zorder=5)

    # PANEL 2: ONLINE REAL-TIME INFERENCE SUBSYSTEM
    panel2_bg = patches.FancyBboxPatch((0.4, 0.4), 15.2, 4.2,
                                      boxstyle="round,pad=0.15,rounding_size=0.2",
                                      facecolor='#F0FDF4', edgecolor='#BBF7D0', linewidth=1.5, zorder=1)
    ax.add_patch(panel2_bg)
    ax.text(0.8, 4.35, "PHASE 2: ONLINE REAL-TIME INFERENCE & HUMAN-COMPUTER INTERACTION PIPELINE (30+ FPS)",
            fontsize=12, fontweight='bold', color='#166534', zorder=2)

    # Boxes in Phase 2
    draw_box(0.6, 0.7, 2.6, 3.3, "A. Video Capture",
             subtitle="OpenCV Video Stream",
             items=["- 720p HD Integrated Webcam", "- 30 Frames Per Second", "- Horizontal Frame Flip", "- BGR to RGB Conversion", "- Low-latency frame grab"],
             bg_color="#FFFFFF", border_color="#10B981")

    draw_box(3.6, 0.7, 2.7, 3.3, "B. Skeletal Tracking",
             subtitle="MediaPipe Hands (utils.py)",
             items=["- Real-Time Palm Detection", "- 21 3D Skeletal Joints", "- Relative Wrist Translation", "- Generates 63-dim Vector", "- Handedness Classification"],
             bg_color="#FFFFFF", border_color="#059669")

    draw_box(6.7, 0.7, 2.7, 3.3, "C. Neural Inference",
             subtitle="predict.py + Model",
             items=["- Predicts Class Index", "- Calculates Probabilities", "- Extracts Confidence Score", "- Sub-2.5ms inference on CPU", "- Feeds Tri-Stage Filter"],
             bg_color="#FFFFFF", border_color="#6366F1")

    draw_box(9.8, 0.7, 2.7, 3.3, "D. Tri-Stage Filter",
             subtitle="Post-Processing Engine",
             items=["1. Handedness Enforcement:\n   L=A-Z, R=Commands", "2. 10-Frame Debouncing:\n   Eliminates jitter/noise", "3. D vs O Heuristic:\n   Index Tip Y-coord check"],
             bg_color="#FFFBEB", border_color="#F59E0B", title_color="#B45309")

    draw_box(12.9, 0.7, 2.5, 3.3, "E. Output Synthesis",
             subtitle="CustomTkinter + TTS",
             items=["- Dark Mode GUI Display", "- Real-Time Confidence Bar", "- Dynamic Sentence Buffer", "- pyttsx3 Offline Audio", "- Native Laptop Speakers"],
             bg_color="#FAF5FF", border_color="#9333EA", title_color="#6B21A8")

    # Connect Phase 2 with arrows
    arrow_props2 = dict(arrowstyle="->", lw=2, color="#059669", mutation_scale=15)
    ax.annotate("", xy=(3.6, 2.35), xytext=(3.2, 2.35), arrowprops=arrow_props2, zorder=5)
    ax.annotate("", xy=(6.7, 2.35), xytext=(6.3, 2.35), arrowprops=arrow_props2, zorder=5)
    ax.annotate("", xy=(9.8, 2.35), xytext=(9.4, 2.35), arrowprops=arrow_props2, zorder=5)
    ax.annotate("", xy=(12.9, 2.35), xytext=(12.5, 2.35), arrowprops=arrow_props2, zorder=5)

    # Cross-phase connection: Model -> Neural Inference
    ax.annotate("Loads Weights", xy=(8.05, 4.0), xytext=(14.15, 5.2),
                arrowprops=dict(arrowstyle="->", lw=2, ls="--", color="#DC2626",
                                connectionstyle="angle,angleA=-90,angleB=180,rad=15",
                                mutation_scale=15),
                fontsize=9.5, fontweight='bold', color="#DC2626", zorder=6)

    plt.tight_layout()
    output_path = r"C:\Users\vinay\.gemini\antigravity\scratch\GestureSpeakAI\system_architecture.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("New system_architecture.png saved successfully!")

if __name__ == '__main__':
    create_system_architecture()
