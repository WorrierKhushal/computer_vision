"""
Chart and Diagram Generation Script for SmartVision-Ed.
Generates publication-quality charts and architectural diagrams for the academic project report.
Author: Khushal Mahajan (24MIM10014)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Styling palette
DARK_BG = "#0d111a"
CARD_BG = "#161c2b"
TEXT_COLOR = "#f1f5f9"
CYAN = "#38bdf8"
EMERALD = "#10b981"
AMBER = "#f59e0b"
ROSE = "#f43f5e"
PURPLE = "#a855f7"

plt.rcParams.update({
    "figure.facecolor": DARK_BG,
    "axes.facecolor": CARD_BG,
    "axes.edgecolor": "#2d3748",
    "axes.labelcolor": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "text.color": TEXT_COLOR,
    "grid.color": "#242c3d",
    "font.sans-serif": "DejaVu Sans",
    "font.family": "sans-serif"
})


def generate_architecture_diagram():
    """Generates visual representation of system architecture."""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Layer boxes
    layers = [
        {"y": 4.6, "title": "Layer 1: Video Capture & Real-Time Ingestion", "items": "Video Stream (30 FPS) | Privacy Filter | Gaussian Face Blurring | Salted SHA-256 Token", "color": CYAN},
        {"y": 3.2, "title": "Layer 2: Computer Vision Perception & Feature Engine", "items": "68-Point Facial Landmarks | Eye Aspect Ratio (EAR) | 3D Head Pose (PnP) | MAR Yawn Detector", "color": PURPLE},
        {"y": 1.8, "title": "Layer 3: Temporal Tracking & Multi-Modal Risk Analytics", "items": "EMA Temporal Smoothing (α=0.25) | CAVS Model | Academic Fusion (Att+Internals+LMS+Vision)", "color": AMBER},
        {"y": 0.4, "title": "Layer 4: Application, Intervention & Presentation", "items": "FastAPI REST Server | Interactive HUD Web Dashboard | Early Warning Alerts | ReportLab PDF Engine", "color": EMERALD},
    ]

    for layer in layers:
        rect = plt.Rectangle((0.5, layer["y"]), 9.0, 1.0, facecolor=CARD_BG, edgecolor=layer["color"], linewidth=2, transform=ax.transData)
        ax.add_patch(rect)
        ax.text(0.8, layer["y"] + 0.65, layer["title"], fontsize=11, fontweight="bold", color=layer["color"])
        ax.text(0.8, layer["y"] + 0.28, layer["items"], fontsize=9, color="#cbd5e1")

    # Arrows between layers
    for y_arrow in [4.6, 3.2, 1.8]:
        ax.annotate("", xy=(5.0, y_arrow), xytext=(5.0, y_arrow + 0.35),
                    arrowprops=dict(arrowstyle="->", color="#94a3b8", lw=2))

    plt.title("SmartVision-Ed: Four-Tier System Architecture\nAuthor: Khushal Mahajan (24MIM10014)",
              fontsize=13, fontweight="bold", pad=15, color="#ffffff")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "architecture_diagram.png")
    plt.savefig(path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {path}")


def generate_workflow_diagram():
    """Generates detailed process workflow diagram."""
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    steps = [
        ("Video Frame\nCapture", 0.8),
        ("Facial Landmark\nExtraction", 2.6),
        ("EAR, MAR & PnP\nHead Pose", 4.4),
        ("Temporal EMA\nAttention Score", 6.2),
        ("CAVS Fusion &\nWarning Trigger", 8.0)
    ]

    for title, x in steps:
        box = plt.Rectangle((x - 0.7, 1.6), 1.4, 1.6, facecolor=CARD_BG, edgecolor=CYAN, linewidth=2)
        ax.add_patch(box)
        ax.text(x, 2.4, title, fontsize=9.5, fontweight="bold", ha="center", va="center", color="#ffffff")

    # Connect with arrows
    for i in range(len(steps) - 1):
        x1 = steps[i][1] + 0.7
        x2 = steps[i + 1][1] - 0.7
        ax.annotate("", xy=(x2, 2.4), xytext=(x1, 2.4),
                    arrowprops=dict(arrowstyle="->", color=EMERALD, lw=2.5))

    plt.title("End-to-End Processing Pipeline Workflow\nAuthor: Khushal Mahajan (24MIM10014)",
              fontsize=13, fontweight="bold", pad=15, color="#ffffff")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "workflow_diagram.png")
    plt.savefig(path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {path}")


def generate_ear_curve():
    """Generates EAR over time curve highlighting normal blinks vs drowsiness."""
    np.random.seed(42)
    frames = np.arange(0, 150)
    # Baseline open eye ~ 0.30 with small natural noise
    ear = 0.30 + np.random.normal(0, 0.015, len(frames))

    # Add quick normal blink at frame 35-37
    ear[35:38] = [0.19, 0.10, 0.20]

    # Add another normal blink at frame 70-72
    ear[70:73] = [0.18, 0.09, 0.21]

    # Add sustained micro-sleep (drowsiness event) from frame 105 to 130
    ear[105:130] = np.random.normal(0.12, 0.015, 25)

    fig, ax = plt.subplots(figsize=(9, 4), dpi=300)
    ax.plot(frames, ear, color=CYAN, lw=2, label="Eye Aspect Ratio (EAR)")
    ax.axhline(0.22, color=AMBER, linestyle="--", lw=1.5, label="Blink Threshold (0.22)")
    ax.axhline(0.18, color=ROSE, linestyle="--", lw=1.5, label="Drowsiness Threshold (0.18)")

    # Highlight drowsiness event
    ax.axvspan(105, 130, color="red", alpha=0.2, label="Drowsiness / Micro-Sleep Episode (>14 frames)")

    ax.set_title("Ocular Dynamics: Eye Aspect Ratio (EAR) vs. Video Frame Sequence\nAuthor: Khushal Mahajan (24MIM10014)", fontsize=11, fontweight="bold")
    ax.set_xlabel("Video Frame Index (30 FPS)")
    ax.set_ylabel("EAR Metric")
    ax.set_ylim(0.05, 0.40)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", fontsize=8.5, facecolor="#1e2536", edgecolor="#2d3748")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "ear_drowsiness_curve.png")
    plt.savefig(path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {path}")


def generate_cavs_cohort_plot():
    """Generates cohort CAVS scores across students."""
    students = ["Khushal (24MIM10014)", "Aarav", "Rohan (Warning)", "Priya", "Aditya (Warning)", "Ananya", "Vikram (Warning)", "Sanya"]
    cavs_scores = [10.6, 25.9, 51.2, 13.2, 41.4, 19.7, 57.8, 17.7]
    colors = [EMERALD, EMERALD, ROSE, EMERALD, ROSE, EMERALD, ROSE, EMERALD]

    fig, ax = plt.subplots(figsize=(9.5, 4.2), dpi=300)
    bars = ax.bar(students, cavs_scores, color=colors, width=0.55, edgecolor="#ffffff", linewidth=0.5)

    ax.axhline(50.0, color=ROSE, linestyle="--", lw=1.5, label="Critical Risk Boundary (CAVS ≥ 50)")
    ax.axhline(30.0, color=AMBER, linestyle="--", lw=1.5, label="Moderate Risk Boundary (CAVS ≥ 30)")

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, h + 1.5, f"{h:.1f}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    ax.set_title("Cohort Academic Vulnerability Index (CAVS) Distribution\nAuthor: Khushal Mahajan (24MIM10014)", fontsize=11, fontweight="bold")
    ax.set_ylabel("CAVS Score (0 - 100, Lower is Better)")
    ax.set_ylim(0, 75)
    ax.grid(True, linestyle=":", alpha=0.6, axis="y")
    ax.legend(loc="upper left", fontsize=8.5, facecolor="#1e2536", edgecolor="#2d3748")
    plt.xticks(rotation=20, ha="right", fontsize=8.5)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "cavs_distribution.png")
    plt.savefig(path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {path}")


if __name__ == "__main__":
    generate_architecture_diagram()
    generate_workflow_diagram()
    generate_ear_curve()
    generate_cavs_cohort_plot()
    print("All report charts generated successfully!")
